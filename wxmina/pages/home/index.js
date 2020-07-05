// pages/home/index.js

const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        show: false,
        noSearch: false,
        banners: [],
        searchInput: "",
        search_list: [],
        ad_center: Array,
        history: [],
        infoContent: "本平台为自由发帖平台，请自行辨别信息的真实性，注意自身和财产安全，有问题联系客服，或加入江海大i生活反馈交流群《1026426864》"
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function(options) {
        this.getHome()
        if (wx.getStorageSync("history") != "") {
            this.setData({
                history: wx.getStorageSync("history")
            })
        }
    },
    //是否有消息
    ismsg: function() {
        var that = this
        wx.request({
            url: app.buildUrl("/msg/"),
            header: app.getRequestHeader(),
            success: function(res) {
                var resp = res.data.data
                wx.stopPullDownRefresh()
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
    copy: function() {
        wx.setClipboardData({
            data: this.data.infoContent,
            success(res) {
                wx.showToast({
                    title: '已复制到剪贴板',
                    icon: 'none',
                    duration: 2000
                })
            }
        })
    },

    getHome: function() {
        var that = this;
        wx.request({
            url: app.buildUrl("/home/advertise"),
            header: app.getRequestHeader(),
            success: function(res) {
                var resp = res.data
                if(res.statusCode == 502){
                    wx.showToast({
                        title: '哇！服务器似乎挂了',
                        icon: 'none',
                        duration: 3000
                    })
                    return
                }
                if (resp.code != 200) {
                    wx.showToast({
                        title: '加载失败',
                        icon: 'none',
                        duration: 3000
                    })

                    return;
                }
                
                if (!resp.data.phone && app.globalData.userInfo) {
                    wx.showModal({
                        title: '完善信息',
                        content: '为保证功能的正常使用，请至少填写一种联系方式(电话/微信/QQ)',
                        success(res) {
                            if (res.confirm) {
                                wx.navigateTo({
                                    url: '../changeUser/index',
                                })
                            }
                        }
                    })
                    app.globalData.phone = false
                }

                that.setData({
                    banners: resp.data.advertise,
                    ad_center: resp.data.ad_center
                })
                var infocontent = resp.data.info
                if (infocontent){
                    that.setData({
                        infoContent: infocontent.content 
                    })
                }
                wx.setStorage({
                    key: 'banners',
                    data: resp.data.advertise,
                })
            }

        })
    },
    // 查看文章詳情
    seeDetail: function(e) {
        var that = this
        let history = that.data.history
        let article = that.data.search_list[e.currentTarget.dataset.index]
        let category = e.currentTarget.dataset.ctg
        let article_id = e.currentTarget.dataset.id
        var formId = e.detail.formId
        
        wx.request({
            url: app.buildUrl('/saveFormId/'),
            method: "POST",
            header: app.getRequestHeader(),
            data: ({
                formId: formId,
            }),
            success: function(res) {

            }
        })
        that.setData({
            leassonId: e.currentTarget.dataset.id,
        })
        for (let i = 0; i < history.length; i++) {

            if (history[i].nid == article.nid) {
                history.splice(i, 1)
            }
        }

        var re = history.unshift(article)

        if (history.length >= 30) {
            history.pop()

        }

        // 设置浏览缓存
        wx.setStorage({
            key: 'history',
            data: history
        })
        if (category == "二手"){
            wx.navigateTo({
                url: '../../detail/second/index?id=' + e.currentTarget.dataset.id,
            })
        }else if(category == "资料"){
            wx.navigateTo({
                url: '../../detail/learn/index?id=' + article_id,
            })
        }else if (category == "租借"){
            wx.navigateTo({
                url: '../../detail/rent/index?id=' + article_id,
            })
        }
        

    },

    secondary: function() {
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../../classify/second/index'
        })
    },
    study: function() {
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../../classify/learn/index',
        })
    },
    rent: function() {
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../../classify/rent/index',
        })
    },

    errand: function() {
        // 跑腿
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../../classify/errand/index',
        })
        // wx.request({
        //     url: app.buildUrl("/auth/jou/"),
        //     header: app.getRequestHeader(),
        //     data:{
        //         auth: "auth"
        //     },
        //     success: (res)=>{
        //         var resp = res.data
        //         console.log(resp)
        //         if(resp.code == 401){
        //             wx.showModal({
        //                 title: '身份认证',
        //                 content: '为保证信息安全，需要进行身份认证，是否继续？',
        //                 success(res){
        //                     if (res.confirm) {
        //                         wx.navigateTo({
        //                             url: '../../classify/auth/index',
        //                         })
        //                     } else if (res.cancel) {
        //                         console.log('用户点击取消')
        //                     }
        //                 }
        //             })
        //         }else if(resp.code == 200){
        //             wx.navigateTo({
        //                 url: '../../classify/errand/index',
        //             })
        //         }
        //     }
        // })

    },

    collect: function () {
        if (!app.getUserInfo()) {
            return
        }
        wx.navigateTo({
            url: '../../classify/collect/index',
        })
    },

    ad_article: function(e) {
        wx.navigateTo({
            url: '../../detail/ad_head/index?nid=' + e.currentTarget.dataset.nid,
        })
    },
    listenerSearchInput: function(e) {
        this.setData({
            searchInput: e.detail.value
        });

    },
    searchData: function(e) {
        
        if (!e.detail) {
            this.setData({
                noSearch: true,
                search_list: e.detail
            })
            return
        }
        this.setData({
            search_list: e.detail
        })
    },
    look: function(e) {
        wx.navigateTo({
            url: '../../detail/ad_head/index?nid=' + e.detail.id,
        })
    },
    searchShow: function(e) {

        if (e.detail) {
            var noSearch = false

        } else {
            var noSearch = true
        }
        this.setData({
            show: e.detail,
            noSearch: noSearch
        })

    },

   
    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function() {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function() {
        var user = wx.getStorageSync("user")
        if (user) {
            this.ismsg()
        }

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function() {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function() {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function() {
        this.ismsg()

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function() {

    }
})