// lib/authClient.ts
import axios, { AxiosError } from "axios";
import * as SecureStore from "expo-secure-store";

const API_URL = "http://10.0.2.2:8000/api"; 
// Android emulator -> 10.0.2.2
// iOS simulator -> http://localhost:8000
// Real device -> "http://YOUR_LAN_IP:8000/api"

const ACCESS_KEY = "accessToken";
const REFRESH_KEY = "refreshToken";

async function saveTokens(access: string, refresh?: string) {
  await SecureStore.setItemAsync(ACCESS_KEY, access);
  if (refresh) await SecureStore.setItemAsync(REFRESH_KEY, refresh);
}

async function getAccessToken(): Promise<string | null> {
  return SecureStore.getItemAsync(ACCESS_KEY);
}

async function getRefreshToken(): Promise<string | null> {
  return SecureStore.getItemAsync(REFRESH_KEY);
}

export async function clearTokens() {
  await SecureStore.deleteItemAsync(ACCESS_KEY);
  await SecureStore.deleteItemAsync(REFRESH_KEY);
}

export const api = axios.create({
  baseURL: API_URL,
});

// attach access token
api.interceptors.request.use(async (config) => {
  const token = await getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest: any = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refresh = await getRefreshToken();
      if (!refresh) {
        await clearTokens();
        return Promise.reject(error);
      }

      try {
        const res = await axios.post(`${API_URL}/auth/refresh/`, { refresh });
        const newAccess = (res.data as any).access;
        await saveTokens(newAccess, refresh);

        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        return axios(originalRequest);
      } catch (e) {
        await clearTokens();
        return Promise.reject(e);
      }
    }

    return Promise.reject(error);
  }
);

// high-level helpers
export async function loginRequest(username: string, password: string) {
  const { data } = await axios.post(`${API_URL}/auth/login/`, {
    username,
    password,
  });
  await saveTokens(data.access, data.refresh);

  const meRes = await api.get("/auth/me/");
  return meRes.data;
}

export async function fetchCurrentUser() {
  try {
    const res = await api.get("/auth/me/");
    return res.data;
  } catch {
    return null;
  }
}
