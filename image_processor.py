import os
import argparse
from PIL import Image
from PIL.Image import Resampling 
from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def resize_image(
    input_path: Annotated[str, typer.Argument(help="enter the path to the image file")],
    width: Annotated[int, typer.Option("--width", "-w", help="enter a width")] = None,
    height: Annotated[int, typer.Option("--height", "-h", help="enter a height")] = None
):
    with Image.open(input_path) as img:
        orig_width, orig_height = img.size

        if width and height:
            new_size = (width, height)
        elif width:
            ratio = width / orig_width
            new_size = (width, int(orig_height * ratio))
        elif height:
            ratio = height / orig_height
            new_size = (int(orig_width * ratio), height)
        else:
            print("At least one of width or height must be specified")
            raise typer.Exit(code=0)

        resized_img = img.resize(new_size, Resampling.LANCZOS)

        path_stem = Path(input_path).stem 
        path_width_height = f"{new_size[0]}x{new_size[1]}"
        path_suffix = Path(input_path).suffix
        output_path = f"{path_stem}-{path_width_height}{path_suffix}"
        
        resized_img.save(output_path)        

@app.command()
def format_image(input_path: str, extension: str = None):
    if not extension:
        print("No extension specified.")
        raise typer.Exit(code=0)

    extension = extension.lower()

    valid_ext = ("jpg", "jpeg", "png", "webp")
    if extension not in valid_ext:
        print("Invalid format. Choose from: jpg, jpeg, png, webp.")
        raise typer.Exit(code=0)

    # Normalize jpeg → jpg
    if extension == "jpeg":
        extension = "jpg"

    with Image.open(input_path) as img:
        pil_format = None 
        
        # Choose the correct PIL format
        if extension == "jpg":
            pil_format = "JPEG"
            img = img.convert("RGB")   # Required for JPEG
        elif extension == "png":
            pil_format = "PNG"
        elif extension == "webp":
            pil_format = "WEBP"

        output_path = f"{Path(input_path).stem}.{extension}"
        img.save(output_path, pil_format)

        print(f"Saved as {output_path}")


if __name__ == "__main__":
    app()