import os

import streamlit as st
from PIL import Image

from aws import extract_id_information

# """
# # TODO s
# 2. Make Upload function more pretty
# 3. change resolution of image
# """


def user_authentification():
    """This function receives a users password and name from the environment variables."""
    st.write("User Management")
    st_user_name = st.text_input("User Name")
    st_user_password = st.text_input("Password", type="password")

    user_name = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")

    if st_user_name == user_name and st_user_password == password:
        st.write("User authenticated")
        return True
    return False


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
    option = st.selectbox("Select an option", ["Camera", "Image"])
    if option == "Image":
        return image_uploader()
    else:
        return camera_uploader()


def extract_information(image: Image.Image):
    if st.button("Extract Text"):
        extracted_text = extract_id_information(image)
        st.write("Extracted Text:", extracted_text)


def run():

    st.header("Document AI App")

    is_valid_user = user_authentification()
    is_valid_user = True
    if not is_valid_user:
        st.write("User not authenticated. Please try again.")
    else:

        st.subheader("Upload an image or take a photo to extract information")
        st.write(
            "This app allows you to upload an image or take a photo using your camera. Once you have selected an image, you can extract information from it using the 'Extract Text' button."  # noqa E501
        )
        st.write("The extracted text will be displayed below the image.")
        image = selector_image_or_camera()
        st.write("You can extract information from the image.")
        extract_information(image)


if __name__ == "__main__":
    run()
