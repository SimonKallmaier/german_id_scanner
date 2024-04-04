import streamlit as st
from PIL import Image

from aws import extract_id_information


def camera_uploader():
    image = st.camera_input("Take a photo")
    if image is not None:
        st.image(image, caption="Captured Image.", use_column_width=True)
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
    else:
        return camera_uploader()


def extract_information(image: Image.Image):
    if st.button("Extract Text"):
        extracted_text = extract_id_information(image)
        st.write("Extracted Text:", extracted_text)


def run():

    st.header("Document AI App")
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
