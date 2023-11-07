from skimage.io import imread
import bitarray
from utils.text_to_image import check_bit_size


def image_to_image(image_dest, image_src):
    print(image_src)
    print(image_dest)

    # reading both the images
    image_src = imread(image_src)
    image_dest = imread(image_dest)

    print(
        "Src Image is {} by {} by {}".format(
            *image_src.shape if len(image_src.shape) == 3 else image_src.shape + (1,)
        )
    )
    print("Dest Image is {} by {} by {}".format(*image_dest.shape))

    # encoding the image
    encoded_image = encodeImage(image_dest, image_src)

    print(image_dest[200][200])
    print(encoded_image[200][200])  # type:ignore

    return encoded_image


def imageToBits(img):
    try:
        channels = str(img.shape[2])
    except:
        channels = 1

    # basically this tag contains information about the image. It will be used to decode the image
    # contains info that, it is image, height, width, and number of channels
    tag = "{:<20}".format(f"img,{img.shape[0]},{img.shape[1]},{channels}")

    # convert tags to bits
    code = bitarray.bitarray()
    code.frombytes(tag.encode("utf-8"))
    tag = "".join(["1" if x == True else "0" for x in code.tolist()])

    # combine tag bits with image bits
    bits_strings = tag + "".join(["{0:08b}".format(x) for x in img.flatten().tolist()])

    return bits_strings


def messageToBits(message):
    # tag message (and paw w/ spaces till 20 characters)
    tag = "{:<20}".format("text," + str(len(message) * 8))
    message = tag + message
    # print("Tag", tag)

    # convert to bits
    code = bitarray.bitarray()
    code.frombytes(message.encode("utf-8"))
    code = "".join(["1" if x == True else "0" for x in code.tolist()])
    return code


def encodeImage(img, message):
    # print(message)
    if type(message) == str:
        code = messageToBits(message)
    else:
        # print("Image")
        code = imageToBits(message)

    # code = imageToBits(message)

    # print(img_dest.shape)

    if check_bit_size(img, code):
        shape = img.shape
        img = img.flatten()
        code = list(code)
        code_len = len(code)

        for i, x in enumerate(img):
            if i * 2 < code_len:
                zbits = list("{0:08b}".format(x))[:6] + code[i * 2 : i * 2 + 2]
                img[i] = int("".join(zbits), 2)
            else:
                return img.reshape(shape)

        return img.reshape(shape)
