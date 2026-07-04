#!/usr/bin/env python3
"""真实执行源码 — 14_02_背景减除"""
def exp_14_2():
    """实验2: 背景减除法"""
    eid = '14_02_背景减除'
    d = exp_start(eid, '背景减除')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 模拟: 前几帧作为背景, 后面出现"运动目标"
    bg = gray.copy()
    # 添加运动目标: 在某个区域叠加
    fg_region = gray[80:200, 80:200].copy()

    frames_with_fg = []
    for i in range(4):
        frame = bg.copy()
        if i >= 1:  # 第2帧开始出现前景
            # 前景位置逐渐移动
            ox, oy = 50 + i*30, 30 + i*20
            roi = frame[oy:oy+120, ox:ox+120]
            if roi.shape == fg_region.shape:
                cv2.addWeighted(roi, 0.5, fg_region, 0.5, 0, roi)
        frames_with_fg.append(frame)

    # 背景建模: 用第一帧
    bg_model = frames_with_fg[0].astype(np.float32)
    fg_masks = []
    for f in frames_with_fg[1:]:
        diff = cv2.absdiff(f, bg_model.astype(np.uint8))
        _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        fg_masks.append(mask)

    fig = make_montage(
        frames_with_fg + fg_masks,
        ['背景帧', '帧2(目标出现)', '帧3(移动)', '帧4(移动)',
         '前景mask 2', '前景mask 3', '前景mask 4'],
        cols=4, figsize=(16, 12),
        main_title='背景减除法运动检测'
    )
    p1 = os.path.join(d, '01_背景减除.png')
    save_img(fig, p1); files.append(p1)

    # 图2: MOG2背景建模 (模拟)
    backSub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=36)
    mog_masks = []
    for f in frames_with_fg:
        mask = backSub.apply(f)
        mog_masks.append(mask)

    fig = make_montage(
        mog_masks,
        ['MOG2 frame1', 'MOG2 frame2', 'MOG2 frame3', 'MOG2 frame4'],
        cols=4, figsize=(16, 4),
        main_title='MOG2自适应背景建模'
    )
    p2 = os.path.join(d, '02_MOG2背景建模.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'methods': ['static_bg','MOG2']})
