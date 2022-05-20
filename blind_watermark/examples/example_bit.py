# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from blind_watermark import att
from blind_watermark import WaterMark
import cv2
from blind_watermark import WaterMarkCore
import numpy as np

# %%

bwm = WaterMark(password_img=1, password_wm=1)

# 读取原图
bwm.read_img('pic/ori_img.jpeg')

# 读取水印
wm = [True, False, True, False, True, False, True, False, True, False]
bwm.read_wm(wm, mode='bit')

# 打上盲水印
bwm.embed('output/embedded.png')

len_wm = len(wm)  # 解水印需要用到长度
ori_img_shape = cv2.imread('pic/ori_img.jpeg').shape[:2]  # 抗攻击需要知道原图的shape

# %% 解水印

# 注意设定水印的长宽wm_shape
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='bit')
print("不攻击的提取结果：", wm_extract)

assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%截屏攻击

loc = ((0.3, 0.1), (0.7, 0.9))

att.cut_att(input_filename='output/embedded.png', output_file_name='output/截屏攻击.png', loc=loc)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/截屏攻击.png', wm_shape=len_wm, mode='bit')
print("截屏攻击{loc}后的提取结果：".format(loc=loc), wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%
# 一次横向裁剪打击
r = 0.2
att.cut_att_width(input_filename='output/embedded.png', output_file_name='output/横向裁剪攻击.png', ratio=r)
att.anti_cut_att(input_filename='output/横向裁剪攻击.png', output_file_name='output/横向裁剪攻击_填补.png',
                 origin_shape=ori_img_shape)

# 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/横向裁剪攻击_填补.png', wm_shape=len_wm, mode='bit')
print(f"横向裁剪攻击r={r}后的提取结果：", wm_extract)

assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%一次纵向裁剪攻击
ratio = 0.2
att.cut_att_height(input_filename='output/embedded.png', output_file_name='output/纵向裁剪攻击.png', ratio=ratio)
att.anti_cut_att(input_filename='output/纵向裁剪攻击.png', output_file_name='output/纵向裁剪攻击_填补.png',
                 origin_shape=ori_img_shape)

# 提取
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/纵向裁剪攻击_填补.png', wm_shape=len_wm, mode='bit')
print(f"纵向裁剪攻击ratio={ratio}后的提取结果：", wm_extract)

assert np.all(wm == wm_extract), '提取水印和原水印不一致'
# %%椒盐攻击
ratio = 0.05
att.salt_pepper_att(input_filename='output/embedded.png', output_file_name='output/椒盐攻击.png', ratio=ratio)
# ratio是椒盐概率

# 提取
wm_extract = bwm1.extract('output/椒盐攻击.png', wm_shape=len_wm, mode='bit')
print(f"椒盐攻击ratio={ratio}后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%旋转攻击
att.rot_att(input_filename='output/embedded.png', output_file_name='output/旋转攻击.png', angle=45)
att.rot_att(input_filename='output/旋转攻击.png', output_file_name='output/旋转攻击_还原.png', angle=-45)

# 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/旋转攻击_还原.png', wm_shape=len_wm, mode='bit')
print("旋转攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%遮挡攻击
n = 60
att.shelter_att(input_filename='output/embedded.png', output_file_name='output/多遮挡攻击.png', ratio=0.1, n=n)

# 提取
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/多遮挡攻击.png', wm_shape=len_wm, mode='bit')
print(f"遮挡攻击{n}后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%缩放攻击
att.resize_att(input_filename='output/embedded.png', output_file_name='output/缩放攻击.png', out_shape=(800, 600))
att.resize_att(input_filename='output/缩放攻击.png', output_file_name='output/缩放攻击_还原.png', out_shape=ori_img_shape[::-1])
# out_shape 是分辨率，需要颠倒一下

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/缩放攻击_还原.png', wm_shape=len_wm, mode='bit')
print("缩放攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'
