// classify/search/index.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        show: false,
        noSearch: false,
        search_list: [],
        searchLogList: [],
        formId: "",
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        this.setData({
            formId: options.formId
        })
        this.getSearchData()
    },
    getSearchData:function(){
        var that = this;
        wx.request({
            url: app.buildUrl('/search/'),
            method: "POST",
            header: app.getRequestHeader(),
            data: {
                searchTitle: searchTitle,
                formId: that.data.formId
            },
            success: function (res) {
                var resp = res.data
                if (resp.code == 200) {
                    console.log(resp)

                }

            }

        })

    },
    listenerSearchInput: function (e) {
        this.setData({
            searchInput: e.detail.value
        });

    },
    searchData: function (e) {

        if (!e.detail) {
            this.setData({
                noSearch: true,
                search_list: e.detail
            })
            return
        }
        this.setData({
            search_list: e.detail
        })
    },
    searchShow: function (e) {

        if (e.detail) {
            var noSearch = false

        } else {
            var noSearch = true
        }
        this.setData({
            show: e.detail,
            noSearch: noSearch
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