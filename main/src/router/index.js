import { createRouter, createWebHistory} from 'vue-router'
import Ping from '../components/Ping.vue'
import Logs from '../components/Logs.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path:'/', redirect:'/logs' },
    { path: '/ping', name: 'ping', component: Ping },
    { path:'/logs', name:'logs', component:Logs },
    { path:'/:pathMatch(.*)*', redirect:'/logs'}
  ]
})

export default router