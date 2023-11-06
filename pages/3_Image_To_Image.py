import streamlit as st
from utils.image_to_image import image_to_image
import os
from skimage.io import imsave, imread
import numpy as np
from PIL import Image

from utils.image_from_image import image_from_image, decodeImage

st.set_page_config(
    page_title="Image Steganography",
    page_icon="🧊",
)

st.write("## Encrypting Image into Image")

image_src = st.file_uploader("Enter image that you want to hide")

image_dest = st.file_uploader("Enter image in which you want to hide")

if image_src and image_dest:
    col1, col2 = st.columns(2)

    with col1:
        st.write("Image that you want to hide")
        st.image(image_src)

    with col2:
        st.write("Image in which you want to hide")
        st.image(image_dest)

    if st.button("Encrypt"):
        # Store the image in a directory
        os.makedirs("uploaded_images", exist_ok=True)

        # save the image to the directory
        for image in [image_src, image_dest]:
            with open(os.path.join("uploaded_images", image.name), "wb") as f:
                f.write(image.getbuffer())

        encoded_img = image_to_image(
            f"uploaded_images/{image_dest.name}", f"uploaded_images/{image_src.name}"
        )

        os.makedirs("encrypted_images", exist_ok=True)

        imsave(
            f"encrypted_images/encrypted_{image_dest.name.split('.')[0]}.png",
            encoded_img,
        )

        st.success("Image encrypted successfully")

        st.write("### Encrypted image:")
        st.image(f"encrypted_images/encrypted_{image_dest.name.split('.')[0]}.png")
