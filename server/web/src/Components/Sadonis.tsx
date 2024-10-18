import React, { useState } from "react";
import sadonis from "../assets/sadonis.webp";
import kawaidonis from "../assets/kawaidonis.webp";
import arrow from "../assets/arrow.webp";

const Sadonis = () => {
    const [rotation, setRotation] = useState(0);
    const [currentImage, setCurrentImage] = useState(sadonis);

    const handleMouseOver = () => {
        if (rotation === 0) {
            setRotation(180); // Start rotating to 180 degrees
            setTimeout(() => {
                setCurrentImage(kawaidonis); // Switch to second image
                setRotation(360); // Continue rotating to 360 degrees
            }, 200); // Match this duration with your rotation duration
        }
    };

    const handleMouseLeave = () => {
        if (rotation === 360) {
            setRotation(180); // Start rotating back to 180 degrees
            setTimeout(() => {
                setCurrentImage(sadonis); // Switch back to first image
                setRotation(0); // Return to 0 degrees
            }, 200); // Match this duration with your rotation duration
        }
    };

    return (
        <div className="w-full">
            <div
                className="flex flex-row justify-center items-center"
                onMouseOver={handleMouseOver}
                onMouseLeave={handleMouseLeave} 
            >
                <img
                    src={currentImage}
                    alt="Spyros needs some attention"
                    className="transition-transform duration-200 transform" // Add blur on hover
                    style={{ transform: `rotate(${rotation}deg)` }}
                />
            </div>

            <div className="flex justify-center">
                <p className="text-rose-300 text-5xl">Hover!</p>
                <img
                    src={arrow}
                    alt="arrow"
                    height={100}
                    width={50}
                    className="animate-bounce ml-5"
                >
                </img>
            </div>
        </div>
    );
};

export default Sadonis;
