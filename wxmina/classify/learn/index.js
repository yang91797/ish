// classify/learn/index.js

const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
      category: Array,
        other_num: 0,
      bgColors: ['#4AB2BF', '#1895C6', '#4C87E0', '#A361D9', '#F7AE6A', '#FF14A0', '#61F0E1', '#6282A7', '#27998E', '#3C74CC', '#A463DA', '#F0A257', '#DD4B7A', '#59C6BD', '#617FA1', '#1B92C3', '#30A297', '#3B73CB', '#9E57CA', '#A463DA', '#1895C6', '#A361D9', '#FF14A0'],
      
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        
        this.getCategory()
    },
    getCategory:function(){
      var that = this
      wx.request({
        url: app.buildUrl('/home/studyclass'),
        header: app.getRequestHeader(),
        success: function(res){
          var resp = res.data
          that.setData({
            category: resp.data.category,
            other_num: resp.data.other
          })

        }
      })
    },
    getData:function(e){
      wx.navigateTo({
        url: '../learnList/index?id=' + e.currentTarget.dataset.id,
      })
      
    },

    publish: function () {
        wx.navigateTo({
            url: '../add/index?category=' + 4,
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