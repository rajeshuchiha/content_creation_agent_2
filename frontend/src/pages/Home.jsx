import { Link } from "react-router-dom";

function Home() {
    return (
        <div className="relative text-white overflow-hidden bg-slate-950">

            {/* --- Decorative glows in the background --- */}
            <div className="absolute top-[-200px] left-[-150px] w-[500px] h-[500px] rounded-full bg-purple-600/30 blur-[200px]" />
            <div className="absolute bottom-[-200px] right-[-150px] w-[500px] h-[500px] rounded-full bg-blue-600/30 blur-[200px]" />

            {/* --- Floating shapes --- */}
            <div className="absolute inset-0 pointer-events-none">
                <svg className="absolute top-20 right-32 opacity-30 animate-pulse delay-700" width="140" height="140">
                    <circle cx="70" cy="70" r="60" stroke="white" strokeWidth="0.2" fill="none" />
                </svg>
                <svg className="absolute bottom-20 left-20 opacity-20 animate-pulse delay-1000" width="120" height="120">
                    <rect x="10" y="10" width="100" height="100" stroke="white" strokeWidth="0.2" fill="none" />
                </svg>
            </div>


            <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 text-center">

                {/* Glass card with entrance animation */}
                <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl px-10 py-16 shadow-[0_0_40px_rgba(255,255,255,0.08)] max-w-3xl animate-in fade-in zoom-in duration-700 ease-out">

                    <h1 className="text-5xl md:text-6xl font-bold leading-tight bg-linear-to-r from-white to-neutral-400 bg-clip-text text-transparent animate-in slide-in-from-bottom-8 fade-in duration-700 delay-100 fill-mode-forwards">
                        Automate your social media
                    </h1>

                    <p className="text-neutral-300 mt-6 text-lg max-w-xl mx-auto leading-relaxed animate-in slide-in-from-bottom-4 fade-in duration-700 delay-200 fill-mode-forwards">
                        Save hours every week using intelligent automation.
                        Publish, analyze and grow — without doing the repetitive work.
                    </p>

                    {/* buttons */}
                    <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center animate-in slide-in-from-bottom-4 fade-in duration-700 delay-300 fill-mode-forwards">
                        <Link
                            to="/register"
                            className="px-8 py-3 rounded-full bg-linear-to-r from-purple-500 to-blue-500 text-white font-semibold shadow-lg hover:opacity-90 hover:scale-105 transition active:scale-95"
                        >
                            Get Started
                        </Link>

                        <button className="px-8 py-3 rounded-full border border-neutral-700 text-neutral-300 hover:border-neutral-500 hover:bg-white/5 transition active:scale-95">
                            Learn More
                        </button>
                    </div>
                </div>

                {/* Subtle bottom text / Trused by */}
                <div className="mt-12 flex flex-col items-center animate-in fade-in duration-1000 delay-500">
                    <p className="text-neutral-500 text-sm mb-4">
                        Trusted by creators, agencies and businesses worldwide
                    </p>
                    <div className="flex gap-4 opacity-50">
                        {[1, 2, 3, 4].map((i) => (
                            <div key={i} className="w-8 h-8 rounded-full bg-white/20" />
                        ))}
                    </div>
                </div>
            </div>

            {/* --- Animated lines background --- */}
            <div className="absolute inset-0 opacity-[0.08] pointer-events-none">
                <svg width="100%" height="100%">
                    <defs>
                        <pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse">
                            <path d="M 80 0 L 0 0 0 80" fill="none" stroke="white" strokeWidth="0.5" />
                        </pattern>
                    </defs>
                    <rect width="100%" height="100%" fill="url(#grid)" />
                </svg>
            </div>
        </div>
    );
};

export default Home;