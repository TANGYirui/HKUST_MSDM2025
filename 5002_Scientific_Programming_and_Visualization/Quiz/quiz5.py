import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 8))
ax = plt.axes(projection='3d', proj_type='persp')
ax.set_facecolor('white')

# 固定的靶子（在右边）
target_x = 25
circles = []
for radius in [1.5, 3, 4.5, 6]:
    u = np.linspace(0, 2 * np.pi, 50)
    ty = radius * np.cos(u)
    tz = radius * np.sin(u)
    tx = np.full_like(u, target_x)
    circle, = ax.plot(tx, ty, tz, 'r-', linewidth=2.5, alpha=0.8)
    circles.append(circle)

# 箭头的初始化
arrow_line, = ax.plot([], [], [], 'b-', linewidth=4)
arrow_head = ax.scatter([], [], [], c='blue', s=300, marker=(3, 0, -90), depthshade=False)

# 螺旋环的散点
spiral_scatter = ax.scatter([], [], [], c=[], s=30, cmap='rainbow')

# 羽毛（三片）
feathers = []

for color in ['blue', 'blue', 'blue']:
    feather, = ax.plot([], [], [], color=color, linewidth=3, alpha=0.7)
    feathers.append(feather)

# 击中文字
text_obj = ax.text(target_x + 2, 0, 7, '', fontsize=14, color='black', ha='left')


label_text = ax.text(0, 0, 0, 'spiral arrow', fontsize=12, color='black',
                     ha='center', va='bottom', zorder=10)

ax.set_xlim([-5, 30])
ax.set_ylim([-8, 8])
ax.set_zlim([-8, 8])
ax.set_box_aspect(aspect=(2, 1, 1))
ax.view_init(elev=10, azim=-90)


ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False


plt.title('', x=0.3, y=0.5, color="gray", size=14, ha='left')  # 可选：清空标题避免重复

# 动画参数
total_frames = 180
hit_shown = [False]  

def init():
    arrow_line.set_data([], [])
    arrow_line.set_3d_properties([])
    arrow_head._offsets3d = ([], [], [])
    spiral_scatter._offsets3d = ([], [], [])
    text_obj.set_text('')
    label_text.set_position_3d((0, 0, 0))  # 初始位置
    for feather in feathers:
        feather.set_data([], [])
        feather.set_3d_properties([])
    return [arrow_line, arrow_head, spiral_scatter, text_obj, label_text] + feathers

def animate(frame):
    progress = min(frame / 150, 1.0)
    arrow_x_start = -3
    arrow_x_end = target_x - 0.5
    
    arrow_pos = arrow_x_start + (arrow_x_end - arrow_x_start) * progress
    arrow_tail = arrow_pos - 8
    arrow_head_pos = arrow_pos
    
    # 箭杆
    arrow_line.set_data([arrow_tail, arrow_head_pos], [0, 0])
    arrow_line.set_3d_properties([0, 0])
    
    # 箭头
    arrow_head._offsets3d = ([arrow_head_pos], [0], [0])
    
    # 螺旋环的旋转
    rotation_speed = 0.3
    rotation = frame * rotation_speed
    
    n_loops = 4
    n_points = 150
    spiral_center = arrow_pos - 3
    spiral_x = np.linspace(spiral_center - 2, spiral_center + 2, n_points)
    t = np.linspace(0, n_loops * 2 * np.pi, n_points)
    radius = np.linspace(2.5, 0.3, n_points)
    spiral_y_base = radius * np.cos(t)
    spiral_z_base = radius * np.sin(t)
    cos_r = np.cos(rotation)
    sin_r = np.sin(rotation)
    spiral_y = spiral_y_base * cos_r - spiral_z_base * sin_r
    spiral_z = spiral_y_base * sin_r + spiral_z_base * cos_r
    spiral_scatter._offsets3d = (spiral_x, spiral_y, spiral_z)
    colors = np.linspace(1, 0, n_points)
    spiral_scatter.set_array(colors)
    
    # 羽毛（三片）
    feather_length = 2.5
    feather_width = 1.2
    for i, feather in enumerate(feathers):
        angle = rotation + i * (2 * np.pi / 3)
        fy = [0, feather_width * np.cos(angle)]
        fz = [0, feather_width * np.sin(angle)]
        fx = [arrow_tail, arrow_tail - feather_length]
        feather.set_data(fx, fy)
        feather.set_3d_properties(fz)

    # spiral arrow 标签
    arrow_mid_x = (arrow_tail + arrow_head_pos) / 2
    label_text.set_position_3d((arrow_mid_x, 0, 1.8))  # y=0 居中，z=1.8 在上方

    # 当箭头到达靶子时显示文字
    if progress >= 0.98 and not hit_shown[0]:
        text_obj.set_text('Hit the target!')
        hit_shown[0] = True 

    return [arrow_line, arrow_head, spiral_scatter, text_obj, label_text] + feathers

# 创建动画
anim = FuncAnimation(fig, animate, init_func=init, frames=total_frames, 
                    interval=40, blit=False, repeat=True)

plt.tight_layout()
plt.show()