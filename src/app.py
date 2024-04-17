import os

import streamlit as st
from PIL import Image

from aws import extract_id_information
from salary_scanner import get_salary_information

st.set_page_config(layout="wide", page_title="AI Document Processing")

if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False


def user_authentication():
    """Authenticate user based on environment variables."""
    if not st.session_state.user_authenticated:
        st_user_name = st.text_input("User Name")
        st_user_password = st.text_input("Password", type="password")
        user_name = os.getenv("USER_NAME", "admin")
        password = os.getenv("PASSWORD", "admin")

        if st_user_name == user_name and st_user_password == password:
            st.session_state.user_authenticated = True
            st.experimental_rerun()


def camera_uploader():
    im_bytes = st.camera_input("Take a photo")
    if im_bytes:
        image = Image.open(im_bytes)
        return image
    return None


def image_uploader():
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        return image
    return None


def selector_image_or_camera():
    option = st.sidebar.selectbox("Select Input Method", ["Image", "Camera"])
    if option == "Image":
        return image_uploader()
    else:
        st.sidebar.warning("Camera resolution is limited. Please upload an image for better results.")
        return camera_uploader()


def run():
    st.header("German ID Card Information Extraction")
    user_authentication()
    if st.session_state.user_authenticated:
        st.subheader("Upload an image or take a photo to extract information.")
        image = selector_image_or_camera()
        if image:
            option = st.sidebar.selectbox("Select Information to Extract", ["ID", "Salary"])
            extract_func = extract_id_information if option == "ID" else get_salary_information

            col1, col2 = st.columns(2)
            col1.image(image, caption="Processed Image", use_column_width=True)

            if col2.button("Extract Text"):
                extracted_text = extract_func(image)
                if isinstance(extracted_text, dict):
                    col2.json(extracted_text)
                else:
                    # st.write("Extracted Text:", extracted_text)
                    col2.write("Extracted Text:")
                    col2.write(extracted_text)
    else:
        st.write("User not authenticated. Please log in to continue.")


if __name__ == "__main__":
    run()
