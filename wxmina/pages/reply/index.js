// pages/reply/index.js
const app = getApp()
let wxparse = require('../../wxParse/wxParse.js');
Page({

    /**
     * 页面的初始数据
     */
    data: {
        yesSrc: '/images/nav/resizeAf.png',
        noSrc: '/images/nav/resizeBe.png',
        like: false,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        app.getUserInfo()
        wxparse.emojisInit('[]', "/wxParse/emojis/", {
            "0": "0.gif",
            "1": "1.gif",
            "2": "2.gif",
            "3": "3.gif",
            "4": "4.gif",
            "5": "5.gif",
            "6": "6.gif",
            "7": "7.gif",
            "8": "8.gif",
            "9": "9.gif",
            "10": "10.gif",
            "11": "11.gif",
            "12": "12.gif",
            "13": "13.gif",
            "14": "14.gif",
            "15": "15.gif",
            "16": "16.gif",
            "17": "17.gif",
            "18": "18.gif",
            "19": "19.gif",
            "18": "18.gif",
            "19": "19.gif",
            "20": "20.gif",
            "21": "21.gif",
            "22": "22.gif",
            "23": "23.gif",
            "24": "24.gif",
            "25": "25.gif",
            "26": "26.gif",
            "27": "27.gif",
            "28": "28.gif",
            "29": "29.gif",
            "30": "30.gif",
            "31": "31.gif",
            "32": "32.gif",
            "33": "33.gif",
            "34": "34.gif",
            "35": "35.gif",
            "36": "36.gif",
            "37": "37.gif",
            "38": "38.gif",
            "39": "39.gif",
            "40": "40.gif",
            "41": "41.gif",
            "42": "42.gif",
            "43": "43.gif",
            "44": "44.gif",
            "45": "45.gif",
            "46": "46.gif",
            "47": "47.gif",
            "48": "48.gif",
            "49": "49.gif",
            "50": "50.gif",
            "51": "51.gif",
            "52": "52.gif",
            "53": "53.gif",
            "54": "54.gif",
            "55": "55.gif",
            "56": "56.gif",
            "57": "57.gif",
            "58": "58.gif",
            "59": "59.gif",
            "60": "60.gif",
            "61": "61.gif",
            "62": "62.gif",
            "63": "63.gif",
            "64": "64.gif",
            "65": "65.gif",
            "66": "66.gif",
            "67": "67.gif",
            "68": "68.gif",
            "69": "69.gif",
            "70": "70.gif",
            "71": "71.gif",
            "72": "72.gif",
            "73": "73.gif",
            "74": "74.gif",
            "75": "75.gif",
            "76": "76.gif",
            "77": "77.gif",
            "78": "78.gif",
            "79": "79.gif",
            "80": "80.gif",
            "81": "81.gif",
            "82": "82.gif",
            "83": "83.gif",
            "84": "84.gif",
            "85": "85.gif",
            "86": "86.gif",
            "87": "87.gif",
            "88": "88.gif",
            "89": "89.gif",
            "90": "90.gif",
            "91": "91.gif",
            "92": "92.gif",
            "93": "93.gif",
            "94": "94.gif",
            "95": "95.gif",
            "96": "96.gif",
            "97": "97.gif",
            "98": "98.gif",
            "99": "99.gif",
            "100": "100.gif",
            "101": "101.gif",
            "102": "102.gif",
            "103": "103.gif",
            "104": "104.gif",
            "105": "105.gif",
            "106": "106.gif",
            "107": "107.gif",
            "108": "108.gif",
            "109": "109.gif",
            "110": "110.gif",
            "111": "111.gif",
            "112": "112.gif",
            "113": "113.gif",
            "114": "114.gif",
            "115": "115.gif",
            "116": "116.gif",
            "117": "117.gif",
            "118": "118.gif",
            "119": "119.gif",
            "120": "120.gif",
            "121": "121.gif",
            "122": "122.gif",
            "123": "123.gif",
            "124": "124.gif",
            "125": "125.gif",
            "126": "126.gif",
            "127": "127.gif",
            "128": "128.gif",
            "129": "129.gif",
            "130": "130.gif",
            "131": "131.gif",
            "132": "132.gif",
            "133": "133.gif",
            "134": "134.gif"
        })
        this.reply()
    },
    reply:function(){
        var that = this
        wx.request({
            url: app.buildUrl('/reply/'),
            header: app.getRequestHeader(),
            success:function(res){
                var user = wx.getStorageSync("user")
                that.setData({
                    userInfo: user,
                    replyList: res.data.data
                })
                that.comment_wxparse(res.data.data, "replyTemArray")
                
            }
        })
    },
    comment_wxparse: function (event, type) {

        for (let i = 0; i < event.length; i++) {
            var content = "<p>" + event[i].content + "</p >"
            wxparse.wxParse('reply' + i, 'html', event[i].content, this)

            if (i === event.length - 1) {
                wxparse.wxParseTemArray(type, 'reply', event.length, this)
            }
        }
    },
    seeDetail: function (e) {
        this.setData({
            leassonId: e.currentTarget.dataset.id
        })
        wx.navigateTo({
            url: '../detail/detail?id=' + e.currentTarget.dataset.id,
        })
    },
    del:function (e){
        var that = this
        var commentId = e.currentTarget.dataset.commid
        
        wx.showModal({
            title: '删除',
            content: '确认删除？',
            success(res){
                if (res.confirm){
                    wx.request({
                        url: app.buildUrl('/delete/'),
                        method: "POST",
                        header: app.getRequestHeader(),
                        data:{
                            commentId: commentId,
                            type: "reply"
                        },
                        success(res){
                            
                            var resp = res.data
                            if (resp.code == 200){
                                that.onLoad()
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