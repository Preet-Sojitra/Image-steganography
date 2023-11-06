import bitarray
import streamlit as st
from skimage.io import imread


def encrypt_text_to_image(text, image):
    # print(image)
    # print("Encrypting Text into Image")

    # convert text to bits
    message_bits = text_to_bits(text)
    # print(message_bits)

    # read the image
    image = imread(image)

    # check bit size and image size
    will_fit = check_bit_size(message_bits, image)

    if will_fit:
        # encode the message into the image
        return encodeImage(image, message_bits)


def text_to_bits(text):
    # tag message (and paw w/ spaces till 10 characters)
    # print(len(message)*8)  # prints the length of the message
    # tag is basically the length of the message in bits. It helps us to know when to stop decoding
    tag = "{:<10}".format(str(len(text) * 8))
    # print(tag)
    message = tag + text
    # print(message)

    # convert to bits
    bits = bitarray.bitarray()  # creates empty bit array
    bits.frombytes(message.encode("utf-8"))  # converts the message to bits
    # print(code)
    # print(code.tolist()) # converts bitarray to array of bits
    bits = "".join(
        ["1" if x == True else "0" for x in bits.tolist()]
    )  # converts bitarray to bitsting
    # print(code)
    return bits


def check_bit_size(img, message_bits):
    h = img.shape[0]
    w = img.shape[1]
    try:
        c = img.shape[2]
    except:
        c = 1

    img_max_size = h * w * c * 2
    string_size = len(message_bits)

    st.write(
        f"Message is {string_size/8000} KB and image can fit {img_max_size / 8000} KB of data"
    )

    # print(
    #     f"Message is {string_size/8000} KB and image can fit {img_max_size / 8000} KB of data"
    # )

    if string_size > img_max_size:
        st.warning(
            "Message is too big to be encoded in image. Try another image or message"
        )
        # print("Message is too big to be encoded in image")
        return False
    else:
        st.write("Image can be encoded with message. Proceed")
        # print("Image can be encoded with message. Proceed")
        return True


def encodeImage(img, message_bits):
    shape = img.shape
    img = img.flatten()
    message_bits = list(message_bits)
    # print(message_bits[:5])
    message_bits_len = len(message_bits)
    # print("Length of message bits: ", message_bits_len)

    for i, x in enumerate(img):
        # print(x)
        if i * 2 < message_bits_len:
            """
            Since image pixel value (x) is in decimal, we need to convert it to binary. So we use format method to convert it to 8 bit binary. This is done by using {0:08b} in the format method. 0 is the index of the value to be formatted. 08b means 8 bit binary.
            Then we will take first 6 bits of that binary using [:6] and to that we will append the two bits from our binary script.
            So zbits will be 8 bits long.
            """
            zbits = list("{0:08b}".format(x))[:6] + message_bits[i * 2 : i * 2 + 2]
            # print(zbits)

            # convert each item of zbit to string
            # zbits = [str(x) for x in zbits]

            """
            Now we have 8 bits. We need to convert it back to decimal. So we use int function with base 2. 
            
            But before converting, we have zbits as in array. So first we need to join it. Then we will convert it to decimal.
            
            And and that integer will be replaced with the original pixel value.
            """

            img[i] = int("".join(zbits), 2)
        else:
            return img.reshape(shape)

    # since we have flattened the img, we need to convert it back to original shape
    return img.reshape(shape)
