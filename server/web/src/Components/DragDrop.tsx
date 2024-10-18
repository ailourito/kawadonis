import { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import ReactGA from "react-ga4";
import loadingBack from "../assets/dragBackground.webp";
import background from "../assets/background.webp";
import kawaiidemo from "../assets/kawaii-demo.webp";
import Sadonis from "./Sadonis";
import axios from "axios";
import ImageView from "./ImageView";
import DialogView from "./DialogView";
import Plug from "./Plug";

const DragDrop: React.FC = () => {
  const [bgImage, setBgImage] = useState<string>(background);
  const [loading, setLoading] = useState<boolean>(false);
  const [isError, setIsError] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [imageResult, setImageResult] = useState<string>("");

  // Function to send POST request with the file
  const handlePostRequest = async (droppedFile: File | null) => {
    if (!droppedFile) return;


    ReactGA.event({
      category: "User Interaction",
      action: "Image Loaded",
      label: "image-drop",
    });

    setLoading(true);

    const formData = new FormData();
    formData.append("file", droppedFile);
    formData.append("fileSize", droppedFile.size.toString());
    formData.append("fileType", droppedFile.type);
    formData.append("base64_output", "true");

    try {
      const response = await axios.post(
        "/api/load-image",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );
      setLoading(false);
      if (response.status === 200) {
        setImageResult(response.data);
      }

    } catch (error: any) {
      setIsError(true);
      if (error.response) {
        setErrorMessage(error.response.data.detail || "An error occurred.");
      } else {
        setErrorMessage(
          "The monkeys f*ked up big time. No idea what are they doing.",
        );
      }
    }
  };

  // Handle image dropped
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const droppedFile = acceptedFiles[0];

    if (droppedFile) {
      handlePostRequest(droppedFile);
    }
  }, []);

  // Handle image pasted from clipboard
  const handlePaste = useCallback((event: ClipboardEvent) => {
    const items = Array.from(event.clipboardData?.items || []);
    setBgImage(loadingBack);
    for (const item of items) {
      if (item.type.startsWith("image/")) {
        const pastedFile = item.getAsFile();
        if (pastedFile) {
          handlePostRequest(pastedFile);
          setBgImage(background);
        }
      }
    }
  }, []);

  // Add global paste listener when component mounts
  useEffect(() => {
    const handlePasteEvent = (event: ClipboardEvent) => handlePaste(event);

    // Use the correct type for the event listener
    window.addEventListener("paste", handlePasteEvent as EventListener);

    // Cleanup the event listener when the component unmounts
    return () => {
      window.removeEventListener("paste", handlePasteEvent as EventListener);
    };
  }, [handlePaste]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    noClick: true,
  });
  const { getRootProps: getButtonProps, getInputProps: getButtonInputProps } =
    useDropzone({ onDrop });

  useEffect(() => {
    if (isDragActive) {
      setBgImage(loadingBack);
    } else {
      setBgImage(background);
    }
  }, [isDragActive]);

  return (
    <div
      {...getRootProps()}
      className="min-h-screen bg-center bg-cover bg-fixed"
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      <input {...getInputProps()} />

      <div className="flex flex-col  items-center justify-center">

        <div className="flex flex-col text-white items-center mx-5 my-2">
          <h1 className="text-3xl text-red-300">Kawaii-donis</h1>
          <h2 className="text-2xl text-red-300">(*＞ω＜*)</h2>
          <p className="text-xl text-red-200 m-2 text-center">Create a kawaii Adonis with a simple click and let ML do its magic! ✨</p>
        </div>


        <DialogView
          isOpen={loading}
          setIsOpen={setLoading}
          isError={isError}
          errorMessage={errorMessage}
          setIsError={setIsError}
        />

        {imageResult !== ""
          ? (
            // Image selected
            <div className="flex flex-row items-center justify-center w-full p-5">
              <ImageView
                imageResult={imageResult}
                setImageResult={setImageResult}
              />
            </div>
          )
          : (
            // No image picked yet
            <div className="flex flex-col-reverse md:flex-row items-center justify-center w-full">
              <div className="flex flex-row justify-center items-center w-3/4 md:w-1/2">
                <Sadonis />
              </div>

              <div className="flex flex-col justify-center p-5 items-center">
                {/* button click */}
                <div className="flex flex-row justify-center p-2 items-center md:mt-40">
                  <img
                    src={kawaiidemo}
                    alt="kawaiii democracy"
                    className="w-3/4"
                  >
                  </img>
                </div>
                <div {...getButtonProps()} className="w-fit">
                  <input {...getButtonInputProps()} />
                  <div className="mb-4">
                    <button
                      type="button"
                      className="p-2 border border-gray-300 rounded-3xl bg-red-300 text-2xl p-5 group hover:bg-red-100"
                    >
                      Upload Image of{" "}
                      <span className="group-hover:text-red-700 group-hover:underline decoration-wavy text-bold">
                        Adonis
                      </span>
                    </button>
                  </div>
                </div>

                <div className="flex flex-col text-rose-200 text-xl items-center">
                  <p>Drop or Paste</p>
                  <p>an Image</p>
                </div>
              </div>
            </div>
          )}
      </div>
          <Plug />
    </div>
  );
};

export default DragDrop;
