import axios from "axios";
import api_url from "./api_url";

const API_URL = api_url;     

const api = axios.create({
    baseURL: `${API_URL}/api`,
    withCredentials: true,
    timeout: 10000,
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            console.log("Token expired, logging out...");
        }
        return Promise.reject(error);
    }
);


export default api;
