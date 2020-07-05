// components/comment/index.js
const app = getApp()
var util = require('../../utils/util.js');
const wxparse = require('../../wxParse/wxParse.js');

Component({
    pageLifetimes: {
        show() {
            
            // 页面被展示
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
        },
        hide() {
            // 页面被隐藏
        },
        resize(size) {
            // 页面尺寸变化
        }
    },
    /**
     * 组件的属性列表
     */
    properties: {
        article_id:{
            type: Number,
            observer: function(news, olds, path){
                
            }
        },
        comment:{
            type: Array,
            value: [],
            observer: function(news){
               
                this.comment_wxparse(news, "commentTemArray")
            }
        },
       
    },

    /**
     * 组件的初始数据
     */
    data: {
        releaseValue: '',
        reply_list: [],
        commentImage: [],
        files: [],
        reveal: true,
        focus: false,
        commentId: '',
        ancestor: null,
        commentUserId: null,
        replyvie: false,
        emojis: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134"]
    },

    /**
     * 组件的方法列表
     */
    methods: {
        


        // 表情选择
        emojiChoose: function (e) {
            // 当前输入内容和表情合并

            this.setData({
                releaseValue: this.data.releaseValue + "[" + e.currentTarget.dataset.oxf + "]"
            })
        },

        //点击emoji背景遮罩隐藏emoji盒子
        cemojiCfBg: function () {
            this.setData({
                isShow: false,
                cfBg: false
            })
        },

        onReplyBlur: function (e) {
            this.setData({
                releaseValue: e.detail.value,
            })
        },

        textAreaBlur: function (e) {
            this.setData({
                releaseValue: e.detail.value
            })
        },

        textAreaFocus: function () {
            this.setData({
                isShow: false,
                cfBg: false,
            })
        },

        //点击表情显示隐藏表情盒子
        emojiShowHide: function () {
            this.setData({
                isShow: !this.data.isShow,
                isLoad: false,
                cfBg: !this.data.false
            })
        },

        // 评论图片
        chooseImage: function (e) {
            var that = this;
            wx.chooseImage({
                sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
                sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
                success: function (res) {
                    // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
                    
                    that.triggerEvent('reimage', that.data.files.concat(res.tempFilePaths))
                }
            })
        },
        // 发送评论到后台
        formSubmit(e) {
            if (!app.getUserInfo()) {
                return
            }
            var that = this
            var input = e.detail.value.input
            var formId = e.detail.formId
            
            wx.showLoading({
                title: '加载中',
                mask: true
            })
            if (input.slice(0, 3) == "回复 ") {
                let ind = input.indexOf(":")
                input = input.slice(ind + 1)

                if (input == '' || input == ' ') {
                    wx.showToast({
                        title: '评论内容不能为空',
                        icon: 'none'
                    })
                    return false
                }

                wx.request({
                    url: app.buildUrl('/create/comment/'),
                    header: app.getRequestHeader(),
                    method: 'POST',
                    data: {
                        type: 'reply',
                        content: input,
                        article_id: that.data.article_id,
                        comment_id: that.data.commentId,
                        ancestor: that.data.ancestor,
                        commentUserId: that.data.commentUserId,
                        formId: formId,
                
                    },
                    success: function (res) {
                        var code = res.data.code

                        if (code == 200) {
                            // comment_list
                            that.setData({
                                // comment: that.data.comment.concat(comment_list),
                                releaseValue: '',
                                releaseFocus: true,
                                isShow: false,
                                cfBg: false,
                                reveal: false
                            })
                            // that.onLoad({ id: that.data.article_id })
                            that.triggerEvent('onLoad', that.data.article_id)
                        }else if(code == 405){
                            app.alert({ 'content': res.data.msg });
                            return;
                        }

                    },
                    complete: function(){
                        wx.hideLoading()
                    }
                })
                return

            }
            if (input == '' || input == ' ') {
                wx.showToast({
                    title: '评论内容不能为空',
                    icon: 'none'
                })
                return false
            }

            var list = this.data.comment;
        
            // var comment = "<p>" + e.detail.value.input + "</p >"
            wx.request({
                url: app.buildUrl('/create/comment/'),
                header: app.getRequestHeader(),
                method: 'POST',
                data: {
                    content: input,
                    article_id: that.data.article_id,
                    commentUserId: that.data.commentUserId,
                    formId: formId,
                },
                success: function (res) {
                    var code = res.data.code

                    if (code == 200) {
                        // comment_list
                        that.setData({
                            // comment: that.data.comment.concat(comment_list),
                            releaseValue: '',
                            releaseFocus: true,
                            isShow: false,
                            cfBg: false,
                            reveal: false
                        })
                        that.triggerEvent('onLoad', that.data.article_id)
                    }else if(code == 405){
                        app.alert({ 'content': res.data.msg });
                        return;
                    }

                },
                complete: function () {
                    wx.hideLoading()
                }
            })
        },

        changeinputVal(e) {

            this.setData({
                releaseValue: e.detail.value
            })
        },
        copy: function(e){
            console.log(e)
            var that = this
            var commentId = e.currentTarget.dataset.commentid
            var ancestor = e.currentTarget.dataset.ancestor
            if (!ancestor){
                var comment = that.data.comment

            }else{
                var comment = that.data.reply_list
                
            }
            for(let i = 0;i < comment.length; i++){
                
                if(comment[i].nid == commentId){
                    wx.setClipboardData({
                        data: comment[i].content,
                        success(res) {
                            wx.showToast({
                                title: '已复制到剪贴板',
                                icon: 'none',
                                duration: 2000
                            })
                        }
                    })
                }
            }
        },
        onReplyBlur: function (e) {
            this.setData({
                releaseValue: e.detail.value,
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

        // 查看子评论
        seeReply: function (e) {
            var that = this
            var comm_id = e.currentTarget.dataset.id
            var reId = e.currentTarget.dataset.reid
            wx.request({
                url: app.buildUrl('/details/'),
                header: app.getRequestHeader(),
                method: 'POST',
                data: {
                    cid: comm_id
                },
                success: function (res) {
                    let index = 0
                    var data = res.data.data
                    var comment = that.data.comment
                    for (let item of comment) {
                        if (item.nid == comm_id) {
                            if (comment[index].isShow == "" || comment[index].isShow == undefined) {
                                comment[index].isShow = "true"
                            } else {
                                comment[index].isShow = ""
                            }
                        } else {
                            comment[index].isShow = ""
                        }
                        index++
                    }
                    
                    that.comment_wxparse(data, "replyTemArray")
                    that.setData({
                        reply_list: data,
                        reveal: true,
                        comment: comment,
                        replyvie: true
                    })
                }

            })
        },

        reply: function (e) {
            console.log(e)
            let msg = e.currentTarget.dataset
            var content = "回复 " + msg.username + ": "
            var ancestor = msg.ancestor
            var commentUserId = msg.userid
            
            if (ancestor == undefined) {
                ancestor = msg.commentid
            }
            this.setData({
                releaseValue: content,
                focus: true,
                commentId: msg.commentid,
                ancestor: ancestor,
                commentUserId: commentUserId
            })
        },
        userinfo: function (e) {
            
            wx.navigateTo({
                url: '../viewuser/index?id=' + e.currentTarget.dataset.id,
            })
        },

        // 查看大图
        lookImage:function(e){
        
            var comment = this.data.comment
            var commentIndex = e.currentTarget.dataset.commentindex
            var imageIndex = e.currentTarget.dataset.id
            
            wx.previewImage({
                current: this.data.comment[commentIndex].commentImage[imageIndex], // 当前显示图片的http链接
                urls: this.data.comment[commentIndex].commentImage // 需要预览的图片http链接列表
            })
        }

    }
})
