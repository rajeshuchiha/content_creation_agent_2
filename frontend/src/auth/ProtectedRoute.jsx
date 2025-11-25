import { Navigate } from "react-router-dom";
import { useAuthContext } from "@/context/authContext";

export default function ProtectedRoute({ children }) {
    const { User, Loading } = useAuthContext();

    if(Loading){
        return <div>Loading...</div>;
    }

    return User ? children : <Navigate to="/login" replace />;
}