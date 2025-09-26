import axios from 'axios';

const apiClient = axios.create({
    // baseURL: 'http://localhost:8000',
    baseURL: 'https://password-manager-api-julia.onrender.com',
    headers: { 'Content-Type': 'application/json' }
});

apiClient.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => Promise.reject(error));

export default apiClient;