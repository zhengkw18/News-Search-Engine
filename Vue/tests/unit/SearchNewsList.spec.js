import getWrapper from './utils'
import SearchNewsList from '@/components/SearchNewsList'

let dateFormat = (time) => {
    let date = new Date(time)
    return date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() 
      + " " + date.getHours() + ":" +  date.getMinutes() + ":" + date.getSeconds()
  }

describe('SearchNewsList', () => {
    let wrapper = getWrapper.wrapper(SearchNewsList)

    it("display news time", () =>{
        expect(wrapper.vm.getTime(dateFormat(new Date().getTime()))).toBe("刚刚")
        expect(wrapper.vm.getTime(dateFormat(new Date().getTime() - 1000))).toBe("1秒前")
        expect(wrapper.vm.getTime(dateFormat(new Date().getTime() - 60 * 1000))).toBe("1分钟前")
        expect(wrapper.vm.getTime(dateFormat(new Date().getTime() - 60 * 60 * 1000))).toBe("1小时前")
        expect(wrapper.vm.getTime(dateFormat(new Date().getTime() - 24 * 60 * 60 * 1000))).toContain("&nbsp;")
    })
})