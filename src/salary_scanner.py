import ast
import io

import boto3
import openai
from openai import OpenAI
from PIL import Image

client = OpenAI()
TEXTRACT_CLIENT = boto3.client("textract")


def get_completion(text: str):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": (
                    f"You are a helpful assistant that needs to check the salary statements and extract the income before taxes and the final amount that is paid to the employee for the month (not year). The statements are in German. You will get the raw text: RAW_TEXT: {text}"  # noqa E501
                    "The output should a dictionary with the keys 'AUSZAHLUNG' and 'BRUTTO' and the corresponding values as floats."  # noqa E501
                ),
            },
        ],
    )
    return completion.choices[0].message.content


def get_text_salary_information(image: Image.Image):
    imageBytes = io.BytesIO()
    image.save(imageBytes, format="JPEG")
    imageBytes = imageBytes.getvalue()
    # Call Textract
    response = TEXTRACT_CLIENT.detect_document_text(Document={"Bytes": imageBytes})
    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text += f"{item['Text']} "
    return text


def get_salary_information(img) -> dict:
    text = get_text_salary_information(img)
    salary_information = get_completion(text)
    return ast.literal_eval(salary_information)
