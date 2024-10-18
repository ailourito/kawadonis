import React from "react";
import ReactGA from "react-ga4";

interface ImageViewProps {
    imageResult: string;
    setImageResult: React.Dispatch<React.SetStateAction<string>>;
}

const ImageView: React.FC<ImageViewProps> = (
    { imageResult, setImageResult },
) => {

    const buttonClicked = (action: string) => {
        ReactGA.event({
            category: "User Interaction",
            action: "Clicked Button",
            label: action, 
          });
    }

    const downloadedImage = () => {
        buttonClicked("Image Download")
    }

    const newImage = () => {
        setImageResult("")
        buttonClicked("New Image")

    }

    return (
        <div className="flex flex-col items-center justify-center w-full">
            <img
                src={imageResult}
                alt="kawaii-adonis"
                className="p-2 rounded-xl max-w-[75vw] max-h-[75vh] object-contain"
                style={{
                    backgroundColor: "#FAACA8",
                    backgroundImage:
                        "linear-gradient(19deg, #FAACA8 0%, #DDD6F3 100%)",
                }}
            >
            </img>

            <div className="flex flex-col md:flex-row w-full items-center justify-center my-2 md:my-5">
                <a
                    className="border border-gray-300 rounded-3xl bg-red-200 text-xl py-2 px-5 mb-5 md:mr-5 hover:bg-red-300"
                    href={imageResult}
                    download="kawaii-donis.jpg"
                    onClick={downloadedImage}
                >
                    Download Image
                </a>

                <button
                    type="button"
                    onClick={newImage}
                    className="border border-gray-300 rounded-3xl bg-red-200 text-xl py-2 px-12 md:ml-5 hover:bg-red-300"
                >
                    Start Over
                </button>
            </div>
        </div>
    );
};

export default ImageView;
