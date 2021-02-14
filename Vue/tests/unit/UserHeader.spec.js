import getWrapper from './utils'
import "@/mock/index"
import UserHeader from '@/components/UserHeader'
import cookie from "@/utils/cookie"

describe('UserHeader', () => {
    let wrapper = getWrapper.wrapper(UserHeader)
    
    it("logout", async () =>{
        cookie.add_cookie("username", "admin", 24)
        cookie.add_cookie("password", "admin", 24)
  
        expect(cookie.get_cookie("username")).toBe("admin")
        expect(cookie.get_cookie("password")).toBe("admin")
  
        await wrapper.find(".el-dropdown").trigger("hover")
        await wrapper.findAll(".user-dropdown-item").at(0).trigger("click")
  
        expect(cookie.get_cookie("username")).toBe("")
        expect(cookie.get_cookie("password")).toBe("")
        expect(wrapper.vm.$router.history.current.name).toBe("Home")
      })
  })
  