import getWrapper from './utils'
import flushPromises from "flush-promises"
import "@/mock/index"
import LoginDialog from '@/components/LoginDialog'

describe('Search', () => {
    let wrapper = getWrapper.searchWrapper("", 1)

    it("search empty keyword route to home page", async () =>{
      expect(wrapper.vm.$data.keyword).toBe("")
      expect(wrapper.vm.$data.pageNum).toBe(1)
      await flushPromises()

      expect(wrapper.vm.$router.history.current.name).toBe("Home")
    })
    
    it("request search data", async () =>{
      wrapper = getWrapper.searchWrapper("你好", 1)
      
      expect(wrapper.vm.$data.keyword).toBe("你好")
      expect(wrapper.vm.$data.pageNum).toBe(1)
      await flushPromises()
      
      setTimeout(() => {
        expect(wrapper.find(".news-num").text()).toBe("为您找到相关资讯20篇")
        expect(wrapper.vm.$data.newsList.length).toBeLessThan(11)
      }, 1000)
    })

    it("display search approaches", async () =>{
      await wrapper.find(".search-tool").trigger("click")
      
      expect(wrapper.vm.$data.curTop).toBe(1)
    })

    it("click date selector", async () =>{
      await wrapper.find(".el-dropdown").trigger("click")
      await wrapper.findAll(".search-dropdown-item").at(1).trigger("click")
      
      expect(wrapper.vm.activeName_2()).toBe("一天内")
      await wrapper.findAll(".search-dropdown-item").at(2).trigger("click")
      
      expect(wrapper.vm.activeName_2()).toBe("一周内")
      await wrapper.findAll(".search-dropdown-item").at(3).trigger("click")
      
      expect(wrapper.vm.activeName_2()).toBe("一月内")
      await wrapper.findAll(".search-dropdown-item").at(4).trigger("click")
      
      expect(wrapper.vm.activeName_2()).toBe("一年内")
    })

    it("remove search approaches", async () =>{
      await wrapper.find(".search-tool").trigger("click")
      
      expect(wrapper.vm.$data.curTop).toBe(0)
      expect(wrapper.vm.$data.activeValue_0).toBe("relativity")
      expect(wrapper.vm.$data.activeValue_1).toStrictEqual([])
      expect(wrapper.vm.$data.activeIndex_2).toBe(0)
    })

    it("display news number", async () =>{
      await wrapper.setData({
        newsNum: 999
      })
      expect(wrapper.find(".news-num").text()).toBe("为您找到相关资讯999篇")
      
      await wrapper.setData({
        newsNum: 2134
      })
      expect(wrapper.find(".news-num").text()).toBe("为您找到相关资讯约2,000篇")
    })

    it("change current page", async () =>{
      await wrapper.findAll("li.number").at(1).trigger("click")
      
      expect(wrapper.vm.$router.history.current.query).toStrictEqual({
        kd: "你好",
        pn: 2
      })
    })

    it("login success", () =>{
      wrapper.findComponent(LoginDialog).vm.$emit("success")
      expect(wrapper.findComponent(LoginDialog).vm.$props.dialogVisible).toBe(false)
    })
  })
  