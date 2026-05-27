"""
主程序入口 — 把所有模块串起来运行

使用方法：
    python main.py

运行后会：
    1. 扫描 data/input 目录下的所有 Excel 文件
    2. 逐个读取并计算汇总
    3. 生成处理后的 Excel（带"总金额"列）到 data/output
    4. 打印文本报告
    5. 保存 JSON 报告
"""
from pathlib import Path
from file_finder import find_excel_files, get_file_stem
from excel_handler import ExcelProcessor
from report_generator import ReportGenerator, timer


@timer
def run():
    """主流程"""
    input_dir = Path(__file__).parent / "data" / "input"
    output_dir = Path(__file__).parent / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. 扫描文件
    files = find_excel_files(str(input_dir))
    print(f"找到 {len(files)} 个 Excel 文件")

    # 2. 逐个处理
    report = ReportGenerator()

    for file_path in files:
        print(f"\n--- 处理: {file_path.name} ---")

        processor = ExcelProcessor(file_path)

        # 读取
        data = processor.read()
        print(f"  读取了 {len(data)} 行数据")

        # 计算汇总
        summary = processor.get_summary()
        print(f"  总收入: {summary.get('total_revenue', '???')}")

        # 保存带"总金额"列的 Excel
        out_file = output_dir / f"{get_file_stem(file_path)}_processed.xlsx"
        processor.save(out_file)
        print(f"  已保存: {out_file.name}")

        # 加入报告
        report.add_summary(get_file_stem(file_path), summary)

    # 3. 生成报告
    print("\n" + "=" * 50)
    print(report.generate_text_report())

    # 4. 保存 JSON 报告
    json_path = output_dir / "summary_report.json"
    report.save_json_report(json_path)
    print(f"\nJSON 报告已保存: {json_path}")


if __name__ == "__main__":
    run()
