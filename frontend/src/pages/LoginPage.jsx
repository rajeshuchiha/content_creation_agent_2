import { useEffect, useState } from "react"
import { useNavigate, Link } from "react-router-dom";
import api from "@/services/api";
import { useAuthContext } from "@/context/authContext";

import { Input } from "@/components/ui/input";
import { Label } from "@radix-ui/react-label";
import { Button } from "@/components/ui/button";

import { Eye, EyeOff } from "lucide-react";

function Login() {

    const navigate = useNavigate();
    const { login } = useAuthContext();

    const [formData, setFormData] = useState({
        "username": "",
        "password": ""
    })

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value
        }))
    }

    const [show, setShow] = useState(false);

    const LoginHandler = async (e) => {
        e.preventDefault();

        const formDataToSend = new URLSearchParams({
            username: formData.username,
            password: formData.password
        })

        const response = await api.post('/auth/token', formDataToSend, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })

        const { access_token, token_type } = response.data
        await login(access_token)
        navigate('/dashboard')
    }

    // useEffect(()={

    // }, [])

    return (
        <div className="flex justify-center items-center">
            <form 
                onSubmit={LoginHandler}
                className="w-full max-w-md p-6 rounded-xl shadow-md space-y-4"
            >
                <h2 className="text-2xl font-bold text-center text-gray-900 dark:text-gray-50">
                    Login
                </h2>

                <div className="flex flex-col space-y-1">
                    <Label htmlFor="username" className="text-left">Username</Label>
                    <Input
                        id="username"
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        placeholder="Enter your username"
                    />
                </div>
                <div className="flex flex-col space-y-1 relative">
                    <Label htmlFor="password" className="text-left">Password</Label>
                    <Input
                        id="password"
                        type={show?"text":"password"}
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Enter your password (atleast 8 characters)"
                        className="w-full border rounded px-3 py-2 pr-10"
                    />
                    <Button 
                        type="button"
                        className="absolute right-0 top-7 cursor-pointer"
                        onClick={() => {setShow(!show)}}
                    >
                        {show? <EyeOff size={18} /> : <Eye size={18} />}
                    </Button>
                </div>
                
                <Button type="submit" className="bg-primary hover:bg-primary/90 text-sm text-primary-foreground 
                whitespace-nowrap transition-all disabled:pointer-events-none disabled:opacity-50 cursor-pointer">
                    Login
                </Button>
            </form>
        </div>
    )
}

export default Login