import { ref } from "vue";
import api from "./api";

export function useAuth() {
  const user = ref<{ id: number; username: string } | null>(null);
  const error = ref<string | null>(null);

  const login = async (username: string, password: string) => {
    try {
      error.value = null;
      const response = await api.post("/api/login", { username, password });
      user.value = response.data;
      return true;
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Login failed";
      return false;
    }
  };

  return { user, error, login };
}