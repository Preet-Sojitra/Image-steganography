import bitarray
import streamlit as st
import numpy as np
from skimage.io import imread


def image_from_image(img):
    # print(img)
    # read the image
    img = imread(img)
    # print(type(img))
    # print(img)
    decoded_image = decodeImage(img)

    return decoded_image


def decodeImage(img):
    # print(img.shape)
    bit_message = ""
    bit_count = 0
    bit_length = 200
    grey = len(img.shape) == 2
    # print("Grey", grey)
    message_type = ""

    for i, x in enumerate(img):
        for j, y in enumerate(x):
            if grey:
                y = [y]
            for k, z in enumerate(y):
                zbits = "{0:08b}".format(z)
                bit_message += zbits[-2:]
                bit_count += 2
                if bit_count == 160:
                    try:
                        decoded_tag = (
                            bitarray.bitarray(bit_message)
                            .tobytes()
                            .decode("utf-8")
                            .split(",")
                        )
                        message_type = decoded_tag[0]
                        if message_type == "text":
                            bit_length = int(decoded_tag[1]) + 160
                            bit_message = ""
                        else:
                            bit_length = (
                                int(decoded_tag[1])
                                * int(decoded_tag[2])
                                * int(decoded_tag[3])
                                * 8
                            ) + 160

                    except:
                        st.error(
                            "Image does not have decode tag. Image is either not encoded or, at least, not encoded in a way this decoder recognizes"
                        )

                        print(
                            "Image does not have decode tag. Image is either not encoded or, at least, not encoded in a way this decoder recognizes"
                        )
                        return
                elif bit_count >= bit_length:
                    if message_type == "text":
                        return bitarray.bitarray(bit_message).tobytes().decode("utf-8")
                    else:
                        return bitsToImage(bit_message)


def bitsToImage(bits_string):
    try:
        tag = bits_string[:160]  # extract 20 bytes i.e. 160 bits
        tag = (
            bitarray.bitarray(tag).tobytes().decode("utf-8")
        )  # convert to bytes and then to string
        tag = tag.split(
            ","
        )  # split the string to get the info about the image (Since we tagged the image with img, height, width, and number of channels. We will use "," to split the string)
        image_bits = bits_string[
            160:
        ]  # extract the rest of the bits (i.e. the image bits)
        h = int(tag[1])  # height of the image
        w = int(tag[2])  # width of the image
        c = int(tag[3])  # number of channels in the image
        image_bits = np.asarray(
            [int(image_bits[i : i + 8], 2) for i in range(0, len(image_bits), 8)]
        )  # convert the image bits to array of integers (each integer is 8 bits long)

        if c == 1:
            image_bits = image_bits.reshape([h, w])
        else:
            image_bits = image_bits.reshape([h, w, c])

        return image_bits.astype(np.uint8)
    except:
        print("Not a string of image bits")
        st.warning("Not a string of image bits")
