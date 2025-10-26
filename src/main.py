import logging
import os
import shutil
import uuid

import boto3
from fastapi import FastAPI, File, HTTPException, UploadFile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

BUCKET_NAME = os.getenv("BUCKET_NAME", "test-jpgc-aws-developer")

# Create a boto3 session using a specific profile
boto_session = boto3.Session(profile_name="jean-dev")

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "OK"}


@app.post("/uploadimage")
async def upload_image(
    file: UploadFile = File(
        ...
    ),  # Suspensive dots -> Field(...) meaning that is required
):
    """Endpoint to upload a file into the server
    Args:
        file: required file to save it
    Headers:
        Content-Type: must be equal to multipart/form-data
    """
    try:
        dir_path = os.path.realpath(__file__).replace(
            "/main.py", ""
        )  # Using to get root dir of main.py module
        with open(f"{dir_path}/domain/resources/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        unique_name = uuid.uuid4()
        s3_client = boto_session.client("s3")
        s3_client.upload_file(
            f"{dir_path}/domain/resources/{file.filename}",
            BUCKET_NAME,
            str(unique_name) + ".png",
        )
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(f"{dir_path}/domain/resources/{file.filename}")
        return {
            "id": unique_name,
            "name": file.filename,  # Original file name, provisionally
        }


@app.get("/imagetotext")
def imagetotext(id: str):
    """Endpoint to process image and return text extracted

    Args:
        id (str): id of the image to process

    Returns:
        str | None: text extracted from image
    """
    try:
        file_name = f"{id}.png"
        logger.info(f"Processing image with id: {file_name}")
        textract_client = boto_session.client("textract", region_name="us-east-1")
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": BUCKET_NAME,
                    "Name": file_name,
                },
            }
        )
        print(response)
        text = ""
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                logger.info(f"Detected line: {item['Text']}")
                text += item["Text"] + "\n"
        return {"text": None if text == "" else text}
    except Exception as e:
        logger.error(f"Error processing image to text: {e}")
        raise HTTPException(status_code=500, detail=str(e))
