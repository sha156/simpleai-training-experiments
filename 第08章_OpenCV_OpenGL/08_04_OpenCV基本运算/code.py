#!/usr/bin/env python3
"""真实执行源码 — 08_04_OpenCV基本运算"""
def exp_8_4():
    """实验4: OpenCV基本操作 - 算术运算、逻辑运算"""
    eid = '08_04_OpenCV基本运算'
    d = exp_start(eid, 'OpenCV基本运算')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape

    # 算术运算
    bright = cv2.add(gray, 50)
    dark = cv2.subtract(gray, 50)
    contrast = cv2.multiply(gray, 1.5)

    # 逻辑运算
    mask_circle = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask_circle, (w//2, h//2), 100, 255, -1)
    and_op = cv2.bitwise_and(gray, mask_circle)
    or_op = cv2.bitwise_or(gray, mask_circle)
    xor_op = cv2.bitwise_xor(gray, mask_circle)
    not_op = cv2.bitwise_not(gray)

    fig = make_montage(
        [gray, bright, dark, contrast.astype(np.uint8),
         mask_circle, and_op, or_op, not_op],
        ['原图', '亮度+50', '亮度-50', '对比度×1.5',
         '圆形掩码', 'AND', 'OR', 'NOT'],
        cols=4, figsize=(18, 8),
        main_title='OpenCV算术与逻辑运算'
    )
    p1 = os.path.join(d, '01_基本运算.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'operations': ['add','subtract','multiply','bitwise_and','bitwise_or','bitwise_not']})
