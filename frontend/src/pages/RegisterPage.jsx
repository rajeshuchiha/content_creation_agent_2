import { useEffect, useState } from "react"
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

import { Input } from "@/components/ui/input";
import { Label } from "@radix-ui/react-label";
import { Button } from "@/components/ui/button";

import { Eye, EyeOff } from "lucide-react";

function Register() {

    const API_URL = import.meta.env.VITE_API_URL;

    const api = axios.create({
        baseURL: `${API_URL}/api`,
        timeout: 10000,
    });
    
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        "username": "",
        "email": "",
        "password": ""
    })

    const [show, setShow] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value
        }))
    }

    const RegisterHandler = async (e) => {
        e.preventDefault();

        try{
            const response = await api.post("/auth/register", formData, {
                headers: { "Content-Type": "application/json" },
            });

            alert("Registration Successful")
            navigate('/')
        }
        catch (err) {
            if (err.response) {
                console.error("Server responded with:", err.response.data);
                alert(err.response.data.detail || "Registration failed");
            } else {
                console.error("Error:", err);
                alert("Something went wrong");
            }
        }
    }

    // useEffect(()={

    // }, [])

    return (
        <div className="flex justify-center items-center">
            <form 
                onSubmit={RegisterHandler}
                className="w-full max-w-md p-6 rounded-xl shadow-md space-y-4"
            >
                <h2 className="text-2xl font-bold text-center text-gray-900 dark:text-gray-50">
                    Register
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

                <div className="flex flex-col space-y-1">
                    <Label htmlFor="email" className="text-left">Email</Label>
                    <Input
                        id="email"
                        type="email"
                        name="email"
                        value={formData.email}
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
                    Register
                </Button>
            
            </form>
        </div>
    )
}

export default Register