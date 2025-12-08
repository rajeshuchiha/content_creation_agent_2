import PostCard from "@/components/postCard";
import api from "@/services/api";
import { useEffect, useState } from "react";

function History() {
    const [Results, setResults] = useState([]);
    const [Loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchResults() {
            try{
                const res = await api.get("/results/history");
                console.log(res.data)
                setResults(res.data.items);
            }
            catch{
                setResults([]);
            }
            finally{
                setLoading(false)
            }
        }
        fetchResults();
    }, []);

    if(Loading){
        return <div>Loading...</div>
    }

    return (
        <div>
            {Results ? (
                Results.map((result) => (
                    <PostCard key={result.id} post={result} />
                ))
            ) :
                (
                    <h1>No History Found</h1>
                )
            }
        </div>
    );
}

export default History;