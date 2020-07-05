// pages/detail/detail.js
const app = getApp()
var util = require('../../utils/util.js');
let wxparse = require('../../wxParse/wxParse.js');

Page({
    /**
     * 页面的初始数据
     */
    data: {
        dkheight: 300,
        article_id: '',
        show: false,
        show_text: false,
        vie: "vie",
        yesSrc: '/images/nav/resizeAf.png',
        noSrc: '/images/nav/resizeBe.png',
        like: false,
        collect: false,
        study_url: false,
        dkcontent: null,
        reimage: false,
        images: [],
        title: Number,
        time: null,
        author: null,
        openid: null,
        avatar: null,
        gold: 0,
        likeNum: 0,
        likeUp: true,
        commentNum: 0,
        category: null,
        category_id: null,
        type: 'text',
        study_url: null,
        content: null
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function(options) {
        console.log("????")
        app.getUserInfo()
        var that = this;
        that.setData({
            article_id: options.id
        })
        
        that.getArticle()

    },
    userinfo: function(e){
        wx.navigateTo({
            url: '../viewuser/index?id=' + e.currentTarget.dataset.id,
        })
    },
    getArticle: function(e) {
        var that = this
        wx.request({
            url: app.buildUrl('/details/'),
            header: app.getRequestHeader(),
            data: {
                article_id: this.data.article_id
            },
            success: function(res) {
                var resp = res.data.data
                var article = resp.article
               
                that.setData({
                    dkcontent: article.content,
                    title: article.title,
                    time: article.create_time,
                    author: article.user__username,
                    avatar: article.user__avatar,
                    openid: article.user__openid,
                    gold: article.study_url__gold,
                    likeNum: article.up_count,
                    likeUp: resp.likeUp,
                    readCount: article.read_count,
                    commentNum: article.comm_count,
                    category: article.category__title,
                    category_id: article.category_id, 
                    images: article.img,
                    type: article.type,
                    study_url: resp.study_url,
                    comment: resp.comment
                })
                if (that.data.images.length == 0){
                    that.setData({
                        images: false
                    })
                }
                if (resp.likeUp){
                    that.setData({
                        like: true
                    })
                }
                if (resp.collect){
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

   

    catchhide: function () {
        this.setData({
            releaseFocus: true
        })
        // console.log(this.data.releaseFocus)
    },

    lookImage(e){
       
        wx.previewImage({
            urls: this.data.images,
            current: this.data.images[e.currentTarget.dataset.index]
        })
    },
    reLoad: function(e){
        this.onLoad({ id: e.detail})
    },
    getLink:function(){
        var that = this
        wx.showModal({
            title: '确认',
            content: '确定打赏？',
            success(res){
                if (res.confirm){
                    wx.request({
                        url: app.buildUrl('/study_link/'),
                        header: app.getRequestHeader(),
                        data: {
                            article_id: that.data.article_id
                        },
                        success: function (res) {
                            var resp = res.data
                            if (resp.code == 200){
                                
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
    setcp: function(){
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
    onUpTap:function(){
        var that = this
        wx.request({
            url: app.buildUrl('/like/'),
            header: app.getRequestHeader(),
            data: {
                nid: that.data.article_id
            },
            success: function (res) {
                if (res.data.data.code = 200){
                    let like = that.data.like
                    let likeNum = like ? that.data.likeNum - 1 : that.data.likeNum + 1
                    that.setData({
                        like:!like,
                        likeNum: likeNum
                    })
                }
            }
        })

    },
    onCollectionTap:function(e){
        var that = this
        wx.request({
            url: app.buildUrl("/collect/"),
            method: "POST",
            header: app.getRequestHeader(),
            data:{
                articleId: that.data.article_id 
            },
            success:function(res){
                var resp = res.data
                if(resp.code == 200){
                    that.setData({
                        collect: !that.data.collect
                    })
                }
            }
        })
    },
    reimage:function(e){
        this.setData({
            reimage: e.detail
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