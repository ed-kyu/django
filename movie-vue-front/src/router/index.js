import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Signup from '@/views/accounts/Signup'
import Login from '@/views/accounts/Login'
import Profile from '@/views/accounts/Profile'
import MovieDetail from '@/components/MovieDetail'
import ReviewDetail from '@/components/ReviewDetail/ReviewDetail'
import FindMovie from '@/components/FindMovie.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: Login,
  },  
  {
    path: '/accounts/',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/movie/detail/:id',
    name: 'Detail',
    component: MovieDetail
  },
  {
    path: '/reviews',
    name: 'ReviewDetail',
    component: ReviewDetail
  },
  {
    path: '/findmovie',
    name: 'FindMovie',
    component: FindMovie
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
