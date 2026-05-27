"""
测试文件 — 验证各个模块功能是否正常

运行方法：
    cd excel_tool
    pytest tests/ -v
"""
import pytest
import pandas as pd
from pathlib import Path

# 导入要测试的模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from file_finder import find_excel_files, get_file_stem
from excel_handler import ExcelProcessor


# ========================================
# 测试 file_finder 模块
# ========================================

class TestFileFinder:
    """测试文件扫描功能"""

    def test_find_excel_files_returns_list(self):
        """find_excel_files 应该返回一个列表"""
        # 注意：需要先运行 create_sample_data.py 生成样本数据
        input_dir = str(Path(__file__).parent.parent / "data" / "input")
        result = find_excel_files(input_dir)
        assert isinstance(result, list), "应该返回列表"

    def test_find_excel_files_finds_correct_count(self):
        """应该找到 3 个 Excel 文件"""
        input_dir = str(Path(__file__).parent.parent / "data" / "input")
        result = find_excel_files(input_dir)
        assert len(result) == 3, f"应该找到 3 个文件，实际找到 {len(result)} 个"

    def test_get_file_stem(self):
        """get_file_stem 应该去掉后缀"""
        path = Path("data/input/sales_2024_01.xlsx")
        assert get_file_stem(path) == "sales_2024_01"


# ========================================
# 测试 excel_handler 模块
# ========================================

class TestExcelProcessor:
    """测试 Excel 处理功能"""

    @pytest.fixture
    def sample_file(self):
        """提供一个样本 Excel 文件路径"""
        return Path(__file__).parent.parent / "data" / "input" / "sales_2024_01.xlsx"

    def test_read_returns_dataframe(self, sample_file):
        """read() 应该返回 DataFrame"""
        processor = ExcelProcessor(sample_file)
        data = processor.read()
        assert isinstance(data, pd.DataFrame), "应该返回 DataFrame"
        assert len(data) > 0, "不应该返回空数据"

    def test_read_has_correct_columns(self, sample_file):
        """读取的数据应该包含"商品"列"""
        processor = ExcelProcessor(sample_file)
        data = processor.read()
        assert "商品" in data.columns, "应该有'商品'列"
        assert "单价" in data.columns, "应该有'单价'列"
        assert "数量" in data.columns, "应该有'数量'列"

    def test_read_file_not_found(self):
        """读取不存在的文件应该抛出异常"""
        processor = ExcelProcessor(Path("不存在的文件.xlsx"))
        with pytest.raises(FileNotFoundError):
            processor.read()

    def test_add_total_column(self, sample_file):
        """add_total_column 应该新增'总金额'列"""
        processor = ExcelProcessor(sample_file)
        processor.read()
        data = processor.add_total_column()
        assert "总金额" in data.columns, "应该有'总金额'列"
        # 第一行：键盘 299 * 10 = 2990
        assert data.iloc[0]["总金额"] == 2990, f"第一行总金额应该是 2990，实际是 {data.iloc[0]['总金额']}"

    def test_get_summary(self, sample_file):
        """get_summary 应该返回包含正确字段的字典"""
        processor = ExcelProcessor(sample_file)
        processor.read()
        summary = processor.get_summary()
        assert isinstance(summary, dict), "应该返回字典"
        assert "total_revenue" in summary, "应该有 total_revenue"
        assert "top_product" in summary, "应该有 top_product"


# ========================================
# 测试运行入口
# ========================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
