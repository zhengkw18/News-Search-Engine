import getWrapper from './utils'
import flushPromises from "flush-promises"
import "@/mock/index"
import Register from '@/views/Register'
import LoginDialog from "@/components/LoginDialog"
import cookie from "@/utils/cookie"
import AuthCode from "@/components/AuthCode"

describe('Register', () => {
    const wrapper = getWrapper.wrapper(Register)
    
    it("用户名不能为空", async () =>{
        await wrapper.setData({
            ruleForm: {
                username: "",
                email: "12345678@qq.com",
                password: "12345"
            }
        })

        expect(wrapper.find(".el-form-item__error").text()).toBe("用户名不能为空")
        expect(wrapper.vm.$data.valid).toBe(false)    
    }) 

    it("用户名格式错误", async () =>{
        await wrapper.setData({
            ruleForm: {
                username: "&1234",
                email: "12345678@qq.com",
                password: "12345"
            }
        })

        expect(wrapper.find(".el-form-item__error").text()).toBe("用户名格式错误")
        expect(wrapper.vm.$data.valid).toBe(false)    
    }) 

    it("密码长度不足", async () =>{
        await wrapper.setData({
            ruleForm: {
                username: "admin",
                email: "12345678@qq.com",
                password: "12"
            }
        })

        expect(wrapper.find(".el-form-item__error").text()).toBe("密码长度不足")
        expect(wrapper.vm.$data.valid).toBe(false)    
    })

    it("Undefined Interface", async () =>{
        await wrapper.setData({
            ruleForm: {
                username: "admin",
                email: "11111111@qq.com",
                password: "12345"
            }
        })

        expect(wrapper.vm.$data.valid).toBe(true)
        wrapper.findComponent(AuthCode).vm.$emit("success")
        await flushPromises() 
        
        expect(wrapper.find(".form-item__tip").text()).toBe("Undefined Interface")
        expect(wrapper.vm.$data.alreadySent).toBe(false)
    })

    it("邮箱激活码发送失败", async () =>{
        expect(wrapper.vm.$data.time > 0).toBe(true)
        wrapper.findComponent(AuthCode).vm.$emit("success")
        await flushPromises() 
        
        expect(wrapper.find(".form-item__tip").text()).toContain("邮箱激活码发送失败")
    })

    it("邮箱激活码发送成功", async () =>{
        await wrapper.setData({
            ruleForm: {
                username: "admin",
                email: "12345678@qq.com",
                password: "12345"
            },
            disabled: false
        })

        expect(wrapper.vm.$data.valid).toBe(true)
        wrapper.findComponent(AuthCode).vm.$emit("success")
        await flushPromises() 
        
        expect(wrapper.find(".form-item__tip").text()).toContain("邮箱激活码已发送")
    })

    it("用户名已存在", async () =>{
        await wrapper.setData({
            ruleForm: {
                username: "admin",
                email: "12345678@qq.com",
                password: "12345",
                check: "1234"
            }
        })
        await wrapper.findAll(".el-button").at(1).trigger("click")
        await flushPromises()   

        expect(wrapper.find(".header-error").text()).toBe("用户名已存在")
    })

    it("注册成功", async () =>{
        await wrapper.setData({
            ruleForm: {
                username: "curtis",
                email: "12345678@qq.com",
                password: "12345",
                check: "1234"
            },
            alreadySent: true
        })
        
        expect(wrapper.vm.$data.valid).toBe(true) 
        
        await wrapper.findAll(".el-button").at(1).trigger("click")
        await flushPromises() 

        expect(wrapper.find(".header-error").text()).toBe("")
        expect(cookie.get_cookie("username")).toBe("curtis")
        expect(cookie.get_cookie("password")).toBe("12345")
        expect(wrapper.vm.$router.history.current.name).toBe("Home")
    })

    it("登录成功", () =>{
        wrapper.findComponent(LoginDialog).vm.$emit("success") 
        expect(wrapper.findComponent(LoginDialog).vm.$props.dialogVisible).toBe(false)
        expect(wrapper.vm.$router.history.current.name).toBe("Home")
    })
  })
  