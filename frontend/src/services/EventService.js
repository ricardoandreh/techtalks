import axios from "axios";
import { useAuthStore } from "../stores/auth";

const apiClient = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api`,
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(async (config) => {
  const authStore = useAuthStore();

  if (authStore.token) {
    await authStore.isTokenValid();

    config.headers.Authorization = `Bearer ${authStore.token}`;
  }

  return config;
});

export default {
  getEvents() {
    return apiClient.get("/events");
  },
  getEvent(id) {
    return apiClient.get("/events/" + id);
  },
};
