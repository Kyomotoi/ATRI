import yaml

from pathlib import Path


def load_yml(file: Path, encoding="utf-8") -> dict:
    """加载 yml 文件"""
    with open(file, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data
