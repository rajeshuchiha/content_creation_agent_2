import DOMPurify from 'dompurify';
import ReactMarkdown from "react-markdown"
import { useState } from 'react';

function PostCard({ post }) {

    // Safety check just in case
    if (!post) return null;

    const htmlString = post.blog_post || '';
    const sanitized = DOMPurify.sanitize(htmlString);

    // const textOnly = sanitized.replace(/<[^>]+>/g, "");
    const [blogExpanded, setBlogExpanded] = useState(false);
    const [redditExpanded, setRedditExpanded] = useState(false);

    return (
        <div className="bg-gray-900/40 backdrop-blur-md border border-gray-800/50 rounded-xl p-6 mb-6 hover:shadow-[0_0_20px_rgba(168,85,247,0.15)] transition-all duration-300 hover:border-purple-500/30 group">
            <div className="space-y-6">
                {/* Tweet Section */}
                <div className="bg-blue-950/20 p-4 rounded-lg border border-blue-900/30 relative overflow-hidden group/tweet hover:border-blue-300/30">
                    <div className="absolute top-0 right-0 w-20 h-20 bg-blue-500/10 blur-2xl rounded-full transform translate-x-10 -translate-y-10 group-hover/tweet:bg-blue-400/20 transition-all duration-500"></div>
                    <span className="text-xs font-semibold text-blue-400 uppercase tracking-wider mb-2 block relative z-10">Twitter</span>
                    <p className="text-gray-200 text-lg font-medium relative z-10 leading-relaxed">{post.tweet}</p>
                </div>

                {/* Blog Post Section */}
                <div className="bg-purple-950/10 p-4 rounded-lg border border-purple-900/20 relative overflow-hidden hover:border-purple-300/30">
                    <div className="absolute bottom-0 left-0 w-32 h-32 bg-purple-500/10 blur-3xl rounded-full transform -translate-x-10 translate-y-10"></div>
                    <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider mb-2 block relative z-10">Blog Post</span>
                    <h1 className="text-xl font-bold text-gray-100 mb-3 relative z-10">Blog Post</h1>
                    {/* <div
                        className="relative z-10 content-wrapper prose prose-invert prose-purple max-w-none text-gray-300 line-clamp-3"
                        dangerouslySetInnerHTML={{ __html: sanitized }}
                    /> */}
                    <div className='relative z-10'>
                        <div
                            className={`content-wrapper prose prose-invert prose-purple max-w-none text-gray-300 
                                ${blogExpanded ? "line-clamp-none" : "line-clamp-3"}`}
                            dangerouslySetInnerHTML={{ __html: sanitized }}
                        />
                        <button
                            className="text-blue-400 hover:text-blue-400/40 cursor-pointer underline mt-1"
                            onClick={() => setBlogExpanded(!blogExpanded)}
                        >
                            {blogExpanded ? "Show less" : "Show more"}
                        </button>
                    </div>

                </div>

                {/* Reddit Section */}
                {post.reddit_post && (
                    <div className="bg-orange-950/10 p-4 rounded-lg border border-orange-900/20 relative overflow-hidden hover:border-orange-300/30">
                        <div className="absolute top-1/2 left-1/2 w-40 h-40 bg-orange-500/5 blur-3xl rounded-full transform -translate-x-1/2 -translate-y-1/2"></div>
                        <span className="text-xs font-semibold text-orange-400 uppercase tracking-wider mb-2 block relative z-10">Reddit</span>
                        <p className="text-lg font-bold text-gray-100 mb-2 relative z-10">{post.reddit_post.title}</p>
                        {/* <p className="text-gray-300 relative z-10 leading-relaxed">{post.reddit_post.body}</p> */}
                        <div className='relative z-10'>
                            <div
                                className={`content-wrapper prose prose-invert prose-purple max-w-none text-gray-300 leading-relaxed    
                                ${redditExpanded ? "line-clamp-none" : "line-clamp-3"}`}
                            >
                                <ReactMarkdown>{post.reddit_post.body}</ReactMarkdown>
                            </div>
                            <button
                                className="text-blue-400 hover:text-blue-400/40 cursor-pointer underline mt-1"
                                onClick={() => setRedditExpanded(!redditExpanded)}
                            >
                                {redditExpanded ? "Show less" : "Show more"}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div >
    );
}

export default PostCard;

// import DOMPurify from 'dompurify';
// import { MessageCircle, FileText, Hash } from 'lucide-react';

// function PostCard({ post }) {
//     const htmlString = post.blog_post || '';
//     const sanitized = DOMPurify.sanitize(htmlString);

//     return (
//         <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 mb-6 overflow-hidden border border-gray-200">
//             {/* Tweet Section */}
//             <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-4 border-b border-gray-200">
//                 <div className="flex items-start gap-3">
//                     <MessageCircle className="w-5 h-5 text-blue-600 mt-1 flex-shrink-0" />
//                     <div className="flex-1">
//                         <h3 className="text-sm font-semibold text-gray-700 mb-2">Tweet</h3>
//                         <p className="text-gray-800 leading-relaxed">{post.tweet}</p>
//                     </div>
//                 </div>
//             </div>

//             {/* Blog Post Section */}
//             <div className="p-6 border-b border-gray-200">
//                 <div className="flex items-center gap-2 mb-4">
//                     <FileText className="w-5 h-5 text-green-600" />
//                     <h3 className="text-lg font-bold text-gray-900">Blog Post</h3>
//                 </div>
//                 <div
//                     className="prose prose-sm max-w-none text-gray-700 leading-relaxed"
//                     dangerouslySetInnerHTML={{ __html: sanitized }}
//                 />
//             </div>

//             {/* Reddit Post Section */}
//             {post.reddit_post && (
//                 <div className="bg-orange-50 p-4">
//                     <div className="flex items-start gap-3">
//                         <Hash className="w-5 h-5 text-orange-600 mt-1 flex-shrink-0" />
//                         <div className="flex-1">
//                             <h3 className="text-sm font-semibold text-gray-700 mb-2">Reddit Post</h3>
//                             <h4 className="font-bold text-gray-900 mb-2">{post.reddit_post.title}</h4>
//                             {post.reddit_post.body && (
//                                 <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
//                                     {post.reddit_post.body}
//                                 </p>
//                             )}
//                         </div>
//                     </div>
//                 </div>
//             )}
//         </div>
//     );
// }


// export default PostCard;   