import { createRouter, createWebHistory } from "vue-router"
import EventDetailView from "../views/EventDetailView.vue"
import EventListView from "../views/EventListView.vue"
import LoginView from "../views/LoginView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginView
    },
    {
      path: "/",
      name: "event-list",
      component: EventListView
    },
    {
      path: "/event/:id",
      name: "event-details",
      props: true,
      component: EventDetailView
    },
  ]
})

export default router