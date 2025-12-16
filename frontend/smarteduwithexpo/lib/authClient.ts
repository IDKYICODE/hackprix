// lib/authClient.ts

import axios, { AxiosError } from "axios";
import * as SecureStore from "expo-secure-store";
import { Platform } from "react-native";

const API_URL =
Platform.OS === "android"
? "http://10.0.2.2:8000/api"
: "http://192.168.31.114:8000/api";

// 🔑 Single source of truth for keys
const ACCESS_KEY = "accessToken";
const REFRESH_KEY = "refreshToken";

/* -----------------------------
Cross-platform secure storage
-------------------------------- */
const storage = {
async getItem(key: string): Promise<string | null> {
    if (Platform.OS === "web") {
      return localStorage.getItem(key);
    }
    return SecureStore.getItemAsync(key);
  },

  async setItem(key: string, value: string): Promise<void> {
    if (Platform.OS === "web") {
      localStorage.setItem(key, value);
      return;
    }
    await SecureStore.setItemAsync(key, value);
  },

  async deleteItem(key: string): Promise<void> {
    if (Platform.OS === "web") {
      localStorage.removeItem(key);
      return;
    }
    await SecureStore.deleteItemAsync(key);
  },
};

/* -----------------------------
   Token helpers
-------------------------------- */
async function saveTokens(access: string, refresh?: string) {
  await storage.setItem(ACCESS_KEY, access);
  if (refresh) {
    await storage.setItem(REFRESH_KEY, refresh);
  }
}

async function getAccessToken() {
  return storage.getItem(ACCESS_KEY);
}

async function getRefreshToken() {
  return storage.getItem(REFRESH_KEY);
}

export async function clearTokens() {
  await storage.deleteItem(ACCESS_KEY);
  await storage.deleteItem(REFRESH_KEY);
}

/* -----------------------------
   Axios instance
-------------------------------- */
export const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

/* -----------------------------
   Request interceptor
   (DO NOT attach token to login/refresh)
-------------------------------- */
api.interceptors.request.use(async (config) => {
  const skipAuth =
    config.url?.includes("/auth/login/") ||
    config.url?.includes("/auth/refresh/");

  if (!skipAuth) {
    const token = await getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }

  return config;
});

/* -----------------------------
   Response interceptor (auto-refresh)
-------------------------------- */
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest: any = error.config;

    if (error.response?.status === 401 && !originalRequest?._retry) {
      originalRequest._retry = true;

      const refresh = await getRefreshToken();
      if (!refresh) {
        await clearTokens();
        return Promise.reject(error);
      }

      try {
        const res = await api.post("/auth/refresh/", { refresh });
        const newAccess = (res.data as any).access;

        await saveTokens(newAccess, refresh);
        originalRequest.headers.Authorization = `Bearer ${newAccess}`;

        return api(originalRequest);
      } catch {
        await clearTokens();
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

/* -----------------------------
   Auth API helpers
-------------------------------- */
export async function loginRequest(username: string, password: string) {
  const { data } = await api.post("/auth/login/", {
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

export async function updateProfile(formData: FormData) {
  const res = await api.patch("/auth/profile/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return res.data;
}
