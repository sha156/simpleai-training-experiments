#!/usr/bin/env python3
"""真实执行源码 — 08_01_OpenCV绘图函数"""
def exp_8_1():
    """实验1: OpenCV绘图函数 - 直线、圆、矩形、文字"""
    eid = '08_01_OpenCV绘图函数'
    d = exp_start(eid, 'OpenCV绘图函数')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    h, w = img.shape[:2]
    draw = img.copy()
    bgr = cv2.cvtColor(draw, cv2.COLOR_RGB2BGR)

    # 绘制各种图形
    cv2.line(bgr, (0, 0), (w, h), (255, 0, 0), 3)
    cv2.line(bgr, (w, 0), (0, h), (0, 255, 0), 3)
    cv2.rectangle(bgr, (50, 50), (200, 200), (0, 0, 255), 2)
    cv2.circle(bgr, (w//2, h//2), 100, (255, 255, 0), 3)
    cv2.circle(bgr, (w//2, h//2), 5, (0, 255, 255), -1)
    cv2.ellipse(bgr, (w-100, 100), (60, 30), 45, 0, 360, (255, 0, 255), 2)

    pts = np.array([[300,400],[350,350],[400,380],[420,430],[370,460],[320,440]], np.int32)
    cv2.polylines(bgr, [pts], True, (0, 255, 255), 2)

    # 添加文字
    cv2.putText(bgr, 'OpenCV Drawing', (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(bgr, 'Line', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    cv2.putText(bgr, 'Rect', (210, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.putText(bgr, 'Circle', (w//2+110, h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    ax.set_title('OpenCV绘图函数演示', fontproperties=FONT, fontsize=14)
    ax.axis('off')
    fig.tight_layout()
    p1 = os.path.join(d, '01_绘图函数演示.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 单独展示各种图形
    canvas = np.ones((400, 600, 3), dtype=np.uint8) * 40
    cv2.line(canvas, (50, 50), (550, 50), (255, 0, 0), 2)
    cv2.rectangle(canvas, (50, 80), (200, 180), (0, 255, 0), -1)
    cv2.rectangle(canvas, (220, 80), (370, 180), (0, 255, 0), 2)
    cv2.circle(canvas, (485, 130), 50, (0, 0, 255), -1)
    cv2.circle(canvas, (135, 230), 50, (0, 0, 255), 2)
    cv2.ellipse(canvas, (390, 230), (80, 40), 0, 0, 360, (255, 255, 0), -1)
    cv2.ellipse(canvas, (390, 320), (80, 40), 30, 0, 270, (255, 255, 0), 2)
    pts2 = np.array([[50,300],[150,280],[200,330],[180,370],[80,360]], np.int32)
    cv2.polylines(canvas, [pts2], True, (255, 0, 255), 2)
    cv2.putText(canvas, 'OpenCV', (230, 370), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
    ax.set_title('OpenCV绘图元素大全', fontproperties=FONT, fontsize=14)
    ax.axis('off')
    fig.tight_layout()
    p2 = os.path.join(d, '02_绘图元素大全.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'shapes': ['line','rectangle','circle','ellipse','polyline','text']})
