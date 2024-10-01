<script setup>
import { ref } from "vue"
import { useAuthStore } from "../stores/auth"

const authStore = useAuthStore()
const { fetchToken } = authStore

const email = ref()
const password = ref()

const login = () => fetchToken({ email: email.value, password: password.value })
</script>

<template>
  <section>
    <form @submit.prevent="login">
      <label>
        Email
        <input type="text" v-model="email" />
      </label>
      <label>
        Password
        <input type="password" v-model="password" />
      </label>
      <button type="submit">Log in</button>
    </form>
  </section>
</template>

<style scoped>
  button,
  input {
    display: block;
    margin-bottom: 10px;
  }

  #alert {
    color: red;
    margin-bottom: 10px;
  }

  form {
    display: flex;
    flex-direction: column;
    width: 200px;
    align-items: center;
    justify-items: center;
    margin: 0 auto;
  }
</style>