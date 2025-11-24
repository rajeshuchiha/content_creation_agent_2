import { Navigate } from "react-router-dom";
import { useAuthContext } from "@/context/authContext";

export default function ProtectedRoute({ children }) {
    const { User } = useAuthContext();

    return User ? children : <Navigate to="/login" replace />;
}