import getWrapper from './utils'
import flushPromises from "flush-promises"
import "@/mock/index"
import LoginDialog from '@/components/LoginDialog'

describe('Home', () => {
    let wrapper = getWrapper.homeWrapper("all")

    it("empty channel route to all channel", async () =>{
      expect(wrapper.vm.$data.activeName).toBe("all")
      await flushPromises()

      expect(wrapper.vm.$router.history.current.query).toStrictEqual({
        chnl: "all"
      })
    })
    
    it("click route to specific channel", async () =>{
      await wrapper.findAll(".el-tabs__item").at(1).trigger("click")
      await flushPromises()

      expect(wrapper.vm.$router.history.current.query.chnl == "all").toBe(false)
    })

    it("login success", () =>{
      wrapper.findComponent(LoginDialog).vm.$emit("success")
      expect(wrapper.findComponent(LoginDialog).vm.$props.dialogVisible).toBe(false)
    })
  })
  