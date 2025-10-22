import { useState } from "react";
import { usePlatformContext } from "../context/platformContext";

function Platform({ name }) {

    const platform = name.toLowerCase();

    const { Platforms, togglePlatforms } = usePlatformContext();

    const enabled = Platforms[platform];

    return (
        <div>
            <span>{name}: </span>
            {enabled && <span>Enabled</span>}
            <button
                onClick={() => {togglePlatforms(platform)}}
                style={{ marginLeft: "8px" }}
            >
                {enabled ? "Disable" : "Enable"}
            </button>

        </div>
    );
}

export default Platform