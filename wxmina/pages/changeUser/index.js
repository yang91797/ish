// pages/changeUser/index.js
const app = getApp()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        userinfo: {},
        sex:[
            { number: 0, value: "不详"},
            {number: 1, value: '男'},
            {number: 2, value: "女"}
        ],
        avatar: '',
        files: {},
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        this.change()
    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },
    change: function(){
        var that = this
        wx.request({
            url: app.buildUrl("/changeUser/"),
            header: app.getRequestHeader(),
            success(res){
                var userinfo = res.data.data
                that.setData({
                    userinfo: userinfo,
                    avatar: userinfo.avatar
                })
                
            }
        })
    },
    radioChange:function(e){
        console.log(e)
    },
    chooseImage: function (e) {
        var that = this;
        wx.chooseImage({
            count: 1,
            sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
            sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
            success: function (res) {
                // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
                that.setData({
                    files: res.tempFilePaths,
                    avatar: res.tempFilePaths[0]
                });
                console.log(res.tempFilePaths[0])

            }
        })
    },
    formSubmit: function (e) {
        var that = this
        var userinfo = e.detail.value
        wx.showLoading({
            title: '正在保存',
            mask: true
        })
        if(userinfo.telephone || userinfo.qq || userinfo.wechat){
            app.globalData.phone = true
        }else{
            app.globalData.phone = false
        }
        
        if (that.data.files.length != undefined){
            wx.uploadFile({
                url: app.buildUrl("/userinfo/changeUser/"),
                header: app.getRequestHeader(),
                filePath: that.data.avatar,
                name: 'images',
                formData: {
                    username: userinfo.username,
                    sex: userinfo.sex,
                    telephone: userinfo.telephone,
                    qq: userinfo.qq,
                    wechat: userinfo.wechat,
                    email: userinfo.email
                },
                success(res) {
                    wx.hideLoading()
                    var resp = JSON.parse(res.data)
                    
                    if (resp.code == 200) {
                        app.setCache('user', resp.data)
                        wx.showToast({
                            title: '保存成功',
                            icon: 'success',
                            duration: 1000
                        })
                        return
                    }else if(resp.code == 405){
                        app.alert({ 'content': resp.msg });
                        return;
                    } 
                    
                    wx.showToast({
                        title: '保存失败',
                        icon: 'none',
                        duration: 1000
                    })
                }
            })
            return
        }
        
        wx.request({
            url: app.buildUrl("/userinfo/changeUser/"),
            method: "POST",
            header: app.getRequestHeader(),
            data: {
                username: userinfo.username,
                sex: userinfo.sex,
                telephone: userinfo.telephone,
                qq: userinfo.qq,
                wechat: userinfo.wechat,
                email: userinfo.email
            },
            success(res) {
                wx.hideLoading()
                
                if (res.data.code == 200) {
                    app.setCache('user', res.data.data)
                    wx.showToast({
                        title: '保存成功',
                        icon: 'success',
                        duration: 1000
                    })
                    
                    return
                } else if (res.data.code == 405) {
                    app.alert({ 'content': res.data.msg });
                    return;
                } 
                wx.showToast({
                    title: '保存失败',
                    icon: 'none',
                    duration: 1000
                })
            }

        })
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