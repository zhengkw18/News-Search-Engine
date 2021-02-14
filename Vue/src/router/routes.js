import Home from '@/views/Home.vue'
import Register from '@/views/Register.vue'
import Search from '@/views/Search.vue'
import User from '@/views/User.vue'

const routes = [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/search',
      name: 'Search',
      component: Search,
    },
    {
      path: '/user',
      name: 'User',
      component: User,
    }
  ]

  export default routes