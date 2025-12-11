import PostCard from "@/components/postCard";
import api from "@/services/api";
import { useEffect, useState } from "react";

function History() {
    const [Results, setResults] = useState([]);
    const [Loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchResults() {
            try {
                const res = await api.get("/results/history");
                console.log(res.data)
                setResults(res.data.items);
            }
            catch (error) {
                console.error("Failed to fetch history:", error);
                // Mock data for debugging
                const mockData = [
                    {
                        id: 1,
                        tweet: "Just discovered a cool new feature in React! 🚀 #webdev",
                        blog_post: `
                            <h2>Understanding Modern Web Interfaces</h2>
                            <p>
                            Modern web interfaces increasingly rely on flexible design systems, responsive layouts, and interactive components that adapt seamlessly across devices. Developers often integrate frameworks that provide structure while still allowing custom styling. As user expectations rise, interfaces must balance aesthetic appeal with performance, accessibility, and maintainability. The evolution of design practices has pushed teams to adopt component-driven development, where each UI element is reusable, testable, and consistent across an entire application. This shift not only improves developer productivity but also helps ensure that users experience coherent interfaces regardless of the page or feature they are interacting with.
                            </p>
                            <p>
                            At the core of any effective interface lies meaningful content. Typography, spacing, and layout contribute significantly to readability and overall user comfort. Clean HTML structure, combined with semantic elements such as headings and paragraphs, enhances both accessibility and SEO value. Designers also place emphasis on hierarchy, ensuring that information flows naturally and important elements draw appropriate attention. These principles form the foundation of content-first design, enabling users to consume information effortlessly.
                            </p>

                            <h3>The Role of Component-Driven Architecture</h3>
                            <p>
                            Component-driven architecture has become a foundational concept in modern web development. Instead of building entire pages at once, teams construct smaller, modular elements that can be assembled like building blocks. This approach not only increases efficiency but also reduces the cognitive load on developers who can now focus on isolated behaviors and styles. When paired with design systems, components become powerful tools for enforcing brand consistency and preventing UI drift. The modular nature allows teams to update or fix individual components without affecting the rest of the system, making maintenance far more manageable.
                            </p>
                            <p>
                            A common challenge with component-driven systems is ensuring proper communication between components while maintaining separation of concerns. Developers employ patterns such as props, context, or state management libraries to keep data flowing predictably. Even with these complexities, the benefits far outweigh the challenges. Codebases remain cleaner, interfaces grow more stable, and new features can be shipped more rapidly because developers avoid rewriting similar UI structures. This methodology represents a mature phase in frontend evolution, where reusability and structure drive both productivity and reliability.
                            </p>

                            <h3>Improving User Experience Through Content Presentation</h3>
                            <p>
                            User experience depends heavily on how content is presented. Even the most powerful features lose value if users struggle to understand or interact with them. Thoughtful content layout, especially with headings, paragraphs, spacing, and sectioning, gives users the ability to scan information quickly. Visual rhythm plays a key role here: consistent spacing, predictable sizing, and deliberate balance guide the eye and reduce cognitive fatigue. Modern UI frameworks help enforce these patterns, but ultimately it is the developer’s responsibility to ensure that content flows logically and remains easy to read.
                            </p>
                            <p>
                            Performance is another crucial element of user experience. Heavy pages filled with unnecessary scripts or overly complex layouts slow interactions and frustrate users. Instead, developers aim to optimize content delivery through techniques such as lazy loading, caching, and minimal DOM manipulation. Clean markup also contributes to performance gains because browsers can parse and render pages more efficiently. The combination of clarity, speed, and thoughtful design allows modern interfaces to meet the expectations of today’s digital audience. As technology continues to evolve, the balance between aesthetics and usability will remain a guiding principle in crafting exceptional user experiences.
                            </p>
                        `,
                        reddit_post: {
                            title: "React is awesome",
                            body: `Working on a new project and realizing how useful **checklists** can be.  
Here’s what I’m tracking:

- [x] *Plan features*
- [ ] **Write documentation**
- [ ] Add \`unit tests\`

> Tip: Break tasks into smaller chunks to stay motivated.

Also found this helpful guide: [Quick Start](https://example.com).
`
                        }
                    },
                    {
                        id: 2,
                        tweet: "Debugging is like being the detective in a crime movie where you are also the murderer. 🕵️‍♂️ #coding",
                        blog_post: "<p>Debugging strategies that saved my expected life. Just kidding, it saved my project.</p>",
                        reddit_post: {
                            title: "How to debug effectively?",
                            body: "Console logging is my best friend. But debuggers are better."
                        }
                    }
                ];
                setResults(mockData);
            }
            finally {
                setLoading(false)
            }
        }
        fetchResults();
    }, []);

    if (Loading) {
        return <div>Loading...</div>
    }

    return (
        <div className="relative text-white h-screen bg-slate-950">
            {/* --- Decorative glows in the background --- */}
            <div className="absolute top-[-200px] left-[-150px] w-[500px] h-[500px] rounded-full bg-purple-600/20 blur-[200px]" />
            <div className="absolute bottom-[-200px] right-[-150px] w-[500px] h-[500px] rounded-full bg-blue-600/20 blur-[200px]" />

            {/* --- Floating shapes --- */}
            <div className="absolute inset-0 pointer-events-none">
                <svg className="absolute top-20 right-32 opacity-20 animate-pulse delay-700" width="140" height="140">
                    <circle cx="70" cy="70" r="60" stroke="white" strokeWidth="0.2" fill="none" />
                </svg>
                <svg className="absolute bottom-40 left-10 opacity-10 animate-pulse delay-1000" width="120" height="120">
                    <rect x="10" y="10" width="100" height="100" stroke="white" strokeWidth="0.2" fill="none" />
                </svg>
            </div>

            {/* --- Scrollable Content Area --- */}
            <div className="absolute inset-0 overflow-y-auto z-10">
                <div className="max-w-4xl mx-auto p-6 pt-10 pb-20">
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-linear-to-r from-white to-gray-400 mb-8 tracking-tight">History</h1>

                    {Results && Results.length > 0 ? (
                        <div className="space-y-6">
                            {Results.map((result) => (
                                <PostCard key={result.id} post={result} />
                            ))}
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center py-20 opacity-70">
                            <div className="w-20 h-20 rounded-full bg-gray-800/50 flex items-center justify-center mb-4 border border-gray-700">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <h2 className="text-xl font-semibold text-gray-300">No History Found</h2>
                            <p className="text-gray-500 mt-2">Your generated content will appear here.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default History;