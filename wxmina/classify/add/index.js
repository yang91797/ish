// classify/add/index.js
import { promisify } from '../../utils/promise'
import {
    $init,
    $digest
} from '../../utils/common'

const wxUploadFile = promisify(wx.uploadFile)
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        category: 3,
        titleCount: 0,
        contentCount: 0,
        title: '',
        content: '',
        images: [],
        index:0,
        array: ["大学数学", "大学外语", "大学物理", "大学化学", "大学生物", "大学地理", "思想政治","统计", "信息技术", "工学", "建筑", "经济学", "管理学", "法学", "文学", "考证", "考研", "安装包", "其他"]
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        
        this.setData({
            category:options.category
        })
        
    },
    bindPickerChange: function (e) {
        
        this.setData({
            index: e.detail.value
        })
    },
   
    // 获得学习资料链接
    study_url: function (e) {
        this.setData({
            study_url: e.detail.value
        })
    },

    //获得输入的金币数量
    gold: function (e) {
        this.setData({
            gold: e.detail.value
        })
    },

    // 获得标题输入内容
    handleTitleInput(e) {
        const value = e.detail.value
       
        this.setData({
            title: value,
            titleCount: value.length
        })

    },

    // 获得正文内容
    handleContentInput(e) {
        const value = e.detail.value
        this.setData({
            content: value,
            contentCount: value.length,

        })
    },

    addImage: function (e) {
        this.setData({
            images: e.detail
        })

    },

    delImage: function (e) {
        this.setData({
            images: e.detail
        })
    },

    submitForm(e) {
        if (!app.globalData.phone) {
            wx.showToast({
                title: '请至少填写一种联系方式',
                icon: "none",
                duration: 3000
            })
            wx.navigateTo({
                url: '../../pages/changeUser/index',
            })
            
            return
        }
        var that = this
        const title = this.data.title
        const content = this.data.content
        const category = this.data.category
        const study_url = this.data.study_url
        const gold = this.data.gold
        const images = this.data.images
        const subject = this.data.array[this.data.index]
        var formId = e.detail.formId
        

        if (category == 4 && (!study_url || !gold)) {
            wx.showToast({
                title: '请正确输入',
                icon: 'none',
                duration: 1000
            })
            return
        }
        if (title || content || images.length != 0) {
            const arr = []
            for (let path of images) {
                arr.push(wxUploadFile({
                    url: app.buildUrl('/create/upload/'),
                    filePath: path,
                    name: 'images',
                }))

            }

            wx.showLoading({
                title: '正在上传',
                mask: true
            })

            Promise.all(arr).then(res => {
                return res.map(item => JSON.parse(item.data).data)
            }).catch(err => {
                console.log("upload images error:", err)
            }).then(urls => {
                if (app.getCache("user").nid) {
                    wx.request({
                        url: app.buildUrl('/create/add/'),
                        header: app.getRequestHeader(),
                        method: 'POST',
                        data: {
                            title: title,
                            content: content,
                            images: urls,
                            type: 'text',
                            category: category,
                            study_url: study_url,
                            gold: gold,
                            subject: subject,
                            formId: formId,
                        },
                        success: function (res) {
                            
                            if (res.data.code == 405){
                                app.alert({ 'content': res.data.msg });
                                return;
                            } else if (res.data.code != 200){
                                app.alert({ 'content': '发布内容失败了，请重新尝试。' });
                                return;
                            }
                           
                            that.setData({
                                title: '',
                                content: '',
                                images: [],
                                nid: 0,
                                gold: 0
                            })
                            wx.showToast({
                                title: res.data.msg,
                                icon: 'success',
                                duration: 3000
                            })
                            var category = that.data.category
                            if(category == 3){
                                wx.redirectTo({
                                    url: '/classify/second/index',
                                })
                            }else if (category == 4){
                                wx.redirectTo({
                                    url: '/classify/learn/index',
                                })
                            }else if (category == 2){
                                wx.redirectTo({
                                    url: '/classify/rent/index',
                                })
                            }
                            return
                        },
                        complete(res){
                            wx.hideLoading()
                        }
                    })
                }


            })
        }
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