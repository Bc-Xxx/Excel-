"""
报告生成模块 — 汇总所有文件的结果，输出报告
用到的知识点：装饰器、JSON、文件读写
"""
import functools
import json
import time
from pathlib import Path


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"开始时间是{start:.2f}")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"结束时间是{end},总耗时{end - start:.2f}")
        return result

    return wrapper


class ReportGenerator:
    """从多个文件的汇总数据生成最终报告"""

    def __init__(self):
        # 每个元素格式: {"file_name": "xxx", "total_revenue": 100, ...}
        self.summaries = []

    def add_summary(self, file_name: str, summary: dict):
        """添加一个文件的汇总数据"""
        summary["file_name"] = file_name
        self.summaries.append(summary)

    def generate_text_report(self) -> str:
        """
        生成文本格式的总报告

        返回：
            str: 格式化的报告文本
        """
        lines = []  # 创建一个列表，用于存储报告的每一行
        total_revenue_all = 0  # 初始化总营收变量
        for summary in self.summaries:
            lines.append(f"文件:{summary["file_name"]}")
            lines.append(f"商品销售总额:{summary['total_revenue']}")
            lines.append(f"商品总销量:{summary['total_quantity']}")
            lines.append(f"  销售额最高的商品: {summary['top_product']}")
            lines.append("")
            total_revenue_all += summary['total_revenue']
        lines.append(f"所有文件总营收: {total_revenue_all:,.2f}")
        lines.append(f"共处理文件数: {len(self.summaries)}")
        result = "\n".join(lines)
        return result

    def save_json_report(self, output_path: Path):
        """
        把汇总数据保存为 JSON 文件

        参数：
            output_path: 输出路径
        """
        json_content = json.dumps(self.summaries, ensure_ascii=False, indent=2)
        output_path.write_text(json_content, encoding="utf-8")
