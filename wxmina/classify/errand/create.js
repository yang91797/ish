// classify/errand/create.js

const date = new Date()
const app = getApp()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        date: date.getFullYear()+"-"+date.getMonth()+"-"+date.getDate(),
        time: date.getHours()+":"+date.getMinutes()
    },
    
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

    },
    bindDateChange:function(e){
        this.setData({
            date: e.detail.value
        })
    },
    bindTimeChange: function(e){
        this.setData({
            time: e.detail.value
        })
    },

    submit: function(e){
        if (!app.getUserInfo()) {
            return
        }
        var desc = e.detail.value.desc
        var kg = e.detail.value.kg
        var price = e.detail.value.price
        var site = e.detail.value.site
        var outdate = this.data.date + " " + this.data.time
       
        if(!desc || !kg){
            return
        }
        wx.request({
            url: app.buildUrl('/create/errand'),
            header: app.getRequestHeader(),
            method: "POST",
            data:{
                desc: desc,
                kg: kg,
                price: price,
                site: site,
                outdate: outdate
            },
            success: function (res) {
                if (res.data.code == 405) {
                    app.alert({ 'content': res.data.msg });
                    return;
                } else if (res.data.code != 200) {
                    app.alert({ 'content': '发布内容失败了，请重新尝试。' });
                    return;
                }
                wx.redirectTo({
                    url: './index'
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