// classify/errand/index.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        errand: [],
        p: 0,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        
        this.errandList()
    },
    errandList:function(){
        var that = this
        wx.request({
            url: app.buildUrl('/home/errand'),
            header: app.getRequestHeader(),
            data:{
                p: that.data.p
            },
            success: function (res) {
                var resp = res.data
                console.log(resp)
                that.setData({
                    errand: that.data.errand.concat(resp.data.article)
                })

            }
        })
    },
    publish: function(){
        wx.navigateTo({
            url: './create',
        })
    },
    seeDetail:function(e){
        var id = e.currentTarget.dataset.id
        wx.navigateTo({
            url: '../../detail/errand/index?id=' + id,
        })
    },
    take:function(e){
        var that = this
        wx.showModal({
            content: '确定接此单?',
            success(res) {
                if (res.confirm) {
                    that.seePhone(e)
                } else if (res.cancel) {
                    console.log('用户点击取消')
                }
            }
        })
    },

    seePhone:function(e){
        var id = e.currentTarget.dataset.id
        wx.request({
            url: app.buildUrl('/details/phone'),
            header: app.getRequestHeader(),
            data: {
                id: id
            },
            success: function (res) {
                var resp = res.data
                console.log(resp)
                var wechat = resp.data.wechat
                var qq = resp.data.qq
                var telephone = resp.data.telephone
                if (wechat){
                    wx.setClipboardData({
                        data: wechat,
                        success(res) {
                            wx.showToast({
                                title: '已复制对方微信号，请自行添加好友联系',
                                icon: 'success',
                                duration: 2000
                            })

                        }
                    })
                }else if(qq){
                    wx.setClipboardData({
                        data: qq,
                        success(res) {
                            wx.showToast({
                                title: '已复制对方QQ号，请自行添加好友联系',
                                icon: 'success',
                                duration: 2000
                            })

                        }
                    })
                }else if(telephone){
                    wx.showModal({
                        title: "温馨提示",
                        content: '联系对方请礼貌用语&&',
                        confirmText: "确认呼叫",
                        success(res) {
                            if (res.confirm) {
                                wx.makePhoneCall({
                                    phoneNumber: telephone
                                })
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

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})