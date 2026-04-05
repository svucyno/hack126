"""
Image Processing Utility.

Handles background removal using rembg to create a transparent
cutout of the clothing item for the 2D figure.
"""
import os
from PIL import Image
try:
    from rembg import remove
    REMBG_AVAILABLE = True
except Exception:
    REMBG_AVAILABLE = False


def remove_background(input_path: str, output_path: str) -> str:
    """
    Remove background from the image at input_path using rembg.
    Saves the transparent image to output_path.
    
    Returns the output_path on success, or raises Exception on failure.
    """
    if not REMBG_AVAILABLE:
        raise ImportError("rembg is not installed. Background removal unavailable.")

    try:
        input_image = Image.open(input_path)
        # remove() handles PIL.Image in and out
        output_image = remove(input_image)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save as PNG to preserve transparency
        output_image.save(output_path, format="PNG")
        
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to remove background: {str(e)}") from e
