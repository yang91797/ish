//app.js
App({

    getUserInfo: function() {
        var user = this.getCache("user")
        if (!user) {
            wx.showModal({
                title: '授权登录',
                content: '请到“我的”主页授权登录',
                success(res) {
                    if (res.confirm) {
                        wx.switchTab({
                            url: '/pages/my/my',
                        })
                    }
                }
            })
            
            return false
        }
        return true
    },


    onLaunch: function() {
        // 展示本地存储能力
        var logs = wx.getStorageSync('logs') || []
        logs.unshift(Date.now())
        wx.setStorageSync('logs', logs)

        // 登录
        wx.login({
            success: res => {
                // 发送 res.code 到后台换取 openId, sessionKey, unionId
            }
        })
        // 获取用户信息
        wx.getSetting({
            success: res => {
                if (res.authSetting['scope.userInfo']) {
                    // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
                    wx.getUserInfo({
                        success: res => {
                            // 可以将 res 发送给后台解码出 unionId
                            // this.globalData.userInfo = res.userInfo

                            // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
                            // 所以此处加入 callback 以防止这种情况
                            if (this.userInfoReadyCallback) {
                                this.userInfoReadyCallback(res)
                            }
                        }
                    })
                }
            }
        })
    },
    globalData: {
        userInfo: null,
        domain: "https://ishdf.com/wxapi",
        msg: false,
        phone: true
    },

    alert: function(params) {
        var title = params.hasOwnProperty('title') ? params['title'] : '江海大i生活提示您';
        var content = params.hasOwnProperty('content') ? params['content'] : '';
        wx.showModal({
            title: title,
            content: content,
            showCancel: false,
            success: function(res) {
                if (res.confirm) { //用户点击确定
                    if (params.hasOwnProperty('cb_confirm') && typeof(params.cb_confirm) == "function") {
                        params.cb_confirm();
                    }
                } else {
                    if (params.hasOwnProperty('cb_cancel') && typeof(params.cb_cancel) == "function") {
                        params.cb_cancel();
                    }
                }
            }
        })
    },

    getRequestHeader: function() {
        var user = this.getCache('user')
        if(user){
            var nid = this.getCache("user").nid
            var idmd = this.getCache("user").openid
        }
        else{
            var nid = 0
            var idmd = 0
        }
        return {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': nid,
            'IdMd5': idmd
        }
    },

    // 构建url
    buildUrl: function(path, params) {
        var url = this.globalData.domain + path;
        var _paramUrl = "";
        if (params) {
            _paramUrl = Object.keys(params).map(function(k) {
                return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=");
            }).join("&");
            _paramUrl = "?" + _paramUrl;
        }
        return url + _paramUrl;
    },

    // 读取缓存
    getCache: function(key) {
        var value = undefined
        try {
            value = wx.getStorageSync(key);

        } catch (e) {

        }
        return value
    },


    //  设置缓存
    setCache: function(key, value) {
        wx.setStorage({
            key: key,
            data: value,
        });
    }


})