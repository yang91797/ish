// pages/top/top.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        processing: false,
        loadingMoreHidden: true,
        indicatorDots: true,
        p:0,
        article_list:[],
        leassonId: '',          // 查看文章详情页的id
        yesSrc: '/images/nav/resizeAf.png',
        noSrc: '/images/nav/resizeBe.png',
        like: false,
        show: false,
        noSearch: false,
        history: [],
        activeCategoryId: 1,
        storage: []      // 文章缓存
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        app.getUserInfo()
        if(wx.getStorageSync("history") != ""){
            this.setData({
                history: wx.getStorageSync("history")
            })
        }
        this.setData({
            categories: [
                { nid: 1, title: "推荐" },
                { nid: 2, title: "生活" },
                { nid: 3, title: "二手" },
                { nid: 4, title: "资料"},
            ],
        
        });
        wx.request({
            url: 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token=22_956uY4sDnIk8zMeTBpKo2jAsS6k176d_YXgQ-jHjMHoMOhfxbSHDmUN8PCK9EQL5EmTuXb34W1dBW0YHqEHOTlbS0hliXI6bcV2dRCi03FRkOWKFR8FTfXGgUD-Km8S3RG9BTaT2e4JCFLrOOMZiAHAUSF',
            method: "POST",
            data:{
                content:'完2347全dfji试3726测asad感3847知qwez到'
            },
            success:function(res){
                console.log(res)
            }
        })
        
    },

    listenerSearchInput: function (e) {
        this.setData({
            searchInput: e.detail.value
        });
       
    },

    getIndex: function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/index"),
            header: app.getRequestHeader(),
            success: function (res) {
                
                var resp = res.data
                if(resp.code != 200){
                    app.alert({"content": res.msg});
                    return;
                }
                
                that.setData({
                    banners: resp.data.advertise,
                    categories: resp.data.category,
                    activeCategoryId: resp.data.category[0].nid,
                    article_list: resp.data.article,
                    
                });
                wx.setStorage({
                    key: "article_list",
                    data: resp.data.article,
                })
                wx.setStorage({
                    key: 'banners',
                    data: resp.data.advertise,
                })
                wx.stopPullDownRefresh()
            }
        });
    },
    
    getArticleList:function(){
        var that = this;
        var article_storage = wx.getStorageSync("article_list")
        var categoryId = that.data.activeCategoryId
        if(that.data.processing){ 
            return;
        }
        
        if(!that.data.loadingMoreHidden){
            return;
        }

        that.setData({
            processing:true
        });
        wx.showLoading({
            title: '正在加载',
            mask: true
        })
        wx.request({
            url: app.buildUrl("/index"),
            method: 'POST',
            header: app.getRequestHeader(),
            data:{
                cat_id: categoryId,
                mix_kw: that.data.searchInput,
                p:that.data.p
            },
            success:function(res){
                wx.hideLoading()
                var resp = res.data;
                if(resp.code != 200){
                    app.alert({"content": resp.msg})
                    return;
                }
                var article_list = resp.data.article;
                var new_article = that.data.article_list.concat(article_list)
                that.setData({
                    article_list: new_article,
                    processing: false,
                    p: that.data.p + 1,
                });
                
                if(resp.data.has_more == 0){
                    that.setData({
                        loadingMoreHidden:false
                    })
                }
            }
        })
    },

    catClick:function(e){
        console.log(e)
        var that = this
        var category_id = e.currentTarget.id
        var formId = e.detail.formId
        var date = new Date().getTime()
        that.setData({
            loadingMoreHidden: true,
            p: 0
        })
        wx.showLoading({
            title: '加载中',
        })
        
        wx.request({
            url: app.buildUrl('/index/'),
            header: app.getRequestHeader(),
            data: {
                cat_id: category_id,
                formId: formId,
                expire: date + 60480000
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
    
    // 查看文章詳情
    seeDetail:function(e){
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
            success:function(res){
                
            }
        })
        that.setData({
            leassonId: e.currentTarget.dataset.id,
        })
        for (let i = 0;i < history.length;i++){

            if (history[i].nid == article.nid){
                history.splice(i, 1)
            }
        }
        
        var re = history.unshift(article)
        
        if(history.length >= 30){
            history.pop()
            
        }
    
        // 设置浏览缓存
        wx.setStorage({
            key: 'history',
            data: history
        })
        
        wx.navigateTo({
           url: '../detail/detail?id=' + e.currentTarget.dataset.id,
       })
       
    },

    // 向后端验证是否需要更新小程序数据
    storages: function(event1, event2){
        var that = this
        var article_list = wx.getStorageSync("article_list")
        var ad = wx.getStorageSync("banners")
        var activeCategoryId = that.data.activeCategoryId
        if (activeCategoryId != 1){
            
            return
        }
        if (article_list.length == 0 || ad.length == 0){
            that.getIndex()
            return
        }
        wx.request({
            url: app.buildUrl("/storage/"),
            header: app.getRequestHeader(),
            data:({
                event1: event1,
                event2: event2
            }),
            success: function(res){
                var resp = res.data.data
               
                that.setData({
                    storage: resp
                })
                if (resp.event1 != ad[ad.length - 1].id || resp.event2 != article_list[0].id) {
                    
                    that.getIndex();
                }else{
                    that.setData({
                        article_list: article_list,
                        banners: ad
                    
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
        
        // article_list[0].id, ad[ad.length - 1].id
        this.storages("Advertise", "Article")
        this.setData({
            loadingMoreHidden: true
        })
    },


    searchData:function(e){
        
        if (!e.detail){
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
    searchShow:function(e){

        if(e.detail){
            var noSearch = false
            
        }else{
            var noSearch = true
        }
        this.setData({
            show: e.detail,
            noSearch: noSearch
        })
        
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
        this.getIndex()
    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {
        this.getArticleList()
    
    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})