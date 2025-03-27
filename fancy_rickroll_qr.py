import qrcode
import os
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
# Use a different colormask that's definitely available
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from qrcode.constants import ERROR_CORRECT_H

# Constants
WEBSITE_LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
OUTPUT_FILE = "fancy_rickroll_qr.png"

def generate_qr_code(data: str, output_path: str):
    # Initialize QR code with error correction for better scanning
    qr = qrcode.QRCode(
        version=1,  
        error_correction=ERROR_CORRECT_H,  # High error correction
        box_size=10, 
        border=4
    )
    qr.add_data(data)
    qr.make()
    
    # Create stylish QR code with rounded modules and a gradient
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=VerticalGradiantColorMask(
            top_color=(255, 0, 0),   # Red top
            bottom_color=(0, 0, 255) # Blue bottom
        )
    )
    
    # Save QR code image
    output_path = os.path.abspath(output_path)
    img.save(output_path)
    print(f"QR code saved to {output_path}")

if __name__ == "__main__":
    generate_qr_code(WEBSITE_LINK, OUTPUT_FILE)