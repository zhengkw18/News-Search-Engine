import getWrapper from './utils'
import "@/mock/index"
import UserTags from '@/components/UserTags'
import flushPromises from 'flush-promises'

describe('UserTags', () => {
    let wrapper = getWrapper.wrapper(UserTags)
    
    it("render tags of different types", async () =>{  
        await flushPromises()

        expect(wrapper.findAll(".el-tag").length).toBe(3)
        expect(wrapper.findAll(".el-tag").at(0).html()).toContain("danger")
        expect(wrapper.findAll(".el-tag").at(1).html()).toContain("warning")
        expect(wrapper.findAll(".button-remove-tags").length).toBe(1)
      })

    it("remove particular tag", async () =>{  
        await wrapper.findAll(".el-tag__close").at(0).trigger("click")
        await flushPromises()

        expect(wrapper.findAll(".el-tag").length).toBe(2)
      })

    it("remove all tags", async () =>{  
        await wrapper.find(".button-remove-tags").trigger("click")
        await wrapper.findAll(".el-button").at(1).trigger("click")
        await flushPromises()

        expect(wrapper.findAll(".el-tag").length).toBe(0)
        expect(wrapper.findAll(".button-remove-tags").length).toBe(0)
      })
  })
  