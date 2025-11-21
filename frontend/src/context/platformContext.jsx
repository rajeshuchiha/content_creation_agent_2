import { useContext, createContext, useState, useEffect } from "react";
import api from '../services/api';
import { useAuthContext } from "./authContext";

const PlatformContext = createContext();

export const usePlatformContext = () => useContext(PlatformContext);

export const PlatformProvider = ({ children }) => {
    const [Platforms, setPlatforms] = useState({
        "twitter": false,
        "reddit": false,
        "google": false
    });
    const { User } = useAuthContext()

    useEffect(() => {
        if (!User) return;

        const fetchStatuses = async () => {
            try {
                const [twitter_status, reddit_status, google_status] = await Promise.all([
                    api.get("/auth/twitter/status"),
                    api.get("/auth/reddit/status"),
                    api.get("/auth/google/status"),
                ]);
                setPlatforms({
                    "twitter": twitter_status.data.integrated,
                    "reddit": reddit_status.data.integrated,
                    "google": google_status.data.integrated,
                });
            } catch (err) {
                console.error("Failed to fetch platform statuses", err);
            }
        };

        fetchStatuses();
    }, [User]);


    const togglePlatforms = async (platform) => {

        const newValue = !Platforms[platform];
        setPlatforms((prev) => ({ ...prev, [platform]: newValue }));

        try {
            if (newValue) {
                const { data } = await api.get(`/auth/${platform}/authorize`)
                window.location.href = data.auth_url
            }
            else {
                const { data } = await api.delete(`/auth/${platform}/user`);
                console.log(data)
            }

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