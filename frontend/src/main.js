import { createPinia } from "pinia"
import { createPersistedState } from "pinia-plugin-persistedstate";
import { createApp } from "vue"

import App from "./App.vue"
import router from "./router"

const app = createApp(App)
const pinia = createPinia();

pinia.use(
createPersistedState({
    storage: sessionStorage,
    auto: true,
})
);
app.use(pinia)
app.use(router)

app.mount("#app")