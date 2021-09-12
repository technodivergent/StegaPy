import numpy as np
from PIL import Image
import argparse

# define a delimiter to identify the end of the message
delim = "$73G4PY"

class StegaPyImage:
    def __init__(self, path):
        # Import the image, define the image's dimensions and convert image to a numpy array
        img = Image.open(path, 'r')
        self.mode = img.mode
        self.width, self.height = img.size
        self.array = np.array(list(img.getdata()))
        
        # Determine the pixel depth of image.
        # RGB = 3x8-bit (Red, Green, Blue)
        # RGBA = 4x8-bit (Red, Green, Blue, Alpha)
        if img.mode == 'RGB':
            self.dimension = 3
        elif img.mode == 'RGBA':
            self.dimension = 4

        # Define total number of pixels to be used for iteration
        self.totalPixels = self.array.size//self.dimension

def encode(source: str, message: str, destination: str) -> str:
    # Create a StegaPyImage object from the source image
    img = StegaPyImage(source)

    # Add a delimiter so we know when message ends, then
    # Convert it to binary, then
    # Calculate required pixels for new steganographized image
    message += delim
    binMessage = ''.join([format(ord(i), "08b") for i in message])
    requiredPixels = len(binMessage)

    # Throw an exception if the new image exceeds the dimensions of the original image
    # Otherwise, inject the message into the image array
    if requiredPixels > img.totalPixels:
        raise ValueError('The encoded image requires more pixels than the source image')
    else:
        # Inject message into image array
        imgArray = inject_message(img, requiredPixels, binMessage)

        # Convert array back to image and save as specified file
        encodedImage = Image.fromarray(imgArray.astype('uint8'), img.mode)
        encodedImage.save(destination)
        print("Image successfully saved")

def inject_message(img: StegaPyImage, requiredPixels: int, message: str) -> StegaPyImage:
    i = 0
    for p in range(img.totalPixels):
        for q in range(0, 3):
            if i < requiredPixels:
                img.array[p][q] = int(bin(img.array[p][q])[2:9] + message[i], 2)
                i += 1
    imgArray = img.array.reshape(img.height, img.width, img.dimension)
    return imgArray

def getInjectedBits(img: StegaPyImage) -> list:
    stegBits = ""
    for p in range(img.totalPixels):
        for q in range(0, 3):
            stegBits += (bin(img.array[p][q])[2:][-1])

    stegBits = [stegBits[i:i+8] for i in range(0, len(stegBits), 8)]
    return stegBits

def getMessage(img: StegaPyImage) -> str:
    stegBits = getInjectedBits(img)
    message = ""
    for i in range(len(stegBits)):
        if message[-7:] == delim:
            break
        else:
            message += chr(int(stegBits[i], 2))

    if delim in message:
        message = "Hidden message: " + message[:-7]
    else:
        message = "No hidden message found"
    return message

def decode(source: str) -> str:
    # Create a StegaPyImage object from the source image
    img = StegaPyImage(source)
    message = getMessage(img)
    return message

def main():
    argp = argparse.ArgumentParser(description='Determine the difference between two dates.')
    argp.add_argument('-e', '--encode', default=False, action="store_true", help='Use in conjunction with -s to ENCODE a file')
    argp.add_argument('-d', '--decode', default=False, action="store_true", help='Use in conjunction with -s to DECODE a file')

    argp.add_argument('-s', '--source', metavar='SOURCE_FILE', default='',
                        help='Use this to specify the file to be encoded/decoded')
    argp.add_argument('-m', '--message', metavar='MESSAGE', default='',
                        help='Enter a message inside quotes to encode')
    argp.add_argument('-o', '--output', metavar='OUTPUT_FILE', default='',
                        help='Enter the destination file name')
    args = argp.parse_args()

    if args.encode:
        encode(args.source, args.message, args.output)
    elif args.decode:
        message = decode(args.source)
        print(message)
    else:
        raise argparse.ArgumentError()

if __name__ == '__main__':
    main()