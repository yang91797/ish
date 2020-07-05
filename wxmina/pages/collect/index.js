// pages/collect/index.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        yesSrc: '/images/nav/resizeAf.png',
        noSrc: '/images/nav/resizeBe.png',
        like: false,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        app.getUserInfo()
        this.collect()
    },
    collect:function(){
        var that = this
        wx.request({
            url: app.buildUrl('/collect/'),
            header: app.getRequestHeader(),
            success: function (res) {
                if (res.data.code == 200) {

                    that.setData({
                        article_list: res.data.data
                    })
                }
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