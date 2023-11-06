import streamlit as st
from utils.image_to_text import image_to_text
import os
from skimage.io import imsave

st.set_page_config(
    page_title="Image Steganography",
    page_icon="🧊",
)

st.write("## Decrypting Image into Text")

image = st.file_uploader("Enter image")

if image:
    st.write("You uploaded this image")
    st.image(image)

    if st.button("Decrypt"):
        # Store the image in a directory
        os.makedirs("uploaded_images", exist_ok=True)

        with open(os.path.join("uploaded_images", image.name), "wb") as f:
            f.write(image.getbuffer())

        # st.write("Decrypting...")

        decoded_message = image_to_text(f"uploaded_images/{image.name}")

        st.write("### Decrypted message:")
        st.write(f"#### {decoded_message}")
