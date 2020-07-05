// classify/rent/index.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        article_list: [],
        history: [],
        loadingMoreHidden: true,
        p: 0,
        leassonId: '',          // 查看文章详情页的id
        yesSrc: '/images/nav/resizeAf.png',
        noSrc: '/images/nav/resizeBe.png',
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function () {
        
        if (wx.getStorageSync("history") != "") {
            this.setData({
                history: wx.getStorageSync("history")
            })
        }
        this.getRent()
    },

    getRent:function(){
        var that = this
        wx.showLoading({
            title: '正在加载',
            mask: true
        })
        wx.request({
            url: app.buildUrl("/home/rent"),
            header: app.getRequestHeader(),
            data: {
                p: that.data.p
            },
            success: function (res) {
                
                var resp = res.data
                console.log(resp)
                that.setData({
                    article_list: that.data.article_list.concat(resp.data.article)
                })

                wx.setStorage({
                    key: "article_list",
                    data: resp.data.article,
                })
                if (resp.data.has_more == 0) {
                    that.setData({
                        loadingMoreHidden: false
                    })
                }
                wx.stopPullDownRefresh()
            },
            complete:(res)=>{
                wx.hideLoading()
                if(res.data.code != 200){
                    wx.showToast({
                        title: '好像出了点问题',
                        icon: 'none',
                        duration: 1000
                    })
                }
            }
        })
    },
    // 查看文章詳情
    seeDetail: function (e) {
        var that = this
        let history = that.data.history
        let article = that.data.article_list[e.currentTarget.dataset.index]
        var formId = e.detail.formId
        var date = new Date().getTime()
        wx.request({
            url: app.buildUrl('/saveFormId/'),
            method: "POST",
            header: app.getRequestHeader(),
            data: ({
                formId: formId,
                expire: date + 60480000
            }),
            success: function (res) {
                
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

        wx.navigateTo({
            url: '../../detail/rent/index?id=' + e.currentTarget.dataset.id,
        })

    },
    publish: function () {
        wx.navigateTo({
            url: '../add/index?category=' + 2,
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
        this.setData({
            p:0
        })
        this.getRent()
    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {
        this.setData({
            p: this.data.p + 1
        })
        this.getRent()
    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})