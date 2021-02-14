import getWrapper from './utils'
import "@/mock/index"
import SearchBar from '@/components/SearchBar'

describe('SearchBar', () => {
    let wrapper = getWrapper.wrapper(SearchBar)

    const afterSearch = (keyword) => {
      expect(wrapper.vm.$data.isFocus).toBe(false)
      expect(wrapper.vm.$router.history.current.name).toBe("Search")
      expect(wrapper.vm.$router.history.current.query.kd).toBe(keyword)
    }

    it("focus", () =>{
      wrapper.vm.$refs.search_input.focus()
      expect(wrapper.vm.$data.isFocus).toBe(true)
    })

    it("search empty keyword route to home page", async () =>{
      await wrapper.find('.el-input').trigger('keyup.enter')

      expect(wrapper.vm.$data.isFocus).toBe(false)
      expect(wrapper.vm.$router.history.current.name).toBe("Home")
    })

    it("initial props pass data", () =>{
      wrapper = getWrapper.propsWrapper(SearchBar, {
        keyword: "你好"
      })
      expect(wrapper.vm.$data.searchInput).toBe("你好")
    })

    it("search",async () =>{
      await wrapper.find('.el-input').trigger('keyup.enter')
      afterSearch("你好")
    })

    it("add search history after dealing with keyword", async () =>{
      wrapper.setData({
        searchInput: "   你   很   好   "
      })
      await wrapper.find('.el-input').trigger('keyup.enter')
      afterSearch("   你   很   好   ")

      wrapper.vm.$refs.search_input.focus()
      expect(wrapper.findAll("p.history-item").at(0).text()).toBe("你 很 好")
    })

    it("search an item already in history", async () =>{
      wrapper.setData({
        searchInput: "你不好"
      })
      await wrapper.find('.el-input').trigger('keyup.enter')
      afterSearch("你不好")

      wrapper.setData({
        searchInput: "你好"
      })
      await wrapper.find('.el-input').trigger('keyup.enter')
      afterSearch("你好")

      wrapper.vm.$refs.search_input.focus()
      expect(wrapper.findAll("p.history-item").at(0).text()).toBe("你好")
    })

    it("click search history item route to specific search", async () =>{
      await wrapper.findAll("p.history-item").at(1).trigger('click')
      afterSearch("你不好")

      wrapper.vm.$refs.search_input.focus()
      expect(wrapper.findAll("p.history-item").at(0).text()).toBe("你不好")
    })

    it("click delete history item", async () =>{
      await wrapper.findAll("p.remove-history").at(1).trigger('click')

      expect(wrapper.findAll("p.history-item").length).toBe(2)
    })

    it("click delete all history items", async () =>{
      await wrapper.findAll("p.remove-history").at(2).trigger('click')

      expect(wrapper.findAll("p.history-item").length).toBe(0)
    })
  })
  