import re
from django.shortcuts import HttpResponse
# from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request, *args, **kwargs):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入的时候触发执行
        :param request:
        :return:
        """
        
        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/', '/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """
        current_url = request.path_info
        for valid_url in settings.PERMISSION_VALID_URL:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None
            
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_list:
            return HttpResponse('未获取到用户权限信息，请登录！')
        
        flag = False

        # 3. 对用户请求的url进行匹配
        request.current_breadcrumb_list = [
            {'title': '首页', 'url': '#'}
        ]
        static_url = settings.STATIC_FILES
        for item in static_url:
            if re.search(item, request.path_info):
                flag = True
        for name, item in permission_list.items():
            url = item['url']
            regex = "^%s$" % url
            if re.match(regex, request.path_info):
                flag = True
                pid = item['pid']
                pid_name = item['pid_name']
                pid_url = item['pid_url']
                if pid:
                    request.current_permission_pid = item['pid']
                    request.current_breadcrumb_list.extend([
                        {'title': permission_list[pid_name]['title'], 'url': pid_url},
                        {'title': item['title'], 'url': url, 'class': 'active'}
                    ])
                else:
                    request.current_permission_pid = item['id']
                    request.current_breadcrumb_list.append(
                        {'title': item['title'], 'url': url, 'class': 'active'}
                    )
                break

        # for url in permission_list:
        #     reg = "%s$" % url
        #     if re.match(reg, current_url):
        #         flag = True
        #         break
                
        if not flag:
            return JsonResponse({'status': False, 'error': '无权访问'})
        
        