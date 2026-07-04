"""
终端风格截图工具模块
从 gen_ch3_screenshots.py 提取，增加 output_dir 参数和高层封装。
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# 常量配置
# ============================================================
WIDTH = 900
FONT_MONO = "C:\\Windows\\Fonts\\CascadiaCode.ttf"
FONT_CJK = "C:\\Windows\\Fonts\\simhei.ttf"
BG = "#0C0C0C"
TITLE_BAR_BG = "#323232"
FG = "#CCCCCC"
PROMPT_COLOR = "#569CD6"
GREEN = "#6A9955"
YELLOW = "#DCDCAA"
ORANGE = "#CE9178"
WHITE = "#D4D4D4"
RED = "#F44747"
CYAN = "#9CDCFE"


# ============================================================
# 字体加载 (模块级缓存)
# ============================================================
_font_cache = {}


def _get_fonts(font_size: int = 14):
    """加载等宽字体和中文字体，带缓存"""
    key = f"mono_{font_size}"
    if key not in _font_cache:
        try:
            _font_cache[key] = ImageFont.truetype(FONT_MONO, font_size)
        except Exception:
            _font_cache[key] = ImageFont.load_default()

    key = f"cjk_{font_size}"
    if key not in _font_cache:
        try:
            _font_cache[key] = ImageFont.truetype(FONT_CJK, font_size)
        except Exception:
            _font_cache[key] = _font_cache.get(f"mono_{font_size}", ImageFont.load_default())

    return _font_cache[f"mono_{font_size}"], _font_cache[f"cjk_{font_size}"]


def _has_cjk(text: str) -> bool:
    """检测文本中是否包含中文/日文/韩文字符"""
    for c in text:
        cp = ord(c)
        if (0x4E00 <= cp <= 0x9FFF or   # CJK Unified
            0x3400 <= cp <= 0x4DBF or   # CJK Ext-A
            0x20000 <= cp <= 0x2A6DF or # CJK Ext-B
            0xF900 <= cp <= 0xFAFF or   # CJK Compatibility
            0x3040 <= cp <= 0x309F or   # Hiragana
            0x30A0 <= cp <= 0x30FF or   # Katakana
            0xAC00 <= cp <= 0xD7AF or   # Hangul
            0xFF00 <= cp <= 0xFFEF or   # Fullwidth
            0x3000 <= cp <= 0x303F):    # CJK Symbols
            return True
    return False


def _wrap_text(text: str, font, max_width: int) -> list[str]:
    """简单字符数折行 (等宽字体适用)"""
    # 估算每行最大字符数
    char_width = font.getbbox("X")[2] if hasattr(font, 'getbbox') else font.getsize("X")[0]
    max_chars = max(1, max_width // max(1, char_width))
    lines = []
    for line in text.split('\n'):
        while len(line) > max_chars:
            lines.append(line[:max_chars])
            line = line[max_chars:]
        lines.append(line)
    return lines


# ============================================================
# 核心截图函数
# ============================================================
def create_terminal_screenshot(
    lines: list,
    title: str,
    filename: str,
    output_dir: str = None,
    font_size: int = 14,
    width: int = WIDTH,
) -> str:
    """生成终端风格的 PNG 截图

    Args:
        lines: list of (text, color) tuples or plain strings
        title: 标题栏显示的文字
        filename: 输出 PNG 文件名
        output_dir: 输出目录 (默认当前目录)
        font_size: 字体大小
        width: 图片宽度

    Returns:
        生成的 PNG 文件完整路径
    """
    if output_dir is None:
        output_dir = os.getcwd()

    line_height = int(font_size * 1.5)
    margin_x = 25
    margin_y_top = 45
    margin_y_bottom = 25

    font_mono, font_cjk = _get_fonts(font_size)

    # 计算总高度
    total_height = margin_y_top + len(lines) * line_height + margin_y_bottom + 35
    img = Image.new("RGB", (width, total_height), BG)
    draw = ImageDraw.Draw(img)

    # 标题栏
    draw.rectangle([(0, 0), (width, 35)], fill=TITLE_BAR_BG)
    draw.text((12, 8), f"  {title}  ", fill=WHITE, font=font_cjk)

    # 绘制每一行
    y = margin_y_top
    for item in lines:
        if isinstance(item, tuple):
            text, color = item
        else:
            text, color = str(item), FG

        has_cjk = _has_cjk(text)
        font = font_cjk if has_cjk else font_mono
        draw.text((margin_x, y), text, fill=color, font=font)
        y += line_height

    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    return filepath


def create_step_screenshot(
    step_code: str,
    step_output: str,
    title: str,
    filename: str,
    output_dir: str,
    step_num: int = 1,
    total_steps: int = 1,
    font_size: int = 14,
) -> str:
    """生成单步操作的终端风格截图 (代码 + 输出)

    Args:
        step_code: 该步骤的 Python 代码
        step_output: 该步骤的执行输出 (stdout+stderr)
        title: 实验标题
        filename: 输出 PNG 文件名
        output_dir: 输出目录
        step_num: 当前步骤序号
        total_steps: 总步骤数
        font_size: 字体大小

    Returns:
        生成的 PNG 文件完整路径
    """
    lines = []

    # 提示符
    lines.append((f"$ python experiment_step{step_num}.py", PROMPT_COLOR))
    lines.append(("", FG))

    # 代码部分 - 带语法高亮
    for raw_line in step_code.strip().split('\n'):
        stripped = raw_line.rstrip()
        if not stripped:
            lines.append(("", FG))
        elif stripped.strip().startswith('#'):
            lines.append((stripped, GREEN))
        elif stripped.strip().startswith('"""') or stripped.strip().startswith("'''"):
            lines.append((stripped, ORANGE))
        elif any(kw in stripped for kw in ('import ', 'from ')):
            lines.append((stripped, CYAN))
        elif any(kw in stripped for kw in ('def ', 'class ')):
            lines.append((stripped, YELLOW))
        elif 'print(' in stripped or 'print ' in stripped:
            lines.append((stripped, FG))
        else:
            lines.append((stripped, FG))

    # 分隔线
    lines.append(("", FG))
    lines.append(("─" * 80, GREEN))
    lines.append((f"  >>> 输出 (步骤 {step_num}/{total_steps})", YELLOW))
    lines.append(("─" * 80, GREEN))
    lines.append(("", FG))

    # 输出部分
    output_text = step_output.strip()
    if output_text:
        for out_line in output_text.split('\n'):
            stripped = out_line.rstrip()
            if 'Error' in stripped or 'Traceback' in stripped or 'error' in stripped.lower():
                lines.append((stripped, RED))
            elif stripped.startswith('WARNING') or stripped.startswith('Warning'):
                lines.append((stripped, YELLOW))
            else:
                lines.append((stripped, FG))
    else:
        lines.append(("(无输出)", GREEN))

    lines.append(("", FG))
    lines.append((f"✓ 步骤 {step_num}/{total_steps} 完成", GREEN))

    return create_terminal_screenshot(
        lines, title, filename,
        output_dir=output_dir,
        font_size=font_size,
    )


def create_combined_screenshot(
    all_lines: list,
    title: str,
    filename: str,
    output_dir: str,
    font_size: int = 14,
) -> str:
    """生成综合截图 (所有步骤的代码+输出合并)

    Args:
        all_lines: 完整的 (text, color) 行列表
        title: 标题
        filename: 输出文件名
        output_dir: 输出目录
        font_size: 字体大小

    Returns:
        生成的 PNG 文件完整路径
    """
    return create_terminal_screenshot(
        all_lines, title, filename,
        output_dir=output_dir,
        font_size=font_size,
    )
