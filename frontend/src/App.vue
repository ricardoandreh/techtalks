<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import HelloWorld from "./components/HelloWorld.vue";

const data = ref(null);

onMounted(async () => {
  try {
    const response = await axios.get(import.meta.env.VITE_API_URL);
    data.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
});
</script>

<template>
  <div>
    <a href="https://vitejs.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld :data="data" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
