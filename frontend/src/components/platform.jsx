import { useState } from "react";
import { usePlatformContext } from "../context/platformContext";

import { Button } from "./ui/button";

function Platform({ name }) {

    const platform = name.toLowerCase();

    const { Platforms, togglePlatforms } = usePlatformContext();

    const enabled = Platforms[platform];

    return (
        <div className="flex justify-end">
            <span>{name}: </span>
            {enabled && <span>Enabled</span>}
            <Button
                onClick={() => {togglePlatforms(platform)}}
                style={{ marginLeft: "18px" }}
                className="bg-primary hover:bg-primary/90 text-sm text-primary-foreground 
                    whitespace-nowrap transition-all disabled:pointer-events-none disabled:opacity-50 cursor-pointer"
            >
                {enabled ? "Disable" : "Enable"}
            </Button>

        </div>
    );
}

export default Platform