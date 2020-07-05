// detail/learn/index.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        article_id: Number,
        show: false,
        show_text: false,
        yesSrc: '/images/nav/resizeAf.png',
        noSrc: '/images/nav/resizeBe.png',
        like: false,
        collect: false,
        dkcontent: null,
        reimage: false,
        study_url: false,
        images: [],
        likeNum: 0,
        likeUp: true,
        type: 'text',
        comment: Array,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        app.getUserInfo()
        this.setData({
            article_id: options.id
        })
        this.getArticle()
    },
    report: function () {
        wx.navigateTo({
            url: '../../pages/report/index',
        })
    },
    userinfo: function (e) {
        wx.navigateTo({
            url: '../../pages/viewuser/index?id=' + e.currentTarget.dataset.id,
        })
    },
    getArticle: function (e) {
        var that = this
        wx.request({
            url: app.buildUrl('/details/second'),
            header: app.getRequestHeader(),
            data: {
                article_id: this.data.article_id
            },
            success: function (res) {
                var resp = res.data.data
                var article = resp.article
                console.log(res.data)
                that.setData({
                    article: article,
                    dkcontent: article.content,
                    likeNum: article.up_count,
                    images: article.img,
                    type: article.type,
                    study_url: resp.study_url,
                    comment: resp.comment
                })
                if (that.data.images.length == 0) {
                    that.setData({
                        images: false
                    })
                }
                if (resp.likeUp) {
                    that.setData({
                        like: true
                    })
                }
                if (resp.collect) {
                    that.setData({
                        collect: true
                    })
                }
                if (that.data.type != 'text') {
                    that.setData({
                        show: true
                    })
                    wxparse.wxParse('dkcontent', that.data.type, that.data.dkcontent, that, 5)
                } else {
                    that.setData({
                        show_text: true
                    })
                }

            }

        })
    },

    // 收藏
    onCollectionTap: function (e) {
        var that = this
        wx.request({
            url: app.buildUrl("/collect/"),
            method: "POST",
            header: app.getRequestHeader(),
            data: {
                articleId: that.data.article_id
            },
            success: function (res) {
                var resp = res.data
                if (resp.code == 200) {
                    that.setData({
                        collect: !that.data.collect
                    })
                }
            }
        })
    },

    // 点赞
    onUpTap: function () {
        var that = this
        wx.request({
            url: app.buildUrl('/like/'),
            header: app.getRequestHeader(),
            data: {
                nid: that.data.article_id
            },
            success: function (res) {
                if (res.data.data.code = 200) {
                    let like = that.data.like
                    let likeNum = like ? that.data.likeNum - 1 : that.data.likeNum + 1
                    that.setData({
                        like: !like,
                        likeNum: likeNum
                    })
                }
            }
        })

    },
    // 图片评论
    reimage: function (e) {
        this.setData({
            reimage: e.detail
        })
    },

    // 查看文章图片大图
    lookImage(e) {
        wx.previewImage({
            urls: this.data.images,
            current: this.data.images[e.currentTarget.dataset.index]
        })
    },
    reLoad: function (e) {
        this.onLoad({ id: e.detail })
    },
    close: function (e) {
        var article_id = this.data.article_id
        this.setData({
            reimage: e.detail
        })
        this.onLoad({ "id": article_id })
    },
    getLink: function () {
        var that = this
        wx.showModal({
            title: '确认',
            content: '确定打赏？',
            success(res) {
                if (res.confirm) {
                    wx.request({
                        url: app.buildUrl('/study_link/'),
                        header: app.getRequestHeader(),
                        data: {
                            article_id: that.data.article_id
                        },
                        success: function (res) {
                            var resp = res.data
                            if (resp.code == 200) {

                                that.setData({
                                    study_url: resp.data
                                })
                            }
                        }
                    })
                }

            }
        })

    },

    // 设置剪贴板内容
    setcp: function () {
        var that = this
        wx.setClipboardData({
            data: that.data.study_url,
            success(res) {
                wx.showToast({
                    title: '已复制到剪贴板',
                    icon: 'none',
                    duration: 2000
                })
            }
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