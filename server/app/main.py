import io
import os
import re
import random
import base64
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from utils.adonizer import adonizer
from utils.utils import cleanup

app = FastAPI()

# Allow CORS for all origins (update for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/load-image")
async def load_image(
    file: UploadFile = File(...), 
    base64_output: str = Form(None)  
):
    image_path = None

    if not file:
        raise HTTPException(status_code=400, detail="No file sent")

    try:
        # Check if the uploaded file is an image
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail='The uploaded file is not an image.')

        # Read the uploaded image data
        image_data = await file.read()

        file_size_kb = len(image_data) / 1024  # Convert bytes to KB
        if not (int(file_size_kb) < 5 * 1024): 
            raise HTTPException(status_code=400, detail="Invalid image size! File size must be less than 5 MB.")

        # Load the image using PIL
        image = Image.open(BytesIO(image_data))

        # Handle the cases where the image could be PNG or WEBP
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image_path = f'temp/adonis{random.randint(0, 1000000)}.jpg'  # Temporarily save the image to disk
        image.save(image_path, format='JPEG')

        # Find waldonis
        result = adonizer(image_path)

        cleanup(image_path)

        # Adonis is not there
        if result is None:
            raise HTTPException(status_code=400, detail='We couldn\'t find Adonis. Are you sure it\' there?')
        
        if base64_output == "true":
            base64_image = base64.b64encode(result.getvalue()).decode('utf-8')
            base64_image_with_prefix = f"data:image/jpeg;base64,{base64_image}"
            return base64_image_with_prefix

        return StreamingResponse(result, media_type='image/jpeg')

    except Exception as e:
        cleanup(image_path)
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')
