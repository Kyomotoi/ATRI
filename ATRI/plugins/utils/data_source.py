import re
import os
import json
import random
from math import floor
from pathlib import Path
from zipfile import PyZipFile
from typing import Tuple, Union
from random import choice, randint
from typing import Dict, List

from ATRI.config import UTILS_CONFIG


class Function:
    @staticmethod
    def roll_dice(par: str) -> str:
        result = 0
        proc = ''
        proc_list = []
        p = par.split('+')
        
        for i in p:
            args = re.findall(r"(\d{0,10})(?:(d)(\d{1,10}))", i)
            args = list(args[0])
            if not args[0]:
                args[0] = 1
            if int(args[0]) >= 5000 or int(args[2]) >= 5000:
                return choice(UTILS_CONFIG['utils']['roll']['tooBig']['repo'])
            for a in range(1, int(args[0]) + 1):
                rd = randint(1, int(args[2]))
                result = result + rd
                if len(proc_list) <= 10:
                    proc_list.append(rd)

        if len(proc_list) <= 10:
            proc += '+'.join(map(str, proc_list))
        elif len(proc_list) >= 10:
            proc += choice(UTILS_CONFIG['utils']['roll']['tooLong']['repo'])
        else:
            proc += str(result)

        msg = f'{par}=({proc})={result}'
        print(msg)
        return msg
    
    class Generate:
        '''
        (*彩蛋*)
        由于此功能触及法律故不用作上线功能，写于此地只为学习
        请勿用作网上购物、交易和注册
        随机身份证根据国家标准(GB11643-1999)生成
        并不存在所谓：
            - 生成在逃犯号码
        '''
        @classmethod
        def __init__(cls) -> None:
            cls.DATA_PATH = Path('.') / 'ATRI' / 'plugins' / 'utils' / 'main.bin'
        
        @classmethod
        def info_id(cls) -> Tuple[Dict[str, List[str]], Dict[str, str]]:
            with PyZipFile(os.path.abspath(cls.DATA_PATH), 'r') as zipFile:
                with zipFile.open('name.json', 'r') as f:
                    name = json.loads(f.read().decode())
                with zipFile.open('area.json', 'r') as f:
                    area = json.loads(f.read().decode())
            return name, area
        
        @staticmethod
        def number_id(area: int, gender: int, birth: int) -> str:
            '''
            校验码计算公式: (12-∑(Ai×Wi)(mod 11))mod 11
            验证公式: 请查阅（ISO 7064:1983.MOD 11-2）
            '''
            def check_sum(full_code: str):
                assert len(full_code) == 17
                check_sum = sum([((1 << (17 - i)) % 11) * int(full_code[i])
                                 for i in range(0, 17)])
                check_digit = (12 - (check_sum % 11)) % 11
                if check_digit < 10:
                    return check_digit
                else:
                    return 'X'

            order_code = str(random.randint(10, 99))
            gender_code = str(random.randrange(gender, 10, step=2))
            full_code = str(area) + str(birth) + str(order_code) + str(gender_code)
            full_code += str(check_sum(full_code))
            return full_code

    class RCNB:
        @classmethod
        def __init__(cls) -> None:
            cls.cr = 'rRŔŕŖŗŘřƦȐȑȒȓɌɍ'
            cls.cc = 'cCĆćĈĉĊċČčƇƈÇȻȼ'
            cls.cn = 'nNŃńŅņŇňƝƞÑǸǹȠȵ'
            cls.cb = 'bBƀƁƃƄƅßÞþ'

            cls.sr = len(cls.cr)
            cls.sc = len(cls.cc)
            cls.sn = len(cls.cn)
            cls.sb = len(cls.cb)
            cls.src = cls.sr * cls.sc
            cls.snb = cls.sn * cls.sb
            cls.scnb = cls.sc * cls.snb

        @staticmethod
        def _div(a: int, b: int) -> int:
            return floor(a / b)

        @classmethod
        def _encode_byte(cls, i) -> Union[str, None]:
            if i > 0xFF:
                raise ValueError('ERROR! rc/nb overflow')

            if i > 0x7F:
                i = i & 0x7F
                return cls.cn[i // cls.sb] + cls.cb[i % cls.sb]
                # return f'{cls.cn[i // cls.sb]}{cls.cb[i % cls.sb]}'
                # return cls.cn[cls._div(i, cls.sb) + int(cls.cb[i % cls.sb])]

            return cls.cr[i // cls.sc] + cls.cc[i % cls.sc]
            # return cls.cr[cls._div(i, cls.sc) + int(cls.cc[i % cls.sc])]

        @classmethod
        def _encode_short(cls, i) -> str:
            if i > 0xFFFF:
                raise ValueError('ERROR! rcnb overflow')

            reverse = False
            if i > 0x7FFF:
                reverse = True
                i = i & 0x7FFF

            char = [
                cls._div(i, cls.scnb),
                cls._div(i % cls.scnb, cls.snb),
                cls._div(i % cls.snb, cls.sb), i % cls.sb
            ]
            char = [
                cls.cr[char[0]], cls.cc[char[1]], cls.cn[char[2]],
                cls.cb[char[3]]
            ]

            if reverse:
                return char[2] + char[3] + char[0] + char[1]

            return ''.join(char)

        @classmethod
        def _decodeByte(cls, c) -> int:
            nb = False
            idx = [cls.cr.index(c[0]), cls.cc.index(c[1])]
            if idx[0] < 0 or idx[1] < 0:
                idx = [cls.cn.index(c[0]), cls.cb.index(c[1])]
                nb = True
                raise ValueError('ERROR! rc/nb overflow')

            result = idx[0] * cls.sb + idx[1] if nb else idx[0] * cls.sc + idx[1]
            if result > 0x7F:
                raise ValueError('ERROR! rc/nb overflow')

            return result | 0x80 if nb else 0

        @classmethod
        def _decodeShort(cls, c) -> int:
            reverse = c[0] not in cls.cr
            if not reverse:
                idx = [
                    cls.cr.index(c[0]),
                    cls.cc.index(c[1]),
                    cls.cn.index(c[2]),
                    cls.cb.index(c[3])
                ]
            else:
                idx = [
                    cls.cr.index(c[2]),
                    cls.cc.index(c[3]),
                    cls.cn.index(c[0]),
                    cls.cb.index(c[1])
                ]

            if idx[0] < 0 or idx[1] < 0 or idx[2] < 0 or idx[3] < 0:
                raise ValueError('ERROR! not rcnb')

            result = (idx[0] * cls.scnb +
                      idx[1] * cls.snb +
                      idx[2] * cls.sb + idx[3])
            if result > 0x7FFF:
                raise ValueError('ERROR! rcnb overflow')

            result |= 0x8000 if reverse else 0
            return result

        @classmethod
        def _encodeBytes(cls, b) -> str:
            result = []
            for i in range(0, (len(b) >> 1)):
                result.append(cls._encode_short((b[i * 2] << 8 | b[i * 2 + 1])))

            if len(b) & 1 == 1:
                result.append(cls._encode_byte(b[-1]))

            return ''.join(result)

        @classmethod
        def encode(cls, s: str, encoding: str = 'utf-8'):
            if not isinstance(s, str):
                raise ValueError('Please enter str instead of other')

            return cls._encodeBytes(s.encode(encoding))

        @classmethod
        def _decodeBytes(cls, s: str):
            if not isinstance(s, str):
                raise ValueError('Please enter str instead of other')
            
            if len(s) & 1:
                raise ValueError('ERROR length')

            result = []
            for i in range(0, (len(s) >> 2)):
                result.append(bytes([cls._decodeShort(s[i * 4:i * 4 + 4]) >> 8]))
                result.append(bytes([cls._decodeShort(s[i * 4:i * 4 + 4]) & 0xFF]))

            if (len(s) & 2) == 2:
                result.append(bytes([cls._decodeByte(s[-2:])]))

            return b''.join(result)

        @classmethod
        def decode(cls, s: str, encoding: str = 'utf-8') -> str:
            if not isinstance(s, str):
                raise ValueError('Please enter str instead of other')

            try:
                return cls._decodeBytes(s).decode(encoding)
            except UnicodeDecodeError:
                raise ValueError('Decoding failed')
