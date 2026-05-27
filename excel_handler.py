"""
Excel 读写模块 — 核心：用 pandas 处理 Excel 数据
用到的知识点：pandas、异常处理、文件读写
"""
import pandas as pd
from pathlib import Path


class ExcelProcessor:
    """Excel 文件处理器，负责读取、计算、写入"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = None

    def read(self) -> pd.DataFrame:
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件{self.file_path}不存在")
        try:
            self.data = pd.read_excel(self.file_path)
            return self.data
        except Exception as e:
            raise Exception(f"读取文件异常{e}")

    def add_total_column(self) -> pd.DataFrame:
        if self.data is None:
            raise ValueError("目前没有读取到数据文件")
        self.data["总金额"] = self.data["单价"] * self.data["数量"]
        return self.data

    def get_summary(self) -> dict:
        self.add_total_column()
        total_revenue = self.data["总金额"].sum()
        total_quantity = self.data["数量"].sum()
        max_id = self.data["总金额"].idxmax()
        top_product = self.data.loc[max_id, "商品"]
        return {
            "total_revenue": int(total_revenue),
            "total_quantity": int(total_quantity),
            "top_product": str(top_product)
        }

    def save(self, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.data.to_excel(output_path, index=False)
