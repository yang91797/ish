// components/reImage/index.js
const app = getApp()
import { promisify } from '../../utils/promise'
const wxUploadFile = promisify(wx.uploadFile)

Component({
    /**
     * 组件的属性列表
     */
    properties: {
        files:{
            type: Array,
            value: [],
            observer: function(newVal, oldVal){
                
            }
        },
        articleId:{
            type: String
        }
    },

    /**
     * 组件的初始数据
     */
    data: {
        contentCount: 0,
        content: null,
    },

    /**
     * 组件的方法列表
     */
    methods: {
        chooseImage: function (e) {
            var that = this;
            wx.chooseImage({
                sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
                sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
                success: function (res) {
                    // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
                    that.setData({
                        files: that.data.files.concat(res.tempFilePaths)
                    });
                    console.log(that.data.files)
                    
                }
            })
        },

        previewImage: function (e) {
            wx.previewImage({
                current: e.currentTarget.id, // 当前显示图片的http链接
                urls: this.data.files // 需要预览的图片http链接列表
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
        submitForm:function(e){
            if (!app.getUserInfo()) {
                return
            }
            var content = this.data.content
            var articleId = this.data.articleId
            var files = this.data.files
            var formId = e.detail.formId
            var that = this
            if(!content && files.length == 0){
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
            for (let path of files){
                arr.push(wxUploadFile({
                    url: app.buildUrl('/create/upload/'),
                    filePath: path,
                    name: 'images',
                }))
            }
            
            Promise.all(arr).then(res => {
                return res.map(item => JSON.parse(item.data).data)
            }).catch(err => {
                console.log("upload images error:", err)
            }).then(urls => {

                if (app.getCache("user").nid) {
                    wx.request({
                        url: app.buildUrl('/create/comment/'),
                        header: app.getRequestHeader(),
                        method: 'POST',
                        data: {
                            article_id: articleId,
                            content: content,
                            images: urls,
                            formId: formId
                        },
                        success: function (res) {
                            if (res.data.code == 405) {
                                app.alert({ 'content': res.data.msg });
                                return;
                            }else if(res.data.code != 200){
                                app.alert({ 'content': '发布内容失败了，请重新尝试。' });
                                return;
                            }
                            wx.showToast({
                                title: res.data.msg,
                                icon: 'success',
                                duration: 3000
                            })

                            that.triggerEvent('close', false)
                            
                        },
                        complete:function(){
                            wx.hideLoading()
                        }
                    })
                }


            })
        },

        onRemove: function(e){
            var index = e.target.dataset.index
            var files = this.data.files
            files.splice(index, 1)
            this.setData({
                files: files
            })
        },
 
    }
})
