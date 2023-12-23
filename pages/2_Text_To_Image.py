import streamlit as st
from utils.text_to_image import encrypt_text_to_image
import os
from skimage.io import imsave

st.set_page_config(
    page_title="Image Steganography",
    page_icon="🧊",
)

st.write("## Encrypting Text into Image")
text = st.text_area("Enter text")

if text:
    image = st.file_uploader("Enter image")

    if image:
        st.write("You uploaded this image")
        st.image(image)

        if st.button("Submit"):
            # Store the image in a directory
            os.makedirs("uploaded_images", exist_ok=True)

            with open(os.path.join("uploaded_images", image.name), "wb") as f:
                f.write(image.getbuffer())

            # st.write("Encrypting...")

            encrypted_image = encrypt_text_to_image(
                text, f"uploaded_images/{image.name}"
            )

            if encrypted_image is None:
                st.error("Image is too small to fit the text")
            else:
                st.success("Encryption Done!")
                st.write("Here is the encrypted image")
                st.image(encrypted_image)  # type: ignore
                # print(type(encrypted_image))

                os.makedirs("encrypted_images", exist_ok=True)

                imsave(
                    f"encrypted_images/encrypted_{image.name.split('.')[0]}.png",
                    encrypted_image,
                )
