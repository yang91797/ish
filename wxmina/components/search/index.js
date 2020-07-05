// components/search/index.js
const app = getApp()
var searchTitle = ""; // 搜索关键字
Component({
    /**
     * 组件的属性列表
     */
    properties: {

    },

    /**
     * 组件的初始数据
     */
    data: {
        hidden: true,
        inputShowed: true,
        inputVal: "",
        searchLogShowed: false,
        // searchshow: true,
        scrollTop: 100,
        searchLogList: []
        
    },

    /**
     * 组件的方法列表
     */
    methods: {
        // 输入内容时 把当前内容赋值给 查询的关键字，并显示搜索记录
        inputTyping: function (e) {
            var that = this;

            // 如果不做这个if判断，会导致 searchLogList 的数据类型由 list 变为 字符串
            if ("" != wx.getStorageSync('searchLog')) {
                that.setData({
                    inputVal: e.detail.value,
                    searchLogList: wx.getStorageSync('searchLog')
                });
            } else {
                that.setData({
                    inputVal: e.detail.value,
                    searchLogShowed: true
                });
            }
            searchTitle = e.detail.value;
            
        },
        
        // 点击叉叉icon 清除输入内容，同时清空关键字，并加载数据——没有关键字，就是加载所有数据。
        clearInput: function () {
            var that = this;
            that.setData({
                msgList: [],
                scrollTop: 0,
                inputVal: ""
            });
            searchTitle = "";

            that.triggerEvent("searchShow", false)
            that.triggerEvent('searchData', false)
            // that.loadMsgData(1);
        },

        // 通过搜索记录查询数据
        searchDataByLog: function (e) {
            // 从view中获取值，在view标签中定义data-name(name自定义，比如view中是data-log="123" ; 那么e.target.dataset.log=123)
            searchTitle = e.target.dataset.log;
            var that = this;
            that.setData({
                msgList: [],
                scrollTop: 0,
                searchLogShowed: false,
                inputVal: searchTitle
            });
            // pageNum = 1;
            that.loadMsgData();
        },

        // 清除搜索记录
        clearSearchLog: function () {
            var that = this;
            that.setData({
                hidden: false
            });
            wx.removeStorageSync("searchLog");
            that.setData({
                scrollTop: 0,
                searchLogShowed: false,
                hidden: true,
                searchLogList: []
            });
        },

        // 定位数据
        scroll: function (event) {
            var that = this;
            that.setData({
                scrollTop: event.detail.scrollTop
            });
        },

        // 显示搜索历史记录
        searchLogShowed: function () {
            var that = this;
            
            if ("" != wx.getStorageSync('searchLog')) {
                that.setData({
                    searchLogShowed: true,
                    searchLogList: wx.getStorageSync('searchLog')
                });
            } else {
                that.setData({
                    searchLogShowed: true
                });
            }
            
        },

        // 点击 搜索 按钮后 隐藏搜索记录，并加载数据
        searchData: function (e) {
            if (!app.getUserInfo()) {
                return
            }
            var that = this;
            that.setData({
                msgList: [],
                scrollTop: 0,
                searchLogShowed: false,
                formId: e.detail.formId,
            });
            // pageNum = 1;
            that.loadMsgData();
            // 搜索后将搜索记录缓存到本地
            if ("" != searchTitle) {
                var searchLogData = that.data.searchLogList;
                for(let i=0;i<searchLogData.length;i++){
                    if (searchTitle==searchLogData[i]){
                        searchLogData.splice(i,1)
                    }
                }

                searchLogData.unshift(searchTitle);
                
                wx.setStorageSync('searchLog', searchLogData);
            }
        },

        loadMsgData:function(e){
            var that = this
           
            // 显示加载的icon
            that.setData({
                hidden: false
            });
            wx.request({
                url: app.buildUrl('/search/'),
                method: "POST",
                header: app.getRequestHeader(),
                data:{
                    searchTitle:searchTitle,
                    formId: that.data.formId,
                },
                success:function(res){
                   
                    var resp = res.data
                    if (resp.code == 200){
                        that.setData({
                            hidden: true
                        });

                        that.triggerEvent("searchShow", true)
                        if(resp.data.length > 0){
                            that.triggerEvent('searchData', resp.data)
                        }else{
                            that.triggerEvent('searchData', false)
                        }                        
                        
                    }
                    
                }
                
            })

        },
        hideRecord:function(){
            if (searchTitle.length == 0){
                this.clearInput()
            }
            this.setData({
                searchLogShowed:false
            })
        }

    }
})
