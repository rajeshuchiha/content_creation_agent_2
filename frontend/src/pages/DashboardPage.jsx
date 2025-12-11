import Platform from "../components/platform";
import Content from "../components/content";

function Dashboard() {

    return (
        <div className="relative text-white overflow-hidden bg-black min-h-screen">
            {/* Animated Background Blurs */}
            <div className="absolute top-[-100px] left-[-50px] w-[300px] h-[300px] rounded-full bg-purple-600/30 blur-[200px] animate-pulse" />
            <div className="absolute bottom-[-200px] right-[-150px] w-[500px] h-[500px] rounded-full bg-blue-600/30 blur-[200px] animate-pulse" style={{ animationDelay: '1s' }} />
            <div className="absolute top-[40%] left-[50%] w-[400px] h-[400px] rounded-full bg-purple-500/20 blur-[200px] animate-pulse" style={{ animationDelay: '2s' }} />

            {/* Platform Buttons - Fixed Position */}
            <div className="absolute right-20 top-50 flex flex-col justfiy-center space-y-9 z-20">
                <Platform name="Twitter" />
                <Platform name="Reddit" />
                <Platform name="Google" />
            </div>

            {/* Main Content */}
            <Content />
        </div>
    );
}

export default Dashboard