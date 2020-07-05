import requests
import time
import os
import sys


path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "record", "send.txt")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ish import settings
from backstage.utils import sqlheper
sql = sqlheper.SqlHelper()


def send_teleplate(request, openid, article, keyword2, keyword3, keyword4):
    """
    发送模板消息
    :return:
    """
    user_id = request.META.get('HTTP_AUTHORIZATION')
    user_openid = request.META.get("HTTP_IDMD5")
    # expire_list = models.Formid.objects.filter(user_id=user_id).values("id", "expire")
    # now_date = time.time()
    # username = models.Customer.objects.filter(nid=user_id, openid=openid).values("username").first()
    # keyword1 = username.get("username")
    # for item in expire_list:
    #     if float(item.get("expire")) < float(now_date):
    #         models.Formid.objects.filter(id=item.get("id")).delete()
    # formId = models.Customer.objects.filter(openid=openid).values("formid__formid").first().get("formid__formid")
    #
    # url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
    #     settings.MINA_APP.get('appid'), settings.MINA_APP.get('appkey'))
    # access_token = requests.get(
    #     url=url,
    #     headers={
    #         'content-type': 'application/x-www-form-urlencoded',
    #         'referer': 'https://mp.weixin.qq.com/debug/cgi-bin/apiinfo?t=index&type=%E5%9F%BA%E7%A1%80%E6%94%AF%E6%8C%81&form=%E8%8E%B7%E5%8F%96access_token%E6%8E%A5%E5%8F%A3%20/token&token=&lang=zh_CN',
    #         'upgrade-insecure-requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3505.400',
    #
    #     },
    # )
    #
    # access_token = access_token.json().get("access_token")
    # response = requests.post(
    #     url="https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s" % access_token,
    #     json={
    #         "touser": openid,
    #         "template_id": "DN8O2wAjWDh_VxuGMntC7xk_3lNBUj31k5IBP8eqAdQ",
    #         "page": "pages/detail/detail?id=%s" % article,
    #         "form_id": formId,
    #         "data": {
    #             "keyword1": {
    #                 "value": keyword1
    #             },
    #             "keyword2": {
    #                 "value": keyword2
    #             },
    #             "keyword3": {
    #                 "value": keyword3
    #             },
    #             "keyword4": {
    #                 "value": keyword4
    #             }
    #         }
    #     }
    # )
    #
    # models.Formid.objects.filter(formid=formId).delete()
    # print(response.json())


def send_serve():
    """
    发送服务消息
    :param request:
    :return:
    """
    comment_list = sql.get_list("""
                            select wxapi_comment.content, 
                                    wxapi_comment.create_time,
                                    wxapi_comment.nid,
                                    wxapi_article.user_id,
                                    wxapi_comment.user_id,
                                    ancestor_id, 
                                    title, 
                                    parent_comment_id, 
                                    openid,
                                    username,
                                    article_id
                                    from wxapi_comment 
                                            inner join wxapi_article on wxapi_article.nid = wxapi_comment.article_id
                                            inner join wxapi_customer on wxapi_customer.nid = wxapi_comment.user_id
                                    where wxapi_comment.status =1 and send = False
    
    
    """, [])
    print(comment_list)
    expire_list = sql.get_list("select id, expire from wxapi_formid", [])

    now_date = time.time()

    expire_item = []
    for item in expire_list:
        if float(item.get("expire")) < float(now_date):
            expire_item.append(item.get('id'))
    expire_item = tuple(expire_item)

    if expire_item:
        sql.modify("delete from wxapi_formid where id in %s", [expire_item])

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        settings.MINA_APP.get('appid'), settings.MINA_APP.get('appkey'))
    access_token = requests.get(
        url=url
    )
    access_token = access_token.json().get("access_token")
    for i in comment_list:
        keyword1 = i.get("username")
        keyword3 = i.get("content")
        if keyword3 == "null":
            keyword3 = "[图片]"
        keyword4 = i.get("create_time").strftime('%Y-%m-%d %H:%M')
        article = i.get("article_id")
        if i.get("parent_comment_id"):
            comment = sql.get_one("""
                                        select openid,
                                                formid,
                                                wxapi_comment.user_id
                                        from wxapi_comment 
                                                inner join wxapi_article on wxapi_article.nid = wxapi_comment.article_id
                                                inner join wxapi_customer on wxapi_customer.nid = wxapi_comment.user_id
                                                inner join wxapi_formid on wxapi_formid.user_id = wxapi_comment.user_id
                                        where wxapi_comment.status =1 and wxapi_comment.nid=%s


                """, [i.get("parent_comment_id")])
            print(comment, "))))")
            if not comment or i.get("wxapi_comment.user_id") == comment.get("user_id"):
                sql.modify("update wxapi_comment set send = 1 where nid = %s", [i.get("nid")])
                continue
            openid = comment.get("openid")
            formId = comment.get("formid")
            keyword2 = "您评论内容有新回复"

        else:
            comment = sql.get_one("""
                                    select openid,
                                            formId
                                    from wxapi_comment
                                            inner join wxapi_article on wxapi_article.nid = wxapi_comment.article_id
                                            inner join wxapi_customer on wxapi_customer.nid = wxapi_article.user_id
                                            inner join wxapi_formid on wxapi_formid.user_id = wxapi_article.user_id
                                    where wxapi_comment.status =1 and wxapi_comment.nid=%s
            
            """, [i.get("nid")])
            print(comment)
            if not comment or i.get("user_id") == i.get("wxapi_comment.user_id"):
                sql.modify("update wxapi_comment set send = 1 where nid = %s", [i.get("nid")])
                continue
            openid = comment.get("openid")
            formId = comment.get("formId")
            keyword2 = "您发布的内容有新评论"

        print(comment)
        print(keyword1, keyword2, keyword3, keyword4)

        # response = requests.post(
        #     url="https://api.weixin.qq.com/cgi-bin/message/wxopen/template/uniform_send?access_token=%s" % access_token,
        #     json={
        #         "touser": openid,
        #         "weapp_template_msg": {
        #             "template_id": "DN8O2wAjWDh_VxuGMntC7xk_3lNBUj31k5IBP8eqAdQ",
        #             "page": "pages/detail/detail?id=%s" % article,
        #             "form_id": formId,
        #             "data": {
        #                 "keyword1": {
        #                     "value": keyword1
        #                 },
        #                 "keyword2": {
        #                     "value": keyword2
        #                 },
        #                 "keyword3": {
        #                     "value": keyword3
        #                 },
        #                 "keyword4": {
        #                     "value": keyword4
        #                 }
        #             },
        #
        #         },
        #     }
        # )
        #
        # print(response.text)
        # sql.modify("delete from wxapi_formid where formid=%s", [formId])
        #
        # date = time.strftime("%Y-%m-%d %H:%M:%S")
        # msg = "%s:%s:%s" % (i.get("nid"), response.text, date)
        # with open(path, mode="a+", encoding="utf8") as f:
        #     f.write(msg + '\n')
        # if response.json().get("errcode") == 0:
        #     sql.modify("update wxapi_comment set send = 1 where nid = %s", [i.get("nid")])


# send_serve()


def msgSecCheck():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        settings.MINA_APP.get('appid'), settings.MINA_APP.get('appkey'))
    access_token = requests.get(
        url=url
    )
    print(access_token.text)
    response = requests.post(
        url="https://api.weixin.qq.com/wxa/msg_sec_check?access_token=%s" % access_token.json().get("access_token"),
        json={
            "content": "特3456书yuuo莞6543李zxcz蒜7782法fgnv级"
        }
    )
    print(response.text)

msgSecCheck()