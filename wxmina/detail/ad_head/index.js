// detail/tabhead/index.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        nid: "",
        ad_detail: null,
        ad_image: Array,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        this.setData({
            nid: options.nid
        })
        console.log(options)
        this.getContent()
    },
    getContent:function(){
        console.log(this.data.nid)
        wx.request({
            url: app.buildUrl('/home/advertise/'),
            header: app.getRequestHeader(),
            method: "POST",
            data: {
                nid: this.data.nid
            },
            success: (res) => {
                var resp = res.data
                console.log(resp)
                this.setData({
                    ad_detail: resp.data.ad_detail,
                    ad_image: resp.data.ad_image
                })
                console.log(resp.data,"?")
            }
        })
    },
    lookImage:function(e){
        
        wx.previewImage({
            urls: this.data.ad_image,
            current: this.data.ad_image[e.currentTarget.dataset.index]
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