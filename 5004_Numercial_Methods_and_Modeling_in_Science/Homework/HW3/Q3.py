import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------
# Part (a): 读入模糊照片并显示
# ---------------------------------------------------------
print("Loading blur.txt... This might take a few seconds.")
blur = np.loadtxt("blur.txt")
ny, nx = blur.shape # 获取图片的宽和高 (1024 x 1024)

plt.figure(figsize=(7, 7))
# 使用灰度图 cmap='gray'，原题提示：天空在上(亮)，地面在下(暗)
plt.imshow(blur, cmap='gray')
plt.title("Part (a): Original Blurred Photo")
plt.axis('off') # 去掉坐标轴更美观

# 保存第一张图
plt.savefig('q3_1.png', dpi=300, bbox_inches='tight')
plt.show()

# ---------------------------------------------------------
# Part (b): 构建高斯点扩散函数 (PSF)
# ---------------------------------------------------------
sigma = 25
# 创建中心对齐的网格坐标
x = np.arange(nx) - nx // 2
y = np.arange(ny) - ny // 2
X, Y = np.meshgrid(x, y)

# 计算高斯分布
gaussian = np.exp(-(X**2 + Y**2) / (2 * sigma**2))

# 核心步骤：将中心高斯平移到四个角落，满足周期性边界条件
psf = np.fft.ifftshift(gaussian)

plt.figure(figsize=(7, 7))
# 为了能看清角落的光斑，我们通过 vmax 限制一下显示的最高亮度
plt.imshow(psf, cmap='gray', vmax=np.max(psf)*0.01)
plt.title("Part (b): Point Spread Function (Corners)")
plt.axis('off')

# 保存第二张图
plt.savefig('q3_2.png', dpi=300, bbox_inches='tight')
plt.show()

# ---------------------------------------------------------
# Part (c): 频域除法去模糊 (Deconvolution)
# ---------------------------------------------------------
print("Performing 2D Fast Fourier Transforms...")
# 1. 把模糊图和 PSF 都转换到频域
blur_fft = np.fft.fft2(blur)
psf_fft = np.fft.fft2(psf)

# 2. 避免除以零的正则化处理 (Thresholding)
epsilon = 1e-3
deblurred_fft = np.copy(blur_fft) # 复制一份，用来存放还原后的频谱

# 创建一个布尔掩码 (Mask)：找出绝对值大于等于 epsilon 的位置
mask = np.abs(psf_fft) >= epsilon

# 只有在 PSF 频域系数足够大时，才进行除法；
# 对于小于 epsilon 的高频系数，题目要求 "leave that coefficient alone" (保持不变)
deblurred_fft[mask] = blur_fft[mask] / psf_fft[mask]

print("Performing Inverse FFT...")
# 3. 逆变换回空域，并取实部 (丢掉由于计算误差产生的极小虚部)
deblurred = np.fft.ifft2(deblurred_fft).real

plt.figure(figsize=(7, 7))
plt.imshow(deblurred, cmap='gray')
plt.title("Part (c): Deblurred Photo")
plt.axis('off')

# 保存第三张图
plt.savefig('q3_3.png', dpi=300, bbox_inches='tight')
plt.show()
print("Done! Three images saved.")