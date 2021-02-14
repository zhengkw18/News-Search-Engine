import getWrapper from './utils'
import User from '@/views/User'
import UserPassword from "@/components/UserPassword"

describe('User', () => {
    let wrapper = getWrapper.wrapper(User)

    it("active font color", async () =>{
      await wrapper.setData({
          activeIndex: 2
      })

      expect(wrapper.findAll(".user-function-item").at(0).element.style["color"] == "black").toBe(true)
      expect(wrapper.findAll(".user-function-item").at(2).element.style["color"] == "black").toBe(false)
    })

    it("active font color", () =>{
      wrapper.findComponent(UserPassword).vm.$emit("success", "修改密码成功！")

      expect(document.body.innerHTML).toContain("修改密码成功！")
      expect(wrapper.vm.$data.activeIndex).toBe(0)
    })
  })
  