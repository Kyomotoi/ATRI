import re
from math import floor
import jieba.posseg as pseg
from typing import Union, Optional
from random import random, choice, randint


def roll_dice(par: str) -> str:
    result = 0
    proc = ""
    proc_list = []
    p = par.split("+")

    for i in p:
        args = re.findall(r"(\d{0,10})(?:(d)(\d{1,10}))", i)
        args = list(args[0])

        args[0] = args[0] or 1
        if int(args[0]) >= 5000 or int(args[2]) >= 5000:
            return "阿...好大......"

        for a in range(1, int(args[0]) + 1):
            rd = randint(1, int(args[2]))
            result = result + rd

            if len(proc_list) <= 10:
                proc_list.append(rd)

    if len(proc_list) <= 10:
        proc += "+".join(map(str, proc_list))
    elif len(proc_list) > 10:
        proc += "太长了不展示了就酱w"
    else:
        proc += str(result)

    result = f"{par}=({proc})={result}"
    return result


class Encrypt:
    cr = "ĀāĂăĄąÀÁÂÃÄÅ"
    cc = "ŢţŤťŦŧṪṫṬṭṮṯṰṱ"
    cn = "ŔŕŘřṘṙŖŗȐȑȒȓṚṛṜṝṞṟɌɍⱤɽᵲᶉɼɾᵳʀＲｒ"
    cb = "ĨĩĪīĬĭĮįİı"

    sr = len(cr)
    sc = len(cc)
    sn = len(cn)
    sb = len(cb)
    src = sr * sc
    snb = sn * sb
    scnb = sc * snb

    def _div(self, a: int, b: int) -> int:
        return floor(a / b)

    def _encodeByte(self, i) -> Union[str, None]:
        if i > 0xFF:
            raise ValueError("ERROR! at/ri overflow")

        if i > 0x7F:
            i = i & 0x7F
            return self.cn[self._div(i, self.sb) + int(self.cb[i % self.sb])]

        return self.cr[self._div(i, self.sc) + int(self.cc[i % self.sc])]

    def _encodeShort(self, i) -> str:
        if i > 0xFFFF:
            raise ValueError("ERROR! atri overflow")

        reverse = False
        if i > 0x7FFF:
            reverse = True
            i = i & 0x7FFF

        char = [
            self._div(i, self.scnb),
            self._div(i % self.scnb, self.snb),
            self._div(i % self.snb, self.sb),
            i % self.sb,
        ]
        char = [self.cr[char[0]], self.cc[char[1]], self.cn[char[2]], self.cb[char[3]]]

        if reverse:
            return char[2] + char[3] + char[0] + char[1]

        return "".join(char)

    def _decodeByte(self, c) -> int:
        nb = False
        idx = [self.cr.index(c[0]), self.cc.index(c[1])]
        if idx[0] < 0 or idx[1] < 0:
            idx = [self.cn.index(c[0]), self.cb.index(c[1])]
            nb = True
            raise ValueError("ERROR! at/ri overflow")

        result = idx[0] * self.sb + idx[1] if nb else idx[0] * self.sc + idx[1]
        if result > 0x7F:
            raise ValueError("ERROR! at/ri overflow")

        return result | 0x80 if nb else 0

    def _decodeShort(self, c) -> int:
        reverse = c[0] not in self.cr
        if not reverse:
            idx = [
                self.cr.index(c[0]),
                self.cc.index(c[1]),
                self.cn.index(c[2]),
                self.cb.index(c[3]),
            ]
        else:
            idx = [
                self.cr.index(c[2]),
                self.cc.index(c[3]),
                self.cn.index(c[0]),
                self.cb.index(c[1]),
            ]

        if idx[0] < 0 or idx[1] < 0 or idx[2] < 0 or idx[3] < 0:
            raise ValueError("ERROR! not atri")

        result = idx[0] * self.scnb + idx[1] * self.snb + idx[2] * self.sb + idx[3]
        if result > 0x7FFF:
            raise ValueError("ERROR! atri overflow")

        result |= 0x8000 if reverse else 0
        return result

    def _encodeBytes(self, b) -> str:
        result = []
        for i in range(0, (len(b) >> 1)):
            result.append(self._encodeShort((b[i * 2] << 8 | b[i * 2 + 1])))

        if len(b) & 1 == 1:
            result.append(self._encodeByte(b[-1]))

        return "".join(result)

    def encode(self, s: str, encoding: str = "utf-8"):
        if not isinstance(s, str):
            raise ValueError("Please enter str instead of other")

        return self._encodeBytes(s.encode(encoding))

    def _decodeBytes(self, s: str):
        if not isinstance(s, str):
            raise ValueError("Please enter str instead of other")

        if len(s) & 1:
            raise ValueError("ERROR length")

        result = []
        for i in range(0, (len(s) >> 2)):
            result.append(bytes([self._decodeShort(s[i * 4 : i * 4 + 4]) >> 8]))
            result.append(bytes([self._decodeShort(s[i * 4 : i * 4 + 4]) & 0xFF]))

        if (len(s) & 2) == 2:
            result.append(bytes([self._decodeByte(s[-2:])]))

        return b"".join(result)

    def decode(self, s: str, encoding: str = "utf-8") -> str:
        if not isinstance(s, str):
            raise ValueError("Please enter str instead of other")

        try:
            return self._decodeBytes(s).decode(encoding)
        except UnicodeDecodeError:
            raise ValueError("Decoding failed")


class Yinglish:
    @staticmethod
    def _to_ying(x, y, ying) -> str:
        if random() > ying:
            return x
        if x in ["，", "。"]:
            return str(choice(["..", "...", "....", "......"]))
        if x in ["！", "!"]:
            return "❤"
        if len(x) > 1 and random() < 0.5:
            return str(
                choice(
                    [
                        f"{x[0]}..{x}",
                        f"{x[0]}...{x}",
                        f"{x[0]}....{x}",
                        f"{x[0]}......{x}",
                    ]
                )
            )
        else:
            if y == "n" and random() < 0.5:
                x = "〇" * len(x)
            return str(choice([f"...{x}", f"....{x}", f".....{x}", f"......{x}"]))

    @classmethod
    def deal(cls, text, ying: Optional[float] = 0.5) -> str:
        return "".join([cls._to_ying(x, y, ying) for x, y in pseg.cut(text)])
