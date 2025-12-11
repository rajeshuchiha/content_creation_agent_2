import { useState } from "react";
import { Check, X } from "lucide-react";
import { usePlatformContext } from "../context/platformContext";


function Platform({ name }) {

    const platform = name.toLowerCase();
    const { Platforms, togglePlatforms } = usePlatformContext();

    const enabled = Platforms[platform];

    return (
        <div className="group relative">
            {/* Glow effect on hover */}
            <div className={`absolute inset-0 rounded-xl blur-md transition-all duration-300 ${enabled
                ? 'bg-linear-to-r from-purple-600 to-blue-600 opacity-30 group-hover:opacity-50'
                : 'bg-gray-600 opacity-0 group-hover:opacity-20'
                }`} />

            {/* Main card */}
            <div className={`relative bg-gray-900/80 backdrop-blur-sm border rounded-xl px-5 py-3 transition-all duration-300 ${enabled
                ? 'border-purple-500/50 shadow-lg shadow-purple-500/20'
                : 'border-gray-700 hover:border-gray-600'
                }`}>
                <div className="flex items-center justify-between gap-4">
                    {/* Platform name with icon */}
                    <div className="flex items-center gap-3">
                        <span className="font-semibold text-white">{name}</span>
                    </div>

                    {/* Status indicator and button */}
                    <div className="flex items-center gap-3">
                        {/* Status badge */}
                        <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all duration-300 ${enabled
                            ? 'bg-green-600/20 text-green-400 border border-green-600/30'
                            : 'bg-gray-700/30 text-gray-400 border border-gray-600/30'
                            }`}>
                            {enabled ? (
                                <>
                                    <Check className="w-3 h-3" />
                                    <span>Active</span>
                                </>
                            ) : (

                                <>
                                    <X className="w-3 h-3" />
                                    <span>Inactive</span>
                                    {/* <span>{Loading ? "Deactivating...": "Inactive"}</span> */}
                                </>
                            )}
                        </div>

                        {/* Toggle button */}
                        <button
                            onClick={() => togglePlatforms(platform)}
                            className={`px-4 py-2 rounded-lg font-medium text-sm transition-all duration-300 cursor-pointer ${enabled
                                ? 'bg-gray-700/50 text-gray-300 hover:bg-gray-700 hover:text-white border border-gray-600/50 hover:border-gray-500'
                                : 'bg-linear-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700 shadow-md hover:shadow-lg hover:scale-105 active:scale-95'
                                }`}
                        >
                            {enabled ? "Disable" : "Enable"}
                        </button>

                    </div>
                </div>
            </div>
        </div>

    );
}

export default Platform