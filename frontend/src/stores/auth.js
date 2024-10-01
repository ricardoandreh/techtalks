import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(null);
  const refreshToken = ref(null);
  const expiration = ref(null);

  async function fetchToken(loginData) {
    console.log(loginData)
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/token/`,
        null,
        {
          data: {
            email: loginData?.email,
            password: loginData?.password,
          },
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      token.value = response.data.access_token;
      refreshToken.value = response.data.refresh_token;
      expiration.value = Date.now() + 60 * 1000;
    } catch (error) {
      console.error("Erro ao obter token:", error);
    }
  }

  async function fetchRefreshToken(loginData) {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/token/refresh`,
        null,
        {
          data: {
            email: loginData?.email,
            password: loginData?.password,
          },
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      if (response.data.refresh_token) {
        refreshToken.value = response.data.refresh_token;
      }

      token.value = response.data.access_token;
      expiration.value = Date.now() + 60 * 1000;
    } catch (error) {
      console.error("Erro ao obter refresh token:", error);
    }
  }

  async function isTokenValid() {
    if (Date.now() >= expiration.value) {
      await fetchRefreshToken();
    }
  }

  function $reset() {
    token.value = null;
    refreshToken.value = null;
    expiration.value = null;
  }

  return {
    token,
    refreshToken,
    expiration,
    fetchToken,
    fetchRefreshToken,
    isTokenValid,
    $reset,
  };
});
