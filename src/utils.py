import io
import os

import boto3
from PIL import Image

# Set AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

TEXTRACT = boto3.client(
    "textract",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="eu-central-1",
)


def image_loader(image: Image.Image):
    imageBytes = io.BytesIO()
    try:
        print("Trying to save as JPEG")
        image.save(imageBytes, format="JPEG")
        imageBytes = imageBytes.getvalue()
    except OSError:
        print("Failed to save as JPEG, trying PNG")
        image.save(imageBytes, format="PNG")
        imageBytes = imageBytes.getvalue()

    if imageBytes is None:
        raise ValueError("Failed to load image.")

    return imageBytes


def get_text_information(image: Image.Image):
    imageBytes = image_loader(image)
    # Call Textract
    response = TEXTRACT.detect_document_text(Document={"Bytes": imageBytes})
    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text += f"{item['Text']} "
    return text
