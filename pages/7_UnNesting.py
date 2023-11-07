import streamlit as st
from utils.image_from_image import image_from_image, decodeImage
import os

st.set_page_config(
    page_title="Image Steganography",
    page_icon="🧊",
)

st.write("## UnNesting")

image = st.file_uploader("Enter image")

if image:
    st.write("You uploaded this image")
    st.image(image)

    if st.button("Decrypt"):
        # Store the image in a directory
        os.makedirs("uploaded_images", exist_ok=True)

        with open(os.path.join("uploaded_images", image.name), "wb") as f:
            f.write(image.getbuffer())

        st.write("Decrypting...")

        nested_img = image_from_image(f"uploaded_images/{image.name}")
        print("Decoded 1st img")
        nested_img = decodeImage(nested_img)
        print("Decoded 2nd img")
        nested_img = decodeImage(nested_img)
        print("Decoded 3rd img")
        decoded_text = decodeImage(nested_img)
        print("Decoded 4th img")

        st.success("Decrypted successfully")

        st.write("### Decrypted message:")
        st.write(f"#### {decoded_text}")
