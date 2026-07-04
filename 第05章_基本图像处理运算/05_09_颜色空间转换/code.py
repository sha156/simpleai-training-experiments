#!/usr/bin/env python3
"""真实执行源码 — 05_09_颜色空间转换"""
def fix_05_09():
    """颜色空间转换"""
    d = OUT_DIRS[0]
    files = []
    import cv2
    # 使用简单的彩色渐变图
    h, w = 256, 256
    gradient = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            gradient[i, j] = [int(255*i/h), int(255*j/w), 128]
    img_rgb = gradient
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    spaces = [(img_rgb, 'RGB'), (hsv, 'HSV'), (lab, 'Lab'),
              (cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HLS), 'HLS')]
    for i, (img, name) in enumerate(spaces):
        ax = axes[i//2, i%2]
        ax.imshow(img)
        ax.set_title(f'{name}颜色空间', fontproperties=FONT)
        ax.axis('off')
    fig.suptitle('颜色空间转换', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p = os.path.join(d, '01_颜色空间转换.png')
    save_img(fig, p); files.append(p)

    # HSV通道分解
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for i, (name, cmap) in enumerate([('H色调', 'hsv'), ('S饱和度', 'gray'), ('V明度', 'gray')]):
        axes[i].imshow(hsv[:,:,i], cmap=cmap)
        axes[i].set_title(name, fontproperties=FONT)
        axes[i].axis('off')
    fig.suptitle('HSV通道分解', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_HSV通道分解.png')
    save_img(fig, p2); files.append(p2)

    with open(os.path.join(d, 'results.json'), 'w') as f:
        json.dump({'files': files, 'spaces': ['RGB','HSV','Lab','HLS']}, f)
    print(f'05_09: {len(files)} files OK')
