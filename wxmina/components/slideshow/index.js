// components/slideshow/index.js
Component({
    /**
     * 组件的属性列表
     */
    externalClasses: ['shopping', 'shopp-image'],
    properties: {
        banners:{
            type: Array,
            value: [],
            observer: function (news, olds, path) {
                
                if(news.length > 0 && !news[0]['pic_url']){
                    var ima = []
                    for(let i = 0;i < news.length; i++){
                        let dic = {"pic_url": news[i]}
                        ima.push(dic)
                    }
                    this.setData({
                        banners: ima,
                        images_list: news
                    })
                }else{
                    let img = []
                    for(let i = 0;i < news.length;i++){
                        img.push(news[i]['pic_url'])
                        
                    }
                    this.setData({
                        images_list: img
                    })
                }
            }
        },
        images_list:{
            type: Array,
            value: []
        }
    },

    /**
     * 组件的初始数据
     */
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        images_list: [],
    },

    /**
     * 组件的方法列表
     */
    methods: {
        swiperchange: function (e) {
            this.setData({
                swiperCurrent: e.detail.current
            })
        },

        tapBanner:function(e){
            console.log(e)
            var data = {
                id: e.currentTarget.dataset.id,
                index: e.currentTarget.dataset.index
            }
            this.triggerEvent('myevent', data)
            // wx.navigateTo({
            //     url: '../../detail/ad_head/index?nid=' + e.currentTarget.dataset.id,
            // })
        }
    }
})
