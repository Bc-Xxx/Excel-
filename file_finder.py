"""
文件扫描模块 — 找出目录下所有 Excel 文件
用到的知识点：pathlib、列表推导式
"""
from pathlib import Path


def find_excel_files(directory: str, suffix: str = ".xlsx") -> list[Path]:
    directory = Path(directory)
    files=list(directory.glob(f"*{suffix}"))
    return files




def get_file_stem(file_path: Path) -> str:
    stem=file_path.stem
    return stem



