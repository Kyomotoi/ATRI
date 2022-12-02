import io
import re
import skimage
import onnxruntime
import numpy as np
from PIL import Image
from pathlib import Path
from sys import getsizeof

from ATRI.log import log
from ATRI.utils import request
from ATRI.exceptions import RequestError, WriteFileError


SETU_PATH = Path(".") / "data" / "plugins" / "setu"
TEMP_PATH = Path(".") / "data" / "temp"
SETU_PATH.mkdir(parents=True, exist_ok=True)
TEMP_PATH.mkdir(parents=True, exist_ok=True)


MODEL_URL = "https://res.imki.moe/nsfw.onnx"
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


async def detect_image(url: str, max_size: int) -> float:
    try:
        req = await request.get(url)
    except Exception:
        raise RequestError("Get info from download image failed!")

    img_byte = getsizeof(req.read()) // 1024
    if img_byte < max_size:
        return 0

    try:
        pattern = r"-(.*?)\/"
        file_name = re.findall(pattern, url)[0]
        path = TEMP_PATH / f"{file_name}.jpg"
        with open(path, "wb") as f:
            f.write(req.read())
    except Exception:
        raise WriteFileError("Writing file failed!")

    model_path = str(SETU_PATH / "nsfw.onnx")
    session = onnxruntime.InferenceSession(model_path)

    im = Image.open(path)

    if im.mode != "RGB":
        im = im.convert("RGB")
    imr = im.resize((256, 256), resample=Image.BILINEAR)
    fh_im = io.BytesIO()
    imr.save(fh_im, format="JPEG")
    fh_im.seek(0)

    image = skimage.img_as_float32(skimage.io.imread(fh_im))
    final = prepare_image(image)

    input_feed = {session.get_inputs()[0].name: final}
    outputs = [output.name for output in session.get_outputs()]
    result = session.run(outputs, input_feed)

    return result[0][0][1]


async def init_model():
    file_name = "nsfw.onnx"
    path = SETU_PATH / file_name
    if not path.is_file():
        log.warning("插件 setu 缺少资源, 装载中...")
        try:
            data = await request.get(MODEL_URL)
            with open(path, "wb") as w:
                w.write(data.read())
        except Exception:
            log.error("插件 setu 装载资源失败, 命令 '/nsfw' 将失效")

    log.success("插件 setu 装载资源完成")
