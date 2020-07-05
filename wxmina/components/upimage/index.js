// components/upimg/index.js

import { promisify } from '../../utils/promise'
import {
    $init,
    $digest
} from '../../utils/common'

const wxUploadFile = promisify(wx.uploadFile)
const app = getApp()

Component({
    externalClasses: ["img-plus"],
    /**
     * 组件的属性列表
     */
    properties: {
        
    },

    /**
     * 组件的初始数据
     */
    data: {
        titleCount: 0,
        contentCount: 0,
        title: '',
        content: '',
        images: []
    },

    /**
     * 组件的方法列表
     */
    methods: {
        
        handleTitleInput(e) {
            
            const value = e.detail.value
            this.data.title = value
            this.data.titleCount = value.length
            $digest(this)
            
        },

        handleContentInput(e) {
            const value = e.detail.value
            this.data.content = value
            this.data.contentCount = value.length
            $digest(this)
            
        },

        // 选择图片
        chooseImage(e) {
            $init(this)
            
            wx.chooseImage({
                count: 6,
                sizeType: ['original', 'compressed'],
                sourceType: ['album', 'camera'],
                success: res => {
                   
                    const images = this.data.images.concat(res.tempFilePaths)
                    
                    this.data.images = images.length <= 6 ? images : images.slice(0, 6)
                    $digest(this)
                    this.triggerEvent('addImage', this.data.images)
                }
            })
        },

        // 删除选择的图片
        removeImage(e) {
            const idx = e.target.dataset.idx
            this.data.images.splice(idx, 1)
            $digest(this)
            this.triggerEvent('delImage', this.data.images)
        },

        handleImagePreview(e) {
            const idx = e.target.dataset.idx
            const images = this.data.images

            wx.previewImage({
                current: images[idx],
                urls: images,
            })
        },

      
    }
})
