import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu";
import { Link } from "react-router-dom";

export default function Navbar() {
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
      </div>
    </nav>
  );
}
