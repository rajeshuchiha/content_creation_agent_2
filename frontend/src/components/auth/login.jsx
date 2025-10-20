import { useEffect, useState } from "react"
import { useNavigate, Link } from "react-router-dom";
import api from "../../services/api";
import { useAuthContext } from "../../context/authContext";

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
        <div>
            <form onSubmit={LoginHandler}>
                <label>Username:<input type="text" name="username" value={formData.username} onChange={handleChange}></input></label>
                <label>Password: <input type="text" name="password" value={formData.password} onChange={handleChange}></input></label>
                <button type="submit">Login</button>
            </form>
        </div>
    )
}

export default Login