// pages/my/my.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        hasUserInfo: false,
        asset: 0,
        yesSrc: '/images/nav/sign.png',
        noSrc: '/images/nav/nosign.png',
        userInfo: null,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
    
        if (app.getCache('user')) {
            this.setData({
                userInfo: wx.getStorageSync("user"),
                hasUserInfo: true
            })
        } 
       
       
    },
    
    login: function (e) {
        
        var that = this;
        if (!e.detail.userInfo) {
            wx.showToast({
                title: '登录失败',
                icon: "none",
                duration: 2000
            })
            return;
        }
        wx.showLoading({
            title: '正在登录',
        })
        var data = e.detail.userInfo;

        wx.login({
            success: function (res) {
                if (!res.code) {
                    app.alert({ 'content': '登录失败，请再次点击！' });
                    return;
                }

                data['code'] = res.code;
                wx.request({
                    url: app.buildUrl('/userinfo/login/'),
                    header: app.getRequestHeader(),
                    method: 'POST',
                    data: data,
                    success: function (res) {
                        if (res.data.code != 200) {
                            app.alert({ 'content': res.data.msg });
                            return;
                        }
                        console.log(res.data.data,"用户授权")
                        app.setCache('user', res.data.data)
                        that.setData({
                            userInfo: res.data.data,
                            hasUserInfo: true,
                            asset: res.data.data.asset,
                        })
                    },
                    complete(){
                        wx.hideLoading()
                    }
                })
            }
        })


    },
    //是否已经签到
    ismsg: function (){
        var that = this
        
        wx.request({
            url: app.buildUrl("/msg/"),
            header: app.getRequestHeader(),
            success:function(res){
                var resp = res.data.data
                wx.stopPullDownRefresh()
                that.setData({
                    sign: resp.sign
                })
                if (resp.msg) {
                    app.globalData.msg = true
                    wx.setTabBarBadge({
                        index: 1,
                        text: 'New'
                    })
                }
                
            }
        })
    },
    change: function(){
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../changeUser/index',
        })
    },
    explain:function(){
        wx.showModal({
            content: 'i币主要用于兑换资料。获取方式：1、每天签到。2、上传资料，别人打赏获得。',
            showCancel: false
        })
    },
    //签到
    ToSign:function(e){
        if (!app.getUserInfo()) {
            return
        }
        var that = this
        var formId = e.detail.formId
        var date = new Date().getTime()
        wx.request({
            url: app.buildUrl("/sign/"),
            method: 'POST',
            header: app.getRequestHeader(),
            data:{
                formId: formId,
                expire: date + 60480000
            },
            success:function(res){
                if (res.data.code == 200){

                    that.setData({
                        asset: that.data.asset + 5,
                        sign: true
                    })
                    app.globalData.msg = true
                    wx.setTabBarBadge({
                        index: 1,
                        text: 'New'
                    })
                }else{
                    wx.showToast({
                        title: '今天已经签过了哦',
                        icon: 'none',
                        duration: 2000
                    })


                }
            }
        })
    },
    collect:function(){
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../collect/index',
        })
       
    },
    reply:function(){
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../reply/index',
        })
    },
    history: function(){
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../history/index',
        })
    },
    about: function(){
        wx.navigateTo({
            url: '../about/index',
        })
    },
    publish:function(){
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../publish/index',
        })
    },
  

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {
        wx.getSetting({
            success(res) {
                console.log(res.authSetting)
                // res.authSetting = {
                //   "scope.userInfo": true,
                //   "scope.userLocation": true
                // }
            }
        })
        var user = wx.getStorageSync("user")
        if(user){
            this.ismsg()
        }
        
    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {
        this.ismsg()
    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {
        
    }
})