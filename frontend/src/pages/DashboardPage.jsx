import Platform from "../components/platform";
import Content from "../components/content";

function Dashboard(){
    
    return(
        <>
            <div>
                <h2>Hello DashBoard!</h2>
            </div>
            <div className="flex flex-col justfiy-center space-y-4">
                <Platform name={"Twitter"}/>
                <Platform name={"Reddit"}/>
                <Platform name={"Google"}/>
            </div>
            <Content />
        </>
    );
}

export default Dashboard