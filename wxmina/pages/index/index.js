//index.js
//获取应用实例
const app = getApp()

Page({
    data: {
        userInfo: {},
        regFlag: true
    },
    //事件处理函数
    bindViewTap: function () {
        wx.navigateTo({
            url: '../logs/logs'
        })
    },
    onLoad: function () {

        // 调用验证是否注册的方法
        this.checkLogin();
        var that = this
        setTimeout(function () {
            that.goToIndex();   // 去首页
        }, 3000)
    },


    goToIndex:function(){
        
        wx.switchTab({
            url: '/pages/home/index',
            
        })
    },


    checkLogin:function(){
        //  去后台验证是否已经注册
        var that = this;
        wx.login({
            success:function(res){
                if (!res.code) {
                    app.alert({ 'content': '登录失败，请再次点击！' });
                    return;
                }
                wx.request({
                    url: app.buildUrl('/userinfo/check-reg/'),
                    header: app.getRequestHeader(),
                    method: 'POST',
                    data: {code:res.code},
                    success: function (res) {
                        
                        if (res.data.code != 200) {
                            app.alert({ 'content': res.data.msg })
                            app.globalData.userInfo = null
                            wx.removeStorage({
                                key: 'user',
                                success(res) {
                                   
                                }
                            })
                           
                            return;
                        }
                       
                        app.setCache('user', res.data.data)
                        app.globalData.userInfo = res.data.data
                        
                    },
                    fail: function(res){
                        wx.showToast({
                            title: '哇！服务器似乎挂了',
                            icon: "none",
                            duration: 3000
                        })
                    }
                    
                })
                
            }
        })

    },

})
