import getWrapper from './utils'
import AuthCode from '@/components/AuthCode'

describe('AuthCode', () => {
    let wrapper = getWrapper.wrapper(AuthCode)

    it("check code success", async () => { 
        await wrapper.setData({
          check: wrapper.vm.$data.identifyCode
        })
    
        expect(Object.prototype.hasOwnProperty.call(wrapper.emitted(), "success")).toBe(true)
      })

    it("check code fail", async () => { 
        await wrapper.setData({
          check: wrapper.vm.$data.identifyCode + "1"
        })
    
        expect(wrapper.vm.$data.isError).toBe(true)
      })

    it("close dialog", async () => {
      await wrapper.find('.el-dialog__headerbtn').trigger('click')
      
      expect(Object.prototype.hasOwnProperty.call(wrapper.emitted(), "hide")).toBe(true)
    })
})