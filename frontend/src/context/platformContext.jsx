import { useContext, createContext, useState, useEffect } from "react";
import api from '../services/api';

const PlatformContext = createContext();

export const usePlatformContext = () => useContext(PlatformContext);

export const PlatformProvider = ({ children }) => {
    const [Platforms, setPlatforms] = useState({
        "twitter": false,
        "reddit": false,
        "google": false
    });

    useEffect(() => {
        const fetchStatuses = async () => {
            try {
                const [twitter_status, reddit_status, google_status] = await Promise.all([
                    api.get("/auth/twitter/me"),
                    api.get("/auth/reddit/me"),
                    api.get("/auth/google/me"),
                ]);
                setPlatforms({
                    "twitter": twitter_status,
                    "reddit": reddit_status,
                    "google": google_status,
                });
            } catch (err) {
                console.error("Failed to fetch platform statuses", err);
            }
        };

        fetchStatuses();
    }, []);


    const togglePlatforms = async(platform) => {
        
        const newValue = !Platforms[platform];
        setPlatforms((prev) => ({ ...prev, [platform]: newValue }));
        
        try {
            const res = newValue
                ? await api.get(`/auth/${platform}/authorize`)
                : await api.delete(`/auth/${platform}/user`);
            const data = await res.json();
            console.log(data);
        } catch (err) {
            console.error("API error", err);
            // optionally revert state if API fails
            setPlatforms((prev) => ({ ...prev, [platform]: !newValue }));
        }
    };

    const value = {
        Platforms,
        togglePlatforms
    };

    return <PlatformContext.Provider value={value}>
        {children}
    </PlatformContext.Provider>;
}