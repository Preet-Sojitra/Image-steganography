import streamlit as st
from utils.text_to_image import check_bit_size
from utils.image_to_image import imageToBits, messageToBits, encodeImage
import os
from skimage.io import imsave, imread
from skimage.transform import rescale
import numpy as np

plans_img = imread(os.path.join("nesting", "Deathstar_blueprint.jpg"))
death_star_hd_img = imread(os.path.join("nesting", "death_star_HD.jpg"))
xwing_img = imread(os.path.join("nesting", "x-wing.jpg"))
r2d2_img = imread(os.path.join("nesting", "R2D2.jpg"))

r_xwing_img = r_xwing_img = (rescale(xwing_img, 0.95) * 255).astype(np.uint8)


st.set_page_config(
    page_title="Image Steganography",
    page_icon="🧊",
)

st.write("## Nesting")
text = st.text_area("Enter text")
isEncrytped = False

if st.button("Encrypt"):
    if text == "":
        st.error("Please enter text")
    else:
        if ~isEncrytped:
            st.write("Encrypting....")

        # First check space availale for all the sequence of nesting
        if (
            check_bit_size(death_star_hd_img, imageToBits(r_xwing_img))
            and check_bit_size(r_xwing_img, imageToBits(r2d2_img))
            and check_bit_size(r2d2_img, imageToBits(plans_img))
            and check_bit_size(plans_img, messageToBits(text))
        ):
            # st.write("Let's proceed")

            nested_img = encodeImage(plans_img, text)
            print("1st encode done")
            nested_img = encodeImage(r2d2_img, nested_img)
            print("2nd encode done")
            nested_img = encodeImage(r_xwing_img, nested_img)
            print("3rd encode done")
            nested_img = encodeImage(death_star_hd_img, nested_img)
            print("4th encode done")

            os.makedirs("encrypted_images", exist_ok=True)

            imsave("encrypted_images/nested.png", nested_img)

            isEncrytped = True

            if isEncrytped:
                st.success("Encrypted successfully")

                st.write("### Here's the encrypted image: ")
                st.image(nested_img)  # type: ignore
