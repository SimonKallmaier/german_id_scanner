import os

import boto3
import pandas as pd
import trp.trp2 as t2
from PIL import Image

from utils import image_loader

# Set AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Configure Boto3 client
TEXTRACT = boto3.client(
    "textract",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="eu-central-1",
)
print("Successfully configured Boto3 client.")


def extract_id_information(image: Image.Image):
    imageBytes = image_loader(image)
    # Call Textract
    response = TEXTRACT.analyze_document(
        Document={"Bytes": imageBytes},
        # new QUERIES Feature Type for Textract Queries
        # We could add additional Feature Types like FORMS and/or TABLES
        # FeatureTypes=["QUERIES", "FORMS", "TABLS"],
        FeatureTypes=["QUERIES", "FORMS"],
        QueriesConfig={
            "Queries": [
                {"Text": "What is the value below the Vornamen/Given names/ prenoms?", "Alias": "GIVEN_NAME"},
                {"Text": "What is the value below Name/Surname/Nom?", "Alias": "SURNAME"},
                {"Text": "What is the value for date of birth?", "Alias": "DATE_OF_BIRTH"},
                {"Text": "What is the Nationality?", "Alias": "NATIONALITY"},
                {"Text": "What is the date of expiry?", "Alias": "DATE_OF_EXPIRY"},
                {"Text": "What is the place of Birth?", "Alias": "PLACE_OF_BIRTH"},
                {"Text": "What is the ID Number on the header of the Document?", "Alias": "ID_NUMBER_TOP"},
                {"Text": "What is the Number on the bottom of the Document?", "Alias": "ID_NUMBER_BOTTOM"},
            ]
        },
    )

    d = t2.TDocumentSchema().load(response)
    page = d.pages[0]

    query_answers = d.get_query_answers(page=page)

    return pd.DataFrame(query_answers).rename(columns={0: "Question", 1: "Alias", 2: "Answer"})
