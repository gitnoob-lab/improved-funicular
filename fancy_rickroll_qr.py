import qrcode
import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from qrcode.constants import ERROR_CORRECT_H

# Constants
WEBSITE_LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
OUTPUT_FILE = "fancy_rickroll_qr.png"
LOGO_PATH = "rick_logo.png"

def create_circular_logo(logo_path, size):
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.resize((size, size))
    

    # Create a circular mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    circular_logo = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    circular_logo.paste(logo, (0, 0), mask)

    border_size = size + 8  # 4px border all around
    border_img = Image.new('RGBA', (border_size, border_size), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_img)
    border_draw.ellipse((0, 0, border_size, border_size), fill=(255, 255, 255, 230))
    border_img = border_img.filter(ImageFilter.GaussianBlur(2)) # Blur

    position = ((border_size - size) // 2, (border_size - size) // 2)
    border_img.paste(circular_logo, position, circular_logo)
    
    return border_img


def generate_qr_code_with_logo(data: str, logo_path: str, output_path: str):
    # Initialise with error correction for better scanning
    qr = qrcode.QRCode(
        version=1,  
        error_correction=ERROR_CORRECT_H,  # High error correction
        box_size=10, 
        border=4
    )
    qr.add_data(data)
    qr.make()
    
    # Rounded modules and a gradient
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=VerticalGradiantColorMask(
            top_color=(255, 0, 0),   # Red top
            bottom_color=(0, 0, 255) # Blue bottom
        )
    ).convert('RGBA')

    # Load logo
    try:
        

        qr_width, qr_height = img.size
        logo_size = min(qr_width, qr_height) // 5 # 1/5 of the QR code size

        circular_logo = create_circular_logo(logo_path, logo_size)
        border_size = logo_size + 8  # 4px border all around
        position = ((qr_width - border_size) // 2, (qr_height - border_size) // 2) # Center logo

        img.paste(circular_logo, position, circular_logo)


    except Exception as e:
        print(f"Error loading logo: {e}")
        import traceback
        traceback.print_exc()
        print("QR code generated without logo")

    # Save QR code image
    output_path = os.path.abspath(output_path)
    img.save(output_path)
    print(f"QR code saved to {output_path}")

if __name__ == "__main__":
    generate_qr_code_with_logo(WEBSITE_LINK, LOGO_PATH, OUTPUT_FILE)