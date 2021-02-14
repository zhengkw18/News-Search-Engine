import getWrapper from './utils'
import flushPromises from "flush-promises"
import "@/mock/index"
import UserPassword from '@/components/UserPassword'
import cookie from "@/utils/cookie"

describe('UserPassword', () => {
    const wrapper = getWrapper.wrapper(UserPassword)

    it("密码长度不足", async () =>{
        await wrapper.setData({
            ruleForm: {
                password: "12"
            }
        })

        expect(wrapper.find(".el-form-item__error").text()).toBe("密码长度不足")
        expect(wrapper.vm.$data.valid).toBe(false)    
    })

    it("密码不能为空", async () =>{
        await wrapper.setData({
            ruleForm: {
                password: ""
            }
        })

        expect(wrapper.find(".el-form-item__error").text()).toBe("密码不能为空")
        expect(wrapper.vm.$data.valid).toBe(false)    
    }) 

    it("新密码不能与旧密码相同", async () =>{
        cookie.add_cookie("password", "12345", 24)
        await wrapper.setData({
            ruleForm: {
                password: "12345"
            }
        })

        expect(wrapper.find(".el-form-item__error").text()).toBe("新密码不能与旧密码相同")
        expect(wrapper.vm.$data.valid).toBe(false)    
    }) 

    it("设置新密码正确", async () =>{
        await wrapper.setData({
            ruleForm: {
                password: "666666"
            }
        })

        expect(wrapper.vm.$data.valid).toBe(true)    
    })

    it("密码格式错误", async () =>{
        await wrapper.find(".el-button").trigger("click")
        await flushPromises()   

        expect(wrapper.find(".header-error").text()).toBe("密码格式错误")
    })

    it("密码修改成功", async () =>{
        await wrapper.setData({
            ruleForm: {
                password: "123456"
            }
        })
        
        expect(wrapper.vm.$data.valid).toBe(true) 
        
        await wrapper.find(".el-button").trigger("click")
        await flushPromises() 

        expect(wrapper.find(".header-error").text()).toBe("")
        expect(cookie.get_cookie("password")).toBe("123456")
        expect(wrapper.vm.$router.history.current.name).toBe("Home")
    })
  })
  