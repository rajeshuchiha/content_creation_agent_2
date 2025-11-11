import { useState } from "react";
import api from "../services/api";
import PostCard from "./postCard";

import { Input } from "@/components/ui/input";
import { Label } from "@radix-ui/react-label";
import { Button } from "@/components/ui/button";

import Loader from "./loader";

function Content() {

    const [Query, setQuery] = useState("")
    const [isNews, setNews] = useState(false)
    const [Posts, setPosts] = useState([])
    const [Loading, setLoading] = useState(false)


    const fetchResults = async (query, is_news) => {

        const results = await api.get(`/results/${encodeURIComponent(query)}${(is_news ? '?categories=news' : '')}`);

        const data = results.data.Items;
        return data;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try{
            const data = await fetchResults(Query, isNews);
            setPosts(data);
        }
        catch(err){
            console.error(err);
        }
        finally{
            setLoading(false);
        }
    }

    return (
        <div className="flex flex-col justify-center items-center">
            <form 
                onSubmit={handleSubmit}
                className="w-full max-w-md p-6 rounded-xl shadow-md space-y-4"
            >
                <div className="flex items-center gap-2">
                    <Label htmlFor="search">Search </Label>
                    <Input type="text" id="search" value={Query} onChange={(e) => { setQuery(e.target.value) }} />
                </div>
            
                <div className="flex items-center gap-2">
                    <Label className="text-sm font-medium text-left">Categories</Label>

                    <div className="flex gap-3 mt-2">
                        {/* NONE CARD */}
                        <div
                            onClick={() => setNews(false)}
                            className={`cursor-pointer border rounded-lg px-4 py-2 transition 
                                ${!isNews ? "bg-primary text-primary-foreground border-primary" : "hover:bg-muted"}`}
                        >
                        None
                        </div>

                        {/* NEWS CARD */}
                        <div
                            onClick={() => setNews(true)}
                            className={`cursor-pointer border rounded-lg px-4 py-2 transition
                                ${isNews ? "bg-primary text-primary-foreground border-primary" : "hover:bg-muted"}`}
                        >
                        News
                        </div>
                    </div>
                </div>

                
                <Button type="submit" className="bg-primary hover:bg-primary/90 text-sm text-primary-foreground 
                whitespace-nowrap transition-all disabled:pointer-events-none disabled:opacity-50 cursor-pointer">
                    Search
                </Button>
            </form>
            <div className="flex justify-center w-full">
                {Loading ? <Loader /> :
                    <div className="current-post">
                        {Posts && Posts.map((post) => {
                            return <PostCard key={post.id} post={post} />
                        })}
                    </div>
                }
            </div>
        </div>
    );
}

export default Content;