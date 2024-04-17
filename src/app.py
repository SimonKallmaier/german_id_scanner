import os

import streamlit as st
from PIL import Image

from aws import extract_id_information
from salary_scanner import get_salary_information

st.session_state.user_authentificated = False


def user_authentification():
    """This function receives a users password and name from the environment variables."""
    st_user_name = st.text_input("User Name")
    st_user_password = st.text_input("Password", type="password")

    user_name = os.getenv("USER_NAME", "admin")
    password = os.getenv("PASSWORD", "admin")

    if st_user_name == user_name and st_user_password == password:
        st.write("User authenticated")
        st.session_state.user_authentificated = True


def camera_uploader():

    im_bytes = st.camera_input("Take a photo")
    if im_bytes is not None:
        st.image(im_bytes, caption="Captured Image.", use_column_width=True)
        image = Image.open(im_bytes)
        return image
    else:
        return None


def image_uploader():
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
        return image
    else:
        return None


def selector_image_or_camera():
    option = st.selectbox("Select an option", ["Image", "Camera"])
    if option == "Image":
        return image_uploader()
    else:  # Camerag
        st.warning("The resolution of the camera is limited. Please upload an image for better results.")
        return camera_uploader()


def extract_information(image: Image.Image):

    option = st.selectbox("Select an option", ["ID", "Salary"])
    if option == "ID":
        extract_func = extract_id_information

    else:
        extract_func = get_salary_information
        st.write("Not implemented yet.")

    if st.button("Extract Text"):
        extracted_text = extract_func(image)
        st.write("Extracted Text:", extracted_text)


def run():

    st.header("German ID Card Information Extraction")
    user_authentification()
    if not st.session_state.user_authentificated:
        st.write("User not authenticated. Please try again.")
    else:
        st.subheader("Upload an image or take a photo to extract information.")
        image = selector_image_or_camera()
        st.write("You can extract information from the image.")
        extract_information(image)


if __name__ == "__main__":
    run()
