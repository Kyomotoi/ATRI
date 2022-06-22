from random import choice
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageFont, ImageDraw


POLAROID_DIR = Path(".") / "data" / "plugins" / "polaroid"
TEMP_PATH = Path(".") / "data" / "temp"
POLAROID_DIR.mkdir(exist_ok=True)


def image_dealer(user_img: bytes, user_id):
    user_p = str((TEMP_PATH / f"{user_id}.png").absolute())

    with open(user_p, "wb") as w:
        w.write(user_img)

    bg = Image.new("RGBA", (689, 1097), color=(0, 0, 0, 0))

    pol_frame = Image.open(POLAROID_DIR / f"frame-{choice([0, 1])}.PNG").convert("RGBA")
    user = Image.open(user_p).convert("RGBA").resize((800, 800), Image.ANTIALIAS)

    _, _, _, a = pol_frame.split()

    f_path = str(POLAROID_DIR / "font-0.ttf")
    f_date = ImageFont.truetype(f_path, 100)  # type: ignore
    f_msg = ImageFont.truetype(f_path, 110)  # type: ignore

    bg.paste(user, (0, 53))
    bg.paste(pol_frame, (0, 0), a)

    msg = f"今天辛苦了{choice(['！', '❤️', '✨'])}"
    now = datetime.now().strftime("%m / %d")

    img = ImageDraw.Draw(bg)
    img.text((25, 805), now, font=f_date, fill=(99, 184, 255))
    img.text(
        (15, 915),
        msg,
        font=f_msg,
        fill=(255, 100, 97),
    )

    bg.save(user_p)
    return user_p
