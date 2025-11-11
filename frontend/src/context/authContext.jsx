import { useContext, createContext, useState, useEffect } from "react";
import api from '../services/api'

const AuthContext = createContext()

export const useAuthContext = () => useContext(AuthContext)

export const AuthProvider = ({ children }) => {
    const [User, setUser] = useState(null)
    const [Loading, setLoading] = useState(true)

    useEffect(() => {
        const token = localStorage.getItem('token')
        if (token) {
            fetchCurrentUser()
        }
        else {
            setLoading(false)
        }
    }, [])

    const fetchCurrentUser = async () => {
        try {
            const response = await api.get('/auth/users/me');
            setUser(response);
        }
        catch (err) {
            localStorage.removeItem('token');
        }
        finally {
            setLoading(false);
        }
    }

    const login = async (token) => {
        localStorage.setItem('token', token);
        await fetchCurrentUser(token);
    }

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
        
    }

    const value = {
        User, 
        Loading,
        login, 
        logout
    }

    return <AuthContext.Provider value={value}>
        {children}
    </AuthContext.Provider>
}