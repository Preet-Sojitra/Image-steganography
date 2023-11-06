# streamlit
import streamlit as st

st.set_page_config(
    page_title="Image Steganography",
    page_icon="🧊",
)


def Image_into_image():
    st.title("Image into Image")
    st.write("Enter image")
    image = st.file_uploader("Enter image", key="image")
    st.write("Enter image")
    image1 = st.file_uploader("Enter image", key="image1")
    if st.button("Submit"):
        st.write("Submitted")


st.write("# Image Steganography")
st.markdown(
    """
    ## What is Steganography?
    
    Steganography is the practice of concealing a file, message, image, or video within another file, message, image, or video. The word steganography comes from Greek steganographia, which combines the words steganós, meaning "covered or concealed", and -graphia meaning "writing".
    
    ## What is Image Steganography?
    
    Image Steganography is the process of hiding secret data in some image. The secret data is embedded in the image in such a way that no one can know the presence of the data in the image.
    
    ## How to use this app?
    
    This app is divided into two parts:
    
    1. Encrypting text into image
    2. Encrypting image into image
    
    Select the option from the sidebar to move to the respective section.
    
    Then, upload the image and the text to be encrypted. Click on the submit button to encrypt the data.
    """
)
