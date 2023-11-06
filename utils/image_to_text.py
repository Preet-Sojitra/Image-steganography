import bitarray
import streamlit as st
from skimage.io import imread


def image_to_text(image):
    print("Image to text")

    image = imread(image)

    decoded_message = decodeImage(image)
    return decoded_message


def decodeImage(img):
    print("Decode image")
    bit_message = ""
    bit_count = 0
    bit_length = 200
    for i, x in enumerate(img):
        for j, y in enumerate(x):
            for k, z in enumerate(y):
                # convert pixel value to 8 bit binary
                # print(z)
                zbits = "{0:08b}".format(z)
                # extract the last two bits
                bit_message += zbits[-2:]
                bit_count += 2
                """
                When we have first 80 bits. This means we have the tag and decoding the tag will give the actual length of the message.
                So we will replace the bit_length with the actual length of the message.
                """
                if bit_count == 80:
                    try:
                        decoded_tag = (
                            bitarray.bitarray(bit_message).tobytes().decode("utf-8")
                        )
                        bit_length = int(decoded_tag) + 80
                        bit_message = ""
                    except:
                        st.warning(
                            "Image does not have decode tag. Image is either not encoded or, at least, not encoded in a way this decoder recognizes"
                        )

                        print(
                            "Image does not have decode tag. Image is either not encoded or, at least, not encoded in a way this decoder recognizes"
                        )
                        return
                elif bit_count >= bit_length:
                    return bitarray.bitarray(bit_message).tobytes().decode("utf-8")
