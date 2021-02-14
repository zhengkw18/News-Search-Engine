import getWrapper from './utils'
import "@/mock/index"
import UserInformation from '@/components/UserInformation'
import cookie from "@/utils/cookie"
import flushPromises from 'flush-promises'

describe('UserInformation', () => {
    let wrapper = getWrapper.wrapper(UserInformation)

    it("get email successfully", async () =>{  
        await flushPromises()

        expect(wrapper.vm.$data.email.length == 0).toBe(false)
      })
    
    it("empty username route to home", () =>{  
        cookie.delete_cookie("username")
        expect(cookie.get_cookie("username")).toBe("")
        wrapper = getWrapper.wrapper(UserInformation)
        expect(wrapper.vm.$router.history.current.name).toBe("Home")
      })
  })
  