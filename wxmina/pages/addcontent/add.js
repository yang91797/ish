// pages/addcontent/add.js
import {promisify} from '../../utils/promise'
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
        titleCount: 0,
        contentCount: 0,
        title: '',
        content: '',
        images: [],
        arr: [
            {nid: 2, title: "生活"},
            {nid: 3, title: "二手"},
            {nid: 4, title: "资料"}
        ],
        topic: [
            { nid: 2, title: "生活" },
            { nid: 3, title: "二手" },
            { nid: 4, title: "资料" }
        ],
        category: 2,
        nid: 0,
        gold: 0
    
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        app.getUserInfo()
        $init(this)
       
    },
    bindPickerChange: function (e) {
        
        var topic = this.data.topic
        for (let i = 0;i < topic.length;i++){
            
            if (topic[i]['title'] == this.data.arr[e.detail.value]){
               
                this.setData({
                    nid: e.detail.value,
                    category: topic[i]['nid']
                })
            }
            
        }
        
    },
    radioChange: function(e){
        this.setData({
            nid: e.detail.value,
            category: e.detail.value
            
        })
    },

    // 获得学习资料链接
    study_url: function(e){
        this.setData({
            study_url: e.detail.value
        })
    },

    //获得输入的金币数量
    gold:function(e){
        this.setData({
            gold: e.detail.value
        })
    },

    // 获得标题输入内容
    handleTitleInput(e) {
        const value = e.detail.value
        this.data.title = value
        this.data.titleCount = value.length
        $digest(this)

    },

    // 获得正文内容
    handleContentInput(e){
        const value = e.detail.value
        this.data.content = value
        this.data.contentCount = value.length
        $digest(this)
    },

    submitForm(e){
        var that = this
        const title = this.data.title
        const content = this.data.content
        const category = this.data.category
        const study_url = this.data.study_url
        const gold = this.data.gold
        const images = this.data.images
        var formId = e.detail.formId
        var date = new Date().getTime()
        console.log(category, study_url, gold)
        if (category == 4 && (!study_url || !gold)){
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
                    url: app.buildUrl('/upload/'),
                    filePath: path,
                    name: 'file',
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
                        url: app.buildUrl('/create/'),
                        header: app.getRequestHeader(),
                        method: 'POST',
                        data:{
                            title: title,
                            content: content,
                            images: urls,
                            type: 'text',
                            category: category,
                            study_url: study_url,
                            gold: gold,
                            formId: formId,
                            expire: date + 60480000
                        },
                        success:function(res){
                            if (res.data.code != 200){
                                app.alert({ 'content': '发布内容失败了，请重新尝试。' });
                                wx.hideLoading()
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

                            wx.switchTab({
                                url: '/pages/top/top',
                            })
                            return
                        }
                    })
                }


            })
        }
    },

    addImage:function(e){ 
        this.setData({
            images: e.detail
        })  
        
    },

    delImage:function(e){
        this.setData({
            images: e.detail
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