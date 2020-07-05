// classify/learnList/index.js

const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    article_list: Array,
    history: [],
      yesSrc: '/images/nav/resizeAf.png',
      noSrc: '/images/nav/resizeBe.png',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
   
    var that = this
      if (wx.getStorageSync("history") != "") {
          
          this.setData({
              history: wx.getStorageSync("history")
          })
      }
      this.studyClass(options)
   
  },

  studyClass:function(options){
      var that = this
      wx.request({
          url: app.buildUrl("/home/studyclass"),
          method: "POST",
          header: app.getRequestHeader(),
          data: {
              id: options.id
          },
          success: function (res) {
              var resp = res.data
              that.setData({
                  article_list: resp.data
              })
          }
      })
  },
    // 查看文章詳情
    seeDetail: function (e) {
        var that = this
        let history = that.data.history
        let article = that.data.article_list[e.currentTarget.dataset.index]
        var formId = e.detail.formId
        var date = new Date().getTime()
        wx.request({
            url: app.buildUrl('/saveFormId/'),
            method: "POST",
            header: app.getRequestHeader(),
            data: ({
                formId: formId,
                expire: date + 60480000
            }),
            success: function (res) {

            }
        })
        that.setData({
            leassonId: e.currentTarget.dataset.id,
        })
        for (let i = 0; i < history.length; i++) {

            if (history[i].nid == article.nid) {
                history.splice(i, 1)
            }
        }

        var re = history.unshift(article)

        if (history.length >= 30) {
            history.pop()

        }

        // 设置浏览缓存
        wx.setStorage({
            key: 'history',
            data: history
        })

        wx.navigateTo({
            url: '../../detail/learn/index?id=' + e.currentTarget.dataset.id,
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