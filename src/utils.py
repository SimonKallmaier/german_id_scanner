import io

from PIL import Image


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
