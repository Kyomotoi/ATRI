from pathlib import Path
from datetime import timedelta, date
from PIL import Image, ImageFont, ImageDraw


PLUGIN_DIR = Path(".") / "data" / "plugins" / "anti_effort"
TEMP_PATH = Path(".") / "data" / "temp"
PLUGIN_DIR.mkdir(parents=True, exist_ok=True)


def image_dealer(user_img: bytes, user_nickname: str, coding_time: str):
    user_p = str((TEMP_PATH / f"{user_nickname}-ae.png").absolute())

    with open(user_p, "wb") as w:
        w.write(user_img)

    bg_size = 1088, 2048
    bg = Image.new("RGBA", bg_size, color=(0, 0, 0, 0))

    xb_file = PLUGIN_DIR / "xb-bg-0.png"
    xb_frame = Image.open(xb_file).convert("RGBA")
    user_i = Image.open(user_p).convert("RGBA").resize((448, 448), Image.ANTIALIAS)

    _, _, _, a = xb_frame.split()

    today = date.today()
    yd = str(today - timedelta(days=1))

    font_file = str(PLUGIN_DIR / "hwxw.ttf")
    font_user_nickname = ImageFont.truetype(font_file, 60)
    font_coding_time = ImageFont.truetype(font_file, 100)
    font_date = ImageFont.truetype(font_file, 20)

    bg.paste(user_i, (351, 551))
    bg.paste(xb_frame, (0, 0), a)

    text_nick_size = font_user_nickname.getsize(user_nickname)
    text_nick_x = int((bg_size[0] - text_nick_size[0] + 68) / 2)

    text_time_size = font_coding_time.getsize(coding_time)
    text_time_x = int((bg_size[0] - text_time_size[0] + 68) / 2)

    img = ImageDraw.Draw(bg)
    img.text(
        (text_nick_x, 1076),
        user_nickname,
        font=font_user_nickname,
        fill=(255, 201, 72),
    )
    img.text(
        (text_time_x, 1564), coding_time, font=font_coding_time, fill=(255, 201, 72)
    )
    img.text((405, 1156), yd, font=font_date, fill=(255, 201, 72))

    bg.save(user_p)
    return user_p
