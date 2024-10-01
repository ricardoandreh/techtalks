import { createRouter, createWebHistory } from "vue-router"
import EventDetailView from "../views/EventDetailView.vue"
import EventListView from "../views/EventListView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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