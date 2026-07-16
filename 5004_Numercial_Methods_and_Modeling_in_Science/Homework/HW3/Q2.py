import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import dct, idct
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定义一个通用的滤波函数
def filter_signal(filename, keep_fraction, use_dct=False):
    # 读取数据
    data = np.loadtxt(filename)
    N = len(data)
    
    if not use_dct:
        # 使用标准实数快速傅里叶变换 (RFFT)
        c = np.fft.rfft(data)
        # 计算需要保留的系数个数
        keep_elements = int(len(c) * keep_fraction)
        # 将后面的高频系数全部清零 (Low-pass filter)
        c[keep_elements:] = 0
        # 逆变换回到时域
        smoothed = np.fft.irfft(c, n=N)
    else:
        # 使用离散余弦变换 (DCT)
        c = dct(data, norm='ortho')
        keep_elements = int(len(c) * keep_fraction)
        c[keep_elements:] = 0
        smoothed = idct(c, norm='ortho')
        
    return data, smoothed

# ---------------------------------------------------------
# Part (a) - (e): Process dow.txt
# ---------------------------------------------------------
# 获取原始数据、保留前 10% 系数平滑的数据、保留前 2% 系数平滑的数据
dow_data, dow_smooth_10 = filter_signal("dow.txt", 0.10)
_, dow_smooth_02 = filter_signal("dow.txt", 0.02)

plt.figure(figsize=(10, 5))
plt.plot(dow_data, label='Original Data', color='lightgray')
plt.plot(dow_smooth_10, label='10% FFT Smoothing', color='dodgerblue', alpha=0.8)
plt.plot(dow_smooth_02, label='2% FFT Smoothing', color='crimson')
plt.title("Dow Jones Smoothing (dow.txt)")
plt.xlabel("Business Days")
plt.ylabel("Closing Value")
plt.legend()
plt.grid(True, alpha=0.3)

# 保存第一张图 (dow.txt)
plt.savefig('q2_1.png', dpi=300, bbox_inches='tight')
plt.show()

# ---------------------------------------------------------
# Part (f) - (g): Process dow2.txt (FFT vs DCT)
# ---------------------------------------------------------
# 对比 dow2.txt 在 2% 保留率下，标准 FFT 和 DCT 的区别
dow2_data, dow2_fft = filter_signal("dow2.txt", 0.02, use_dct=False)
_, dow2_dct = filter_signal("dow2.txt", 0.02, use_dct=True)

plt.figure(figsize=(10, 5))
plt.plot(dow2_data, label='Original Data', color='lightgray')
plt.plot(dow2_fft, label='2% Standard FFT Smoothing', color='crimson', linestyle='--')
plt.plot(dow2_dct, label='2% DCT Smoothing', color='blue')
plt.title("Dow Jones Smoothing: FFT vs DCT (dow2.txt)")
plt.xlabel("Business Days")
plt.ylabel("Closing Value")
plt.legend()
plt.grid(True, alpha=0.3)

# 保存第二张图 (dow2.txt)
plt.savefig('q2_2.png', dpi=300, bbox_inches='tight')
plt.show()