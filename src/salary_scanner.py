import ast
import io

import boto3
import openai
from openai import OpenAI
from PIL import Image

client = OpenAI()
TEXTRACT_CLIENT = boto3.client("textract")


_OUTPUT = """{{
    "AUSZAHLUNG": float,
    "BRUTTO": float,
    "DATUM": str,
    "SteuerID": str,
    "SV Nummer": str,
}}"""

_FIELDS = {
    "AUSZAHLUNG": "Der finale Auszahlungsbetrag, den der Mitarbeiter für den Monat erhält.",
    "BRUTTO": "Das Einkommen vor Steuern.",
    "DATUM": "Das Datum des Gehaltsdokuments.",
    "SteuerID": "Die Steueridentifikationsnummer des Mitarbeiters.",
    "SV Nummer": "Die Sozialversicherungsnummer des Mitarbeiters.",
}


def get_completion(text: str):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": (
                    f"You are a helpful assistant that needs to extraction certain information from a German salary statement. You will get a dictionary with the required information as keys and description as corresponding value."  # noqa E501
                    f" Required information: {_FIELDS}."
                    " RAW_TEXT_START:\n {text} \n RAW_TEXT_END"
                    f" The output should a dictionary with this format: {_OUTPUT}"  # noqa E501
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
