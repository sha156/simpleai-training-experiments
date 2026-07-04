#!/usr/bin/env python3
"""真实执行源码 — 15_03_HTML解析"""
def exp_15_3():
    """实验3: HTML解析 - BeautifulSoup基础"""
    eid = '15_03_HTML解析'
    d = exp_start(eid, 'HTML解析')
    files = []

    # 模拟HTML
    html_sample = """<!DOCTYPE html>
<html>
<head><title>示例页面</title></head>
<body>
  <div class="container">
    <h1>文章标题</h1>
    <p class="content">这是第一段内容</p>
    <p class="content">这是第二段内容</p>
    <ul id="list">
      <li><a href="/item/1">项目1</a></li>
      <li><a href="/item/2">项目2</a></li>
      <li><a href="/item/3">项目3</a></li>
    </ul>
    <img src="/images/logo.png" alt="Logo">
  </div>
</body>
</html>"""

    # 图: HTML树形结构
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    tree = (
        '                          html\n'
        '                     ┌─────┴─────┐\n'
        '                   head          body\n'
        '                    │              │\n'
        '                  title         div.container\n'
        '                    │         ┌────┼────┬────┐\n'
        '               "示例页面"     h1    p    ul   img\n'
        '                              │    │×2   │    │\n'
        '                          "文章  "内容"  li×3 "Logo"\n'
        '                          标题"        │\n'
        '                                     a×3\n'
        '                                     │\n'
        '                                 "项目N"'
    )
    ax.text(0.5, 0.5, tree, ha='center', va='center', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#f8f8f8'))
    ax.set_title('HTML DOM树解析', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_HTML_DOM树.png')
    save_img(fig, p1); files.append(p1)

    # 图2: BeautifulSoup选择器
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    selectors = [
        ('Tag选择', "soup.find('h1')", "→ 第一个<h1>标签"),
        ('Class选择', "soup.find_all(class_='content')", "→ 所有class='content'的元素"),
        ('ID选择', "soup.find(id='list')", "→ id='list'的元素"),
        ('CSS选择', "soup.select('div.container > ul > li')", "→ 所有容器的<li>"),
        ('属性选择', "soup.find('img')['src']", "→ 图片src属性值"),
        ('文本提取', "soup.find('h1').get_text()", "→ '文章标题'"),
    ]
    for i, (name, code, result) in enumerate(selectors):
        y_pos = 0.85 - i * 0.14
        ax.text(0.1, y_pos, f'{name}:', fontsize=11, fontproperties=FONT, fontweight='bold',
                transform=ax.transAxes)
        ax.text(0.35, y_pos, code, fontsize=10, fontfamily='monospace', transform=ax.transAxes,
                bbox=dict(facecolor='#E3F2FD', alpha=0.5))
        ax.text(0.75, y_pos, result, fontsize=10, transform=ax.transAxes, color='#666')

    ax.set_title('BeautifulSoup常用选择器', fontproperties=FONT, fontsize=14)
    p2 = os.path.join(d, '02_BeautifulSoup选择器.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {})
