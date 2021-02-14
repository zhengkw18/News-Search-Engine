import getWrapper from './utils'
import flushPromises from "flush-promises"
import "@/mock/index"
import LoginDialog from '@/components/LoginDialog'
import cookie from "@/utils/cookie"

let stateDefault = {
  username: "",
  password:""
}
let stateFail = {
  "username": "admin",
  "password": ""
}
let stateSuccess = {
  "username": "admin",
  "password": "admin"
}
describe('LoginDialog', () => {
  const wrapper = getWrapper.wrapper(LoginDialog)
  it("default value of props", () =>{
    expect(wrapper.vm.$props.state).toStrictEqual(stateDefault)
    expect(wrapper.vm.$props.dialogVisible).toStrictEqual(true)
  })

  it("renders props when passed", () =>{
    wrapper.setProps({
      dialogVisible: true,
      state: stateFail
    })
    expect(wrapper.vm.$props.state).toBe(stateFail)
  })

  it("input cannot be empty", async () => {
    await wrapper.find('.el-button').trigger('click')
    await flushPromises()

    expect(wrapper.find('.header-error').text()).toBe("输入不能为空")
  })

  it("close dialog", async () => {
    await wrapper.find('.el-dialog__headerbtn').trigger('click')
    
    expect(Object.prototype.hasOwnProperty.call(wrapper.emitted(), "hide")).toBe(true)
  })

  it("login success", async () => {
    cookie.delete_cookie("username")
    cookie.delete_cookie("password")
    
    wrapper.setProps({
      dialogVisible: true,
      state: stateSuccess
    })
    await wrapper.find('.el-button').trigger('click')
    await flushPromises()

    expect(wrapper.find('.header-error').text()).toBe("")
    expect(Object.prototype.hasOwnProperty.call(wrapper.emitted(), "success")).toBe(true)
    expect(cookie.get_cookie("username")).toBe("admin")
    expect(cookie.get_cookie("password")).toBe("admin")
  })
})
