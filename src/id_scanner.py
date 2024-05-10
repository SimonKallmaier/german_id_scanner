import ast

from utils import get_completion, get_text_information

print("Successfully configured Boto3 client.")


def cost_id_scanner():
    return 15 / 1000  # 0.015 USD per page


def extract_id_information(image):

    text = get_text_information(image)
    salary_information = get_completion(text, salary=False)
    return ast.literal_eval(salary_information)


# import os

# import pandas as pd
# import streamlit as st
# import trp.trp2 as t2
# from PIL import Image
# imageBytes = image_loader(image)

# response = TEXTRACT.detect_document_text(Document={"Bytes": imageBytes})

# # Call Textract
# response = TEXTRACT.analyze_document(
#     Document={"Bytes": imageBytes},
#     # new QUERIES Feature Type for Textract Queries
#     # We could add additional Feature Types like FORMS and/or TABLES
#     # FeatureTypes=["QUERIES", "FORMS", "TABLS"],
#     FeatureTypes=["QUERIES", "FORMS"],
#     QueriesConfig={
#         "Queries": [
#             {"Text": "What is the value below the Vornamen/Given names/ prenoms?", "Alias": "GIVEN_NAME"},
#             {"Text": "What is the value below Name/Surname/Nom?", "Alias": "SURNAME"},
#             {"Text": "What is the value for date of birth?", "Alias": "DATE_OF_BIRTH"},
#             {"Text": "What is the Nationality?", "Alias": "NATIONALITY"},
#             {"Text": "What is the date of expiry?", "Alias": "DATE_OF_EXPIRY"},
#             {"Text": "What is the place of Birth?", "Alias": "PLACE_OF_BIRTH"},
#             {"Text": "What is the ID Number on the header of the Document?", "Alias": "ID_NUMBER_TOP"},
#             {"Text": "What is the Number on the bottom of the Document?", "Alias": "ID_NUMBER_BOTTOM"},
#         ]
#     },
# )

# d = t2.TDocumentSchema().load(response)
# page = d.pages[0]

# query_answers = d.get_query_answers(page=page)

# costs = cost_id_scanner()
# st.write(f"Total cost: ${costs:.4f} USD")
# return pd.DataFrame(query_answers).rename(columns={0: "Question", 1: "Alias", 2: "Answer"})
