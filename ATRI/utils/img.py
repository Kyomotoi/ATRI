import os
from PIL import ImageFile, Image

from ATRI.exceptions import WriteError


def compress_image(out_file, kb=500, quality=85, k=0.9) -> str:
    """将目标图片进行压缩"""
    o_size = os.path.getsize(out_file) // 1024
    if o_size <= kb:
        return out_file
    
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # type: ignore
    while o_size > kb:
        img = Image.open(out_file)
        x, y = img.size
        out = img.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
        try:
            out.save(out_file, quality=quality)
        except WriteError:
            raise WriteError('Writing file failed!')
        o_size = os.path.getsize(out_file) // 1024
    return out_file
