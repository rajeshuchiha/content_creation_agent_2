import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";

import { useAuthContext } from "@/context/authContext";

export default function Navbar() {

  const { User, logout, Loading } = useAuthContext();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/")
  }

  if(Loading){
    return <div></div>;
  }

  return (
    <nav>
      <div className="max-w-6xl mx-auto px-6 py-3 flex justify-between items-center font-medium">
        {/* Left side */}
        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Link to="/">Home</Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>

        {/* Right side */}
        {User?(
          <div className="flex items-center space-x-6">
            <Button
              onClick={handleLogout}
              className="bg-primary hover:bg-primary/90 text-sm text-primary-foreground 
                        whitespace-nowrap transition-all disabled:pointer-events-none disabled:opacity-50 cursor-pointer">
              Logout
            </Button>
          </div>
        ):
        (
          <div className="flex items-center space-x-6">
            <Link
              to="/login"
              className="text-gray-700 dark:text-gray-200 hover:text-blue-600"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="px-3 py-1 rounded-md bg-blue-600 text-white hover:bg-blue-700"
            >
              Register
            </Link>
          </div>
        )}
        
      </div>
    </nav>
  );
}
