import axios from "axios";

const api = axios.create({
    baseURL: "https://bank-statement-analyzer-x2z0.onrender.com"
});

export default api;