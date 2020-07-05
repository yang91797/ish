// pages/publish/index.js

const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        article_list: [],
        categories: [
            { nid: 0, title: "二手", isValid: [
                {name: "二手", value: "已出"}
            ]},
            { nid: 1, title: "资料"},
            { nid: 2, title: "租借", isValid:[
                {name: "租借", value:"已租"}
            ]},
            {nid: 3, title: "跑腿", isValid:[
                {name: "跑腿", value: "已完成"}
            ]}
        ],
        activeCategoryId: 0,
        p: 0,
        yesSrc: '/images/nav/resizeAf.png',
        noSrc: '/images/nav/resizeBe.png',
        loadingMoreHidden: true,

    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        app.getUserInfo()
        this.getArticleList()

    },
    checkboxChange: function(e){
        console.log(e)
        var category = e.currentTarget.dataset.category
        var id = e.currentTarget.dataset.id
        wx.showLoading({
            title: '状态更改',
        })
        wx.request({
            url: app.buildUrl('/my/valid'),
            header: app.getRequestHeader(),
            method: "POST",
            data:{
                category: category,
                id: id
            },
            success:(res)=>{
                var resp = res.data
                console.log(resp)
            },
            complete:(res)=>{
                wx.hideLoading()
                if(res.data.code != 200){
                    wx.showToast({
                        title: '状态更改失败',
                        icon: "none",
                        duration: 2000
                    })
                }
            }
        })
    },
    
    // 获取文章列表
    getArticleList: function () {
        var that = this;
        var categoryId = that.data.activeCategoryId
        var category = that.data.categories[categoryId].title
        wx.showLoading({
            title: '正在加载',
            mask: true
        })
        wx.request({
            url: app.buildUrl("/my/publish"),
            header: app.getRequestHeader(),
            method: "POST",
            data: {
                p: that.data.p,
                category: category
            },
            success: function (res) {
                wx.hideLoading()
                var resp = res.data;
                console.log(resp, "??")
                if (resp.code != 200) {
                    app.alert({ "content": resp.msg })
                    return;
                }
                var article_list = resp.data.article;
                var new_article = that.data.article_list.concat(article_list)
                that.setData({
                    article_list: new_article,
                    processing: false,
                });

                if (resp.data.has_more == 0) {
                    that.setData({
                        loadingMoreHidden: false
                    })
                }
            }
        })
    },

    catClick: function (e) {
        console.log(e)
        var that = this
        var category_id = e.currentTarget.id
        var formId = e.detail.formId
        var category = that.data.categories[category_id].title
        that.setData({
            loadingMoreHidden: true,
            p: 0
        })
        wx.showLoading({
            title: '加载中',
        })
        wx.request({
            url: app.buildUrl('/my/publish'),
            header: app.getRequestHeader(),
            method: "POST",
            data: {
                category: category,
                formId: formId,
                p: 0
            },
            success: function (res) {
                wx.hideLoading()
                that.setData({
                    article_list: res.data.data.article,
                    activeCategoryId: e.currentTarget.id
                })
            }
        })
        
    },

    seeDetail: function (e) {
        this.setData({
            leassonId: e.currentTarget.dataset.id
        })
        wx.navigateTo({
            url: '../detail/detail?id=' + e.currentTarget.dataset.id,
        })
    },
    del: function (e) {
        var that = this
        var id = e.currentTarget.dataset.id
        
        wx.showModal({
            title: '删除',
            content: '确认删除？',
            success(res) {
                if (res.confirm) {
                    wx.request({
                        url: app.buildUrl('/delete/'),
                        method: "POST",
                        header: app.getRequestHeader(),
                        data: {
                            articleId: id,
                            type: 'publish'
                        },
                        success(res) {

                            var resp = res.data
                            if (resp.code == 200) {
                                that.setData({
                                    article_list: []
                                })
                                that.onLoad()
                            }
                        }
                    })
                }
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
        this.setData({
            p: this.data.p + 1
        })
        this.getArticleList()
    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})