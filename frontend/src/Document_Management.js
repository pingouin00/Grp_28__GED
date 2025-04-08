import axios from "axios"
import { ACCESS_TOKEN } from "./constants"

const  Document_Management = axios.create({
    baseURL: import.meta.env.VITE_API_URL? import.meta.env.VITE_API_URL : Document_ManagementUrl,
});

Document_Management.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default  Document_Management;