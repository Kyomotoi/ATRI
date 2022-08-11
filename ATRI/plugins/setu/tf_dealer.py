import io
import re
import skimage
import skimage.io
import numpy as np
from PIL import Image
from pathlib import Path
from sys import getsizeof

import tensorflow as tf

from ATRI.log import logger as log
from ATRI.utils import request
from ATRI.exceptions import RequestError, WriteFileError


SETU_PATH = Path(".") / "data" / "plugins" / "setu"
TEMP_PATH = Path(".") / "data" / "temp"
SETU_PATH.mkdir(parents=True, exist_ok=True)
TEMP_PATH.mkdir(parents=True, exist_ok=True)


MODULE_URL = "https://jsd.imki.moe/gh/Kyomotoi/CDN@master/project/ATRI/nsfw.tflite"
VGG_MEAN = [104, 117, 123]


def prepare_image(img):
    H, W, _ = img.shape
    h, w = (224, 224)

    h_off = max((H - h) // 2, 0)
    w_off = max((W - w) // 2, 0)
    image = img[h_off : h_off + h, w_off : w_off + w, :]

    image = image[:, :, ::-1]

    image = image.astype(np.float32, copy=False)
    image = image * 255.0
    image = image - np.array(VGG_MEAN, dtype=np.float32)

    image = np.expand_dims(image, axis=0)
    return image


async def detect_image(url: str, file_size: int) -> list:
    try:
        req = await request.get(url)
    except Exception:
        raise RequestError("Get info from download image failed!")

    img_byte = getsizeof(req.read()) // 1024
    if img_byte < file_size:
        return [0, 0]

    try:
        pattern = r"-(.*?)\/"
        file_name = re.findall(pattern, url)[0]
        path = TEMP_PATH / f"{file_name}.jpg"
        with open(path, "wb") as f:
            f.write(req.read())
    except Exception:
        raise WriteFileError("Writing file failed!")

    await init_module()
    model_path = str((SETU_PATH / "nsfw.tflite").absolute())

    try:
        interpreter = tf.Interpreter(model_path=model_path)  # type: ignore
    except Exception:
        interpreter = tf.lite.Interpreter(model_path=model_path)

    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    im = Image.open(path)

    if im.mode != "RGB":
        im = im.convert("RGB")
    imr = im.resize((256, 256), resample=Image.BILINEAR)
    fh_im = io.BytesIO()
    imr.save(fh_im, format="JPEG")
    fh_im.seek(0)

    image = skimage.img_as_float32(skimage.io.imread(fh_im))

    final = prepare_image(image)
    interpreter.set_tensor(input_details[0]["index"], final)

    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])

    result = np.squeeze(output_data).tolist()
    return result


async def init_module():
    file_name = "nsfw.tflite"
    path = SETU_PATH / file_name
    if not path.is_file():
        log.warning("缺少模型文件，装载中")
        try:
            data = await request.get(MODULE_URL)
            with open(path, "wb") as w:
                w.write(data.read())
            log.info("模型装载完成")
        except Exception:
            log.error("装载模型失败")
