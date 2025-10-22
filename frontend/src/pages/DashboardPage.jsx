import Platform from "../components/platform";

function Dashboard(){
    
    return(
        <>
            <div>
                <h2>Hello DashBoard!</h2>
            </div>
            <Platform name={"Twitter"}/>
            <Platform name={"Reddit"}/>
            <Platform name={"Google"}/>
        </>
    );
}

export default Dashboard