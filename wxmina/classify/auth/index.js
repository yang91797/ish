// classify/auth/index.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        code: "",
        rsa: "",
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        this.getCode()
    },
    getCode: function(){
        wx.request({
            url: app.buildUrl("/auth/jou"),
            header: app.getRequestHeader(),
            success:(res)=>{
                var resp = res.data
                if(resp.code == 200){
                    this.setData({
                        code: resp.data.code,
                        rsa: resp.data.rsa,
                    })
                }else{
                    wx.showToast({
                        title: '获取验证码失败',
                        icon: "none",
                        duration: 2000
                    })
                }
            }
        })
    },
    refresh: function(){
        this.getCode()
    },

    submit: function(e){
        var formId = e.detail.formId
        var user = e.detail.value.user
        var pwd = e.detail.value.pwd
        var code = e.detail.value.code
        wx.request({
            url: app.buildUrl("/auth/jou"),
            header: app.getRequestHeader(),
            method: "POST",
            data:{
                user: user,
                pwd: pwd,
                code: code,
                formId: formId,
                rsa: this.data.rsa,
            },
            success:(res)=>{
                console.log(res)
                if(res.data.code == 200){
                    wx.showToast({
                        title: '验证成功',
                        icon: "success",
                        duration: 2000
                    })
                    wx.redirectTo({
                        url: '../errand/index',
                    })
                }else{
                    wx.showToast({
                        title: '验证失败,请重新输入',
                        icon: "none",
                        duration: 2000
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

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})