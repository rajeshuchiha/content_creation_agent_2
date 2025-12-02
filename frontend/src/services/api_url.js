const api_url = import.meta.env.VITE_API_URL || '';  //import.meta.env.VITE_API_URL for "Vercel", /api for nginx.conf location/api.

export default api_url;