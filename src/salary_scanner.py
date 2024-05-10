import ast

from utils import get_completion, get_text_information


def get_salary_information(img) -> dict:
    text = get_text_information(img)
    salary_information = get_completion(text)
    return ast.literal_eval(salary_information)
