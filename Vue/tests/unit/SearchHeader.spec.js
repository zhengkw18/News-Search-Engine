import getWrapper from './utils'
import "@/mock/index"
import SearchHeader from '@/components/SearchHeader'
import cookie from "@/utils/cookie"

describe('SearchHeader', () => {
    let wrapper = getWrapper.wrapper(SearchHeader)
    it("default value of props", () =>{
      expect(wrapper.vm.$props.name).toBe("首页")
      expect(wrapper.vm.$props.path).toBe("Home")
      expect(wrapper.vm.$props.keyword).toBe("")
    })

    it("login", async () =>{
      await wrapper.find(".login-button").trigger("click")
      expect(Object.prototype.hasOwnProperty.call(wrapper.emitted(), "login")).toBe(true)
    })

    it("logout", async () =>{
      cookie.add_cookie("username", "admin", 24)
      cookie.add_cookie("password", "admin", 24)

      expect(cookie.get_cookie("username")).toBe("admin")
      expect(cookie.get_cookie("password")).toBe("admin")

      await wrapper.find(".el-dropdown").trigger("hover")
      await wrapper.findAll(".user-dropdown-item").at(1).trigger("click")

      expect(cookie.get_cookie("username")).toBe("")
      expect(cookie.get_cookie("password")).toBe("")
    })

    it("click icon jump home page", async () =>{
      await wrapper.find(".search-img").trigger("click")

      expect(wrapper.vm.$router.history.current.name).toBe("Home")
    })

    it("jump home page", async () =>{
      await wrapper.findAll("p.header-hover").at(1).trigger("click")

      expect(wrapper.vm.$router.history.current.name).toBe("Home")
    })
  })
  