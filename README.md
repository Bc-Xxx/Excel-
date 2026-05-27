# Excel 批量处理工具

批量处理 Excel 销售数据文件，自动计算每个商品的销售额（单价×数量），统计汇总信息并生成报告。

## 功能

- 扫描指定目录下的所有 Excel 文件
- 读取销售数据，自动添加"总金额"列（单价 × 数量）
- 统计每个文件的总收入、总销量、销售额最高的商品
- 保存处理后的 Excel 文件（带"总金额"列）
- 生成文本报告 + JSON 汇总报告

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 生成样本数据
python create_sample_data.py

# 运行
python main.py
```

## 项目结构

```
excel_tool/
├── main.py                  # 主入口
├── file_finder.py           # 文件扫描
├── excel_handler.py         # Excel 读写与计算
├── report_generator.py      # 报告生成
├── create_sample_data.py    # 生成测试样本数据
├── requirements.txt
├── data/
│   ├── input/               # 输入：Excel 文件放在这里
│   └── output/              # 输出：处理后的文件和报告
└── tests/
    └── test_excel_tool.py   # 单元测试
```

## 运行测试

```bash
pytest tests/ -v
```
