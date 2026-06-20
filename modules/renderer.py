from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def create_frame(
    text,
    width=1080,
    height=1920
):

    img = Image.new(
        "RGB",
        (width, height),
        (0, 0, 0)
    )

    draw = ImageDraw.Draw(img)

    draw.text(
        (100, 900),
        text,
        fill="white"
    )

    return img
