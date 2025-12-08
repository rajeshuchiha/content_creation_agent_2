import { Outlet } from "react-router-dom";
import Navbar from "@/components/navBar";

export function AppLayout(){
    return (
        <div className="min-h-screen w-full relative">
            <header className="absolute top-0 left-0 right-0 z-50">
                {<Navbar variant="solid" />}
            </header>
            <main className="w-full h-full">
                {<Outlet />}
            </main>
        </div>
    );
}