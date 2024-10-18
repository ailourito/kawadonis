import {
    Dialog,
    DialogPanel
} from "@headlessui/react";
import { useEffect, useState } from "react";
import whereisado from "../assets/whereisado.webp";
import errorAdonis from "../assets/error.gif"

interface DialogViewInterface {
    isOpen: boolean;
    setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
    isError: boolean;
    setIsError: React.Dispatch<React.SetStateAction<boolean>>;
    errorMessage: string;
}

const DialogView: React.FC<DialogViewInterface> = (
    { isOpen, setIsOpen, isError, setIsError, errorMessage },
) => {
    const [selImage, setSelImage] = useState<string>("");

    // Use useEffect to avoid setting state during render
    useEffect(() => {
        if (!isError) {
            setSelImage(whereisado);
        } else {
            setSelImage(errorAdonis);
        }
    }, [isError]);


    const closeErrorView = () => {
        setIsError(false);
        setIsOpen(false);
    }

    return (
        <div>
            <Dialog
                open={isOpen}
                onClose={closeErrorView}
                className="relative z-50"
            >
                <div className="fixed inset-0 flex w-screen items-center justify-center p-4 bg-gray-900/80">
                    <DialogPanel className="max-w-lg space-y-4 border bg-[#FAC6C9] p-2 rounded-xl">
                        <div className="text-gray-800 text-center py-2">
                            <h1 className="text-3xl font-bold text-gray-700">
                                {isError
                                    ? "🙈  Opppsieee"
                                    : "🔎  Searching for Spyros"}
                            </h1>
                        </div>

                        <div className="flex flex-col md:flex-row items-center p-6">
                            <div className="md:w-1/2">
                                <img
                                    src={selImage}
                                    alt="Status"
                                    className="rounded-lg w-full h-auto"
                                />
                            </div>

                            <div className="md:w-1/2 md:pl-6 mt-6 md:mt-0">
                                <p className="text-gray-700 text-lg">
                                    {!isError ? (
                                        <span>
                                            Our specially trained monkeys are
                                            looking for {' '}
                                            <span className="underline decoration-wavy decoration-green-600">
                                                Spyros
                                            </span>{' '}
                                            AKA {' '}
                                            <span className="underline decoration-wavy decoration-blue-600">
                                                Adonis Georgiadis 
                                            </span>{' '}
                                            AKA {' '}
                                            <span className="underline decoration-wavy decoration-red-900">
                                                "the govement"
                                            </span> {' '}
                                            to cheer him up!! Please wait a
                                            minute.
                                        </span>
                                    ) : (
                                        <span>{errorMessage} :&#40;</span>
                                    )}
                                </p>
                            </div>
                        </div>
                        {isError && (
                            <div className="flex w-full justify-end text-xl font-bold text-red-800">
                                <button onClick={closeErrorView}>
                                    Thank God (OK)!
                                </button>
                            </div>
                        )}
                    </DialogPanel>
                </div>
            </Dialog>
        </div>
    );
};

export default DialogView;
