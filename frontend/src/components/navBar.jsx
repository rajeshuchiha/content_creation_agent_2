import { Link } from "react-router-dom"

function NavBar(){
    return (
        <nav className="navbar">
            <div className="navbar-home">
                <Link to="/">Home</Link>
            </div>
            <div className="navbar-login">
                <Link to="/login">Login</Link>
            </div>
            <div className="navbar-register">
                <Link to="/register">Register</Link>
            </div>
        </nav>
    )
}

export default NavBar