import { useState } from "react";
import { Search, Globe, Newspaper } from "lucide-react";
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
    const [TaskId, setTaskId] = useState(null)
    const [Status, setStatus] = useState("")


    const fetchResults = async (query, is_news) => {
        const results = await api.post(`/results/${encodeURIComponent(query)}${(is_news ? '?categories=news' : '')}`);

        return results.data
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await fetchResults(Query, isNews);

            setStatus(data.status)
            if (data.status !== "failed") {
                setTaskId(data.task_id)
            }
            else {
                console.log(data.error)
            }
        }
        catch (err) {
            console.error(err);
        }
        finally {
            setLoading(false);
        }
    }

    return (
        <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 text-center">
            <div className="mb-8 space-y-3 animate-in fade-in duration-500 slide-in-from-bottom-4">
                <h1 className="text-5xl font-bold bg-linear-to-r from-purple-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                    Content Gen
                </h1>
                <p className="text-gray-400 text-lg">Single topic to post across all</p>
            </div>

            <form
                onSubmit={handleSubmit}
                className="w-full max-w-lg bg-linear-to-br from-gray-900/60 to-gray-800/40 backdrop-blur-xl p-8 rounded-2xl border border-gray-700/50 shadow-2xl space-y-6"
            >
                <div className="space-y-2">
                    <Label htmlFor="search" className="block text-sm font-medium text-gray-300 text-left">Search </Label>
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                        <input
                            type="text"
                            id="search"
                            value={Query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Type any topic here... Eg. Technology"
                            className="w-full pl-10 pr-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        />
                    </div>
                </div>

                <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-300 text-left">
                        Filter by Category
                    </label>
                    <div className="grid grid-cols-2 gap-3">
                        {/* None Option */}
                        <button
                            type="button"
                            onClick={() => setNews(false)}
                            className={`relative overflow-hidden rounded-lg px-4 py-3 font-medium transition-all duration-300 ${!isNews
                                ? "bg-linear-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-500/30 scale-105"
                                : "bg-gray-800/50 text-gray-300 border border-gray-700 hover:border-gray-600 hover:bg-gray-800/70"
                                }`}
                        >
                            <div className="relative z-10 flex items-center justify-center gap-2">
                                <Globe className="w-4 h-4" />
                                <span>All Content</span>
                            </div>
                        </button>

                        {/* News Option */}
                        <button
                            type="button"
                            onClick={() => setNews(true)}
                            className={`relative overflow-hidden rounded-lg px-4 py-3 font-medium transition-all duration-300 ${isNews
                                ? "bg-linear-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-500/30 scale-105"
                                : "bg-gray-800/50 text-gray-300 border border-gray-700 hover:border-gray-600 hover:bg-gray-800/70"
                                }`}
                        >
                            <div className="relative z-10 flex items-center justify-center gap-2">
                                <Newspaper className="w-4 h-4" />
                                <span>News Only</span>
                            </div>
                        </button>
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={!Query.trim() || Loading}
                    className="w-full bg-linear-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 
                text-white font-semibold py-3 px-6 rounded-lg shadow-lg shadow-purple-500/30 transition-all duration-300 
                disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none hover:scale-[1.02] active:scale-[0.98]">
                    {Loading ? "Searching..." : "Search"}
                </button>
                {/* Results Section */}
                <div className="pt-4 border-t border-gray-700/50">
                    {Loading ? (
                        <div className="py-8">
                            <Loader />
                            <p className="text-gray-400 text-sm mt-4">Processing your request...</p>
                        </div>
                    ) : TaskId ? (
                        <div className="space-y-3 animate-in fade-in duration-300 slide-in-from-top-2">
                            <div className="bg-gray-800/40 rounded-lg p-4 border border-gray-700/50">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm text-gray-400">Task ID</span>
                                    <span className="text-xs bg-purple-600/20 text-purple-400 px-2 py-1 rounded border border-purple-600/30">
                                        {TaskId}
                                    </span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-gray-400">Status</span>
                                    <span className={`text-xs px-2 py-1 rounded border ${Status === "started"
                                            ? "bg-green-600/20 text-green-400 border-green-600/30"
                                            : Status === "failed"
                                                ? "bg-red-600/20 text-red-400 border-red-600/30"
                                                : "bg-yellow-600/20 text-yellow-400 border-yellow-600/30"
                                        }`}>
                                        {Status}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <p className="text-gray-500 text-sm py-4">Enter a search query to get started</p>
                    )}
                </div>
            </form>

        </div>
    );
}

export default Content;