import Platform from "../components/platform";
import Content from "../components/content";

function Dashboard() {

    return (
        <div className="relative text-white overflow-hidden bg-black">
            <div className="absolute top-[-100px] left-[-50px] w-[300px] h-[300px] rounded-full bg-purple-600/30 blur-[200px]" />
            <div className="absolute bottom-[-200px] right-[-150px] w-[500px] h-[500px] rounded-full bg-blue-600/30 blur-[200px]" />


            <div className="absolute right-50 top-50 flex flex-col justfiy-center space-y-9">
                <Platform name={"Twitter"} />
                <Platform name={"Reddit"} />
                <Platform name={"Google"} />
            </div>
            <Content />
        </div>
    );
}

export default Dashboard