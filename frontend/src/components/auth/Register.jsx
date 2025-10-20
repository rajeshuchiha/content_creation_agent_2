import { useEffect, useState } from "react"
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";


function Register() {

    const api = axios.create({
        baseURL: "http://localhost:8000/api",
        timeout: 10000,
    });
    
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        "username": "",
        "email": "",
        "password": ""
    })

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
        <div>
            <form onSubmit={RegisterHandler}>
                <label>Username:<input type="text" name="username" value={formData.username} onChange={handleChange}></input></label>
                <label>Email: <input type="email" name="email" value={formData.email} onChange={handleChange} /></label>
                <label>Password: <input type="text" name="password" value={formData.password} onChange={handleChange}></input></label>
                <button type="submit">Register</button>
            </form>
        </div>
    )
}

export default Register