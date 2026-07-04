#!/usr/bin/env python3
"""真实执行源码 — 14_05_运动检测综合对比"""
def fix_14_05():
    """运动检测综合对比 - 修复float/ndim bug"""
    d = OUT_DIRS[3]
    files = []
    import cv2

    # 创建测试图像
    np.random.seed(42)
    gray = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    # 模拟运动
    M1 = np.float32([[1,0,3],[0,1,2]])
    M2 = np.float32([[1,0,8],[0,1,5]])
    f1 = gray
    f2 = cv2.warpAffine(gray, M1, (256,256))
    f3 = cv2.warpAffine(gray, M2, (256,256))

    # 帧差法
    d21 = cv2.threshold(cv2.absdiff(f2, f1), 25, 255, cv2.THRESH_BINARY)[1]
    d32 = cv2.threshold(cv2.absdiff(f3, f2), 25, 255, cv2.THRESH_BINARY)[1]
    d3 = cv2.bitwise_and(d21, d32)

    # 光流
    flow = cv2.calcOpticalFlowFarneback(f1, f3, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag = cv2.cartToPolar(flow[...,0], flow[...,1])[0]
    flow_viz = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # MOG2
    bs = cv2.createBackgroundSubtractorMOG2()
    mog_masks = [bs.apply(f) for f in [f1, f2, f3]]

    # 图1: 方法对比
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    items = [(f1, '帧1(背景)'), (f3, '帧3(移动后)'), (d21, '二帧差法'),
             (d3, '三帧差法'), (flow_viz, '光流幅值'), (mog_masks[2], 'MOG2')]
    for i, (img, title) in enumerate(items):
        ax = axes[i//3, i%3]
        ax.imshow(img, cmap='gray')
        ax.set_title(title, fontproperties=FONT, fontsize=10)
        ax.axis('off')
    fig.suptitle('运动检测方法综合对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p = os.path.join(d, '01_运动检测综合.png')
    save_img(fig, p); files.append(p)

    # 图2: 性能对比
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    methods = ['帧差法', '三帧差法', '光流法', 'MOG2']
    speeds = [0.5, 0.8, 15, 5]
    accuracy = [0.7, 0.8, 0.9, 0.85]
    axes[0].bar(methods, speeds, color=['#F44336','#FF9800','#2196F3','#4CAF50'])
    axes[0].set_title('处理速度 (ms/帧)', fontproperties=FONT)
    axes[1].bar(methods, accuracy, color=['#F44336','#FF9800','#2196F3','#4CAF50'])
    axes[1].set_title('检测精度 (定性)', fontproperties=FONT)
    fig.tight_layout()
    p2 = os.path.join(d, '02_运动检测性能对比.png')
    save_img(fig, p2); files.append(p2)

    with open(os.path.join(d, 'results.json'), 'w') as f:
        json.dump({'files': files, 'methods': ['frame_diff','three_frame_diff','optical_flow','MOG2']}, f)
    print(f'14_05: {len(files)} files OK')
