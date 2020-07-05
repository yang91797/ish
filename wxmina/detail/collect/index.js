// detail/collect/index.js

const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        id: null,
        phone: Array,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        app.getUserInfo()
        this.setData({
            id: options.id
        })

        this.seePhone()
    },

    seePhone: function(){
        wx.request({
            url: app.buildUrl('/details/collect'),
            header: app.getRequestHeader(),
            data:{
                id: this.data.id
            },  
            success:(res)=>{
                var resp = res.data.data
                this.setData({
                    phone: resp.phone
                })
            }
        })
    },
    call:function(e){
        wx.makePhoneCall({
            phoneNumber: e.currentTarget.dataset.phone
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