#!/usr/bin/env python3
"""真实执行源码 — 15_05_JSON_CSV解析"""
def exp_15_5():
    """实验5: JSON/CSV数据解析"""
    eid = '15_05_JSON_CSV解析'
    d = exp_start(eid, 'JSON/CSV解析')
    files = []

    import csv, io

    # JSON示例
    sample_json = {
        'name': '张三',
        'age': 25,
        'skills': ['Python', '爬虫', '数据分析'],
        'address': {'city': '北京', 'district': '朝阳区'},
        'projects': [
            {'name': '项目A', 'status': 'completed'},
            {'name': '项目B', 'status': 'in_progress'},
        ]
    }

    # CSV示例
    csv_data = """姓名,年龄,城市,技能
张三,25,北京,Python
李四,30,上海,Java
王五,28,深圳,Go
赵六,22,杭州,Rust
"""

    # 图1: JSON树结构
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    json_tree = json.dumps(sample_json, ensure_ascii=False, indent=2)
    ax.text(0.02, 0.98, json_tree, ha='left', va='top', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#FFF8E1'))
    ax.set_title('JSON数据结构示例', fontproperties=FONT, fontsize=14, y=1.02)
    p1 = os.path.join(d, '01_JSON结构.png')
    save_img(fig, p1); files.append(p1)

    # 图2: CSV表格
    reader = list(csv.reader(io.StringIO(csv_data)))
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    table = ax.table(cellText=reader[1:], colLabels=reader[0],
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#2196F3')
            cell.set_text_props(color='white', fontweight='bold')
    ax.set_title('CSV表格数据', fontproperties=FONT, fontsize=14)
    p2 = os.path.join(d, '02_CSV表格.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {})
