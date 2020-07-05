// pages/report/index.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        content: '',
        contentCount: 0
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },
    chooseImage: function (e) {
        var that = this;
        wx.chooseImage({
            sizeType: ['original', 'compressed'], 
            sourceType: ['album', 'camera'],
            success: function (res) {
               
                that.setData({
                    files: that.data.files.concat(res.tempFilePaths)
                });
                console.log(that.data.files)

            }
        })
    },

    previewImage: function (e) {
        wx.previewImage({
            current: e.currentTarget.id, 
            urls: this.data.files 
        })
    },

    // 获得正文内容
    handleContentInput(e) {
        const value = e.detail.value
        console.log(value)
        this.setData({
            content: value,
            contentCount: value.length
        })

    },

    // 上传文件
    submitForm: function (e) {
        var content = this.data.content
        var articleId = this.data.articleId
        var files = this.data.files
        console.log(content)
        console.log(files, "*****")
        if (!content && files.length == 0) {
            wx.showToast({
                title: '请输入评论内容或图片',
                icon: "none",
                duration: 1500
            })
            return
        }
        wx.showLoading({
            title: '正在上传',
            mask: true
        })
        const arr = []
        for (let path of files) {
            arr.push(wxUploadFile({
                url: app.buildUrl('/upload/'),
                filePath: path,
                name: 'file',
            }))
        }

        Promise.all(arr).then(res => {
            return res.map(item => JSON.parse(item.data).data)
        }).catch(err => {
            console.log("upload images error:", err)
        }).then(urls => {

            if (app.getCache("user").nid) {
                wx.request({
                    url: app.buildUrl('/comment/'),
                    header: app.getRequestHeader(),
                    method: 'POST',
                    data: {
                        article_id: articleId,
                        content: content,
                        images: urls
                    },
                    success: function (res) {
                        if (res.data.code != 200) {
                            app.alert({ 'content': '发布内容失败了，请重新尝试。' });

                            return;
                        }
                        wx.showToast({
                            title: res.data.msg,
                            icon: 'success',
                            duration: 3000
                        })

                        wx.redirectTo({
                            url: '../detail/detail?id=' + articleId,
                        })

                    }
                })
            }


        })
    },

    onRemove: function (e) {
        var index = e.target.dataset.index
        var files = this.data.files
        files.splice(index, 1)
        this.setData({
            files: files
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