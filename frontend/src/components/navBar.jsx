import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu";
import { Link, useNavigate } from "react-router-dom";

import { useAuthContext } from "@/context/authContext";

export default function Navbar({ variant }) {

  const { User, logout, Loading } = useAuthContext();
  const navigate = useNavigate();
  const isTransparent = variant === "transparent";

  const handleLogout = () => {
    logout();
    navigate("/")
  }

  if (Loading) {
    return <div className="h-16"></div>;
  }

  return (
    <nav className={`${isTransparent ? '' : 'bg-white dark:bg-black'}`}>
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center font-medium">
        {/* Left side */}
        <NavigationMenu>
          <NavigationMenuList className="flex items-center space-x-6">
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                {User ? (
                  <Link to="/dashboard" className={`transition ${
                    isTransparent
                      ? 'text-white/90 hover:text-white'
                      : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                  }`}
                  >
                    Dashboard
                  </Link>
                ) :
                  <Link to="/" className={`transition ${
                    isTransparent
                      ? 'text-white/90 hover:text-white'
                      : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                  }`}
                  >
                    Home
                  </Link>
                }
              </NavigationMenuLink>
            </NavigationMenuItem>
            {User && (
              <NavigationMenuItem>
                <NavigationMenuLink asChild>
                  <Link to="/history" className={
                    isTransparent
                      ? 'text-white/90 hover:text-white transition'
                      : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition'
                  }
                  >
                    History
                  </Link>
                </NavigationMenuLink>
              </NavigationMenuItem>
            )}

          </NavigationMenuList>
        </NavigationMenu>

        {/* Right side */}
        {User ? (
          <div className="flex items-center space-x-4">
            <span className={
              isTransparent
                ? 'text-white/80 text-sm'
                : 'text-gray-600 dark:text-gray-400 text-sm'
            }
            >
              {User.username}
            </span>
            <button
              onClick={handleLogout}
              variant={isTransparent ? "outline" : "default"}
              className={`cursor-pointer ${
                  isTransparent
                  ? 'px-4 py-2 rounded-lg border border-white/30 text-white hover:bg-white/10 transition'
                  : 'px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 transition'
                }`
              }
            // className="bg-primary hover:bg-primary/90 text-sm text-primary-foreground 
            //           whitespace-nowrap transition-all disabled:pointer-events-none disabled:opacity-50 cursor-pointer"
            >
              Logout
            </button>
          </div>
        ) :
          (
            <div className="flex items-center space-x-6">
              <Link
                to="/login"
                // className="text-gray-700 dark:text-gray-200 hover:text-blue-600"
                className={
                  isTransparent
                    ? 'text-white/90 hover:text-white transition'
                    : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition'
                }
              >
                Login
              </Link>
              <Link
                to="/register"
                // className="px-3 py-1 rounded-md bg-blue-600 text-white hover:bg-blue-700"
                className={
                  isTransparent
                    ? 'px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm text-white border border-white/20 hover:bg-white/20 transition'
                    : 'px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition'
                }
              >
                Register
              </Link>
            </div>
          )}

      </div>
    </nav>
  );
}
