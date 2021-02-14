import {mount, createLocalVue} from '@vue/test-utils'
import ElementUI from 'element-ui'
import  VueLazyload from 'vue-lazyload'
import VueRouter from "vue-router"
import Search from '@/views/Search'
import Home from '@/views/Home'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueLazyload)
localVue.use(VueRouter)

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push (location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
  {
    path: '/',
    name: 'Home'
  },
  {
    path: '/register',
    name: 'Register'
  },
  {
    path: '/search',
    name: 'Search'
  }
]
let router = new VueRouter({ 
  mode: 'history', 
  routes 
})

const getWrapper = {
  wrapper: function(component){
    return mount(component, {
      localVue,
      router
    })
  },
  propsWrapper: function(component, props){
    return mount(component, {
      localVue,
      router,
      propsData: props
    })
  },
  searchWrapper: function(kd, pn){
    router.push({    
      name: 'Search',  
      query: {   
        "kd": kd,
        "pn": pn
      }   
    })
    return mount(Search, {
      localVue,
      router
    })
  },
  homeWrapper: function(chnl){
    router.push({    
      name: 'Home',  
      query: {   
        "chnl": chnl
      }   
    })
    return mount(Home, {
      localVue,
      router
    })
  }
}

export default getWrapper