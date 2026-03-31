import argparse
import os
import stepic
from PIL import Image

def process_steganography():
    parser = argparse.ArgumentParser(description="LSB Image Steganography Tool")
    
    # Subcommands: encode or decode
    subparsers = parser.add_subparsers(dest="mode", help="Choose to 'encode' or 'decode'")

    # Setup 'encode' arguments
    encode_parser = subparsers.add_parser("encode", help="Hide a message in an image")
    encode_parser.add_argument("-i", "--image", required=True, help="Path to source image")
    encode_parser.add_argument("-m", "--message", required=True, help="The secret message to hide")
    encode_parser.add_argument("-o", "--output", default="encoded_image.png", help="Output filename (default: encoded_image.png)")

    # Setup 'decode' arguments
    decode_parser = subparsers.add_parser("decode", help="Reveal a message from an image")
    decode_parser.add_argument("-i", "--image", required=True, help="Path to the image containing a message")

    args = parser.parse_args()

    if args.mode == "encode":
        if not os.path.exists(args.image):
            print(f"Error: File '{args.image}' not found.")
            return

        try:
            img = Image.open(args.image)
            # Stepic requires bytes for the message
            encoded_img = stepic.encode(img, args.message.encode('utf-8'))
            encoded_img.save(args.output)
            print(f"[*] Message successfully hidden in: {args.output}")
        except Exception as e:
            print(f"[-] Encoding failed: {e}")

    elif args.mode == "decode":
        if not os.path.exists(args.image):
            print(f"Error: File '{args.image}' not found.")
            return

        try:
            img = Image.open(args.image)
            decoded_message = stepic.decode(img)
            print(f"[*] Decoded Message: {decoded_message}")
        except Exception as e:
            print(f"[-] Decoding failed: {e}")
            
    else:
        parser.print_help()

if __name__ == "__main__":
    process_steganography()
