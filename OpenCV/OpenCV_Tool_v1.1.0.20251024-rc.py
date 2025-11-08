# ==============================================================================================================
# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk, StringVar
# import cv2
# import numpy as np
# from PIL import Image, ImageTk
# import os
#
#
# class ImageEditor:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("OpenCV图像调整工具")
#         self.root.geometry("1200x800")  # 初始窗口大小
#         self.root.configure(bg="#f0f0f0")
#
#         # 确保中文显示正常
#         self.style = ttk.Style()
#         self.style.configure("TLabel", font=("SimHei", 10))
#         self.style.configure("TButton", font=("SimHei", 10))
#         self.style.configure("TScale", font=("SimHei", 10))
#
#         # 图像变量（记录原图尺寸，避免缩放叠加）
#         self.original_image = None
#         self.original_height = 0  # 原图高度
#         self.original_width = 0  # 原图宽度
#         self.processed_image = None
#         self.image_path = None
#
#         # ---------------------- 新增：保存位数选择变量 ----------------------
#         self.save_bit_depth = StringVar(value="24bit")  # 默认24位RGB
#
#         # ---------------------- 核心修改1：左右分栏布局（左侧控制区+右侧图像区） ----------------------
#         # 主分栏容器（可拖动调整宽度）
#         self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
#         self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
#
#         # 左侧：控制区域（带滚动）
#         self.left_frame = ttk.Frame(self.main_pane, width=500)
#         self.main_pane.add(self.left_frame, weight=1)  # weight控制缩放比例
#
#         # 右侧：图像对比区域（固定，不滚动）
#         self.right_frame = ttk.Frame(self.main_pane, width=600)
#         self.main_pane.add(self.right_frame, weight=2)
#
#         # ---------------------- 左侧：滚动控制区 ----------------------
#         # 滚动容器搭建
#         scroll_canvas = tk.Canvas(self.left_frame, bg="#f0f0f0")
#         scroll_scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=scroll_canvas.yview)
#         self.scrollable_frame = ttk.Frame(scroll_canvas, padding=10)
#
#         # 滚动范围绑定
#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
#         )
#         scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
#         scroll_canvas.configure(yscrollcommand=scroll_scrollbar.set)
#
#         # 核心修改2：绑定鼠标滚轮事件（支持Windows/macOS）
#         scroll_canvas.bind_all("<MouseWheel>", lambda e: self.on_mouse_wheel(e, scroll_canvas))  # Windows
#         scroll_canvas.bind_all("<Button-4>", lambda e: self.on_mouse_wheel(e, scroll_canvas))   # macOS上滚
#         scroll_canvas.bind_all("<Button-5>", lambda e: self.on_mouse_wheel(e, scroll_canvas))   # macOS下滚
#
#         # 滚动组件布局
#         scroll_canvas.pack(side="left", fill="both", expand=True)
#         scroll_scrollbar.pack(side="right", fill="y")
#
#         # 左侧控制区内容（按钮+参数调整）
#         self.create_buttons()  # 按钮放在控制区最上方（已新增位数选择单选框）
#         self.create_control_area()  # 参数调整放在按钮下方
#
#         # ---------------------- 右侧：图像对比区域（固定） ----------------------
#         self.create_display_area()  # 原图+处理后图放在右侧
#
#         # 初始化参数和绑定事件
#         self.init_adjustment_parameters()
#         self.bind_adjustments()
#
#     def on_mouse_wheel(self, event, canvas):
#         """鼠标滚轮滚动事件处理"""
#         # Windows：event.delta为120（上滚）/-120（下滚）；macOS：event.num=4（上滚）/5（下滚）
#         if event.delta:
#             canvas.yview_scroll(-int(event.delta / 120), "units")  # Windows
#         else:
#             if event.num == 4:
#                 canvas.yview_scroll(-1, "units")  # macOS上滚
#             elif event.num == 5:
#                 canvas.yview_scroll(1, "units")   # macOS下滚
#
#     def create_display_area(self):
#         """创建图像显示区域（右侧固定，原图+处理后图上下排列）"""
#         display_frame = ttk.Frame(self.right_frame)
#         display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
#
#         # ---------------------- 原图显示区域（固定容器尺寸） ----------------------
#         original_frame = ttk.LabelFrame(display_frame, text="原图", padding=5)
#         original_frame.pack(fill=tk.BOTH, expand=True, pady=5)
#
#         # 固定尺寸容器（避免图像拉伸）
#         self.original_container = ttk.Frame(original_frame, width=550, height=350)
#         self.original_container.pack_propagate(False)  # 禁止容器随内容缩放
#         self.original_container.pack(fill=tk.BOTH, expand=True)
#
#         self.original_label = ttk.Label(self.original_container)
#         self.original_label.pack(fill=tk.BOTH, expand=True)
#
#         # ---------------------- 处理后图像显示区域（与原图容器尺寸一致） ----------------------
#         processed_frame = ttk.LabelFrame(display_frame, text="调整后", padding=5)
#         processed_frame.pack(fill=tk.BOTH, expand=True, pady=5)
#
#         self.processed_container = ttk.Frame(processed_frame, width=550, height=350)
#         self.processed_container.pack_propagate(False)
#         self.processed_container.pack(fill=tk.BOTH, expand=True)
#
#         self.processed_label = ttk.Label(self.processed_container)
#         self.processed_label.pack(fill=tk.BOTH, expand=True)
#
#     def create_control_area(self):
#         """创建控制区域（左侧滚动区内）"""
#         control_frame = ttk.LabelFrame(self.scrollable_frame, text="调整参数", padding=10)
#         control_frame.pack(fill=tk.X, pady=10)
#
#         self.notebook = ttk.Notebook(control_frame)
#         self.notebook.pack(fill=tk.X, expand=True)
#
#         # 标签页
#         self.basic_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.basic_frame, text="基本调整")
#         self.color_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.color_frame, text="颜色调整")
#         self.filter_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.filter_frame, text="滤镜效果")
#         self.geometry_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.geometry_frame, text="几何变换")
#         self.traditional_enhance_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.traditional_enhance_frame, text="传统图像增强")
#
#     def create_buttons(self):
#         """创建功能按钮（左侧滚动区最上方）- 新增“保存位数选择”单选框"""
#         button_frame = ttk.Frame(self.scrollable_frame)
#         button_frame.pack(fill=tk.X, pady=10)
#
#         # 加载按钮
#         self.load_btn = ttk.Button(button_frame, text="加载图像", command=self.load_image, width=12)
#         self.load_btn.pack(side=tk.LEFT, padx=10)
#
#         # 保存按钮
#         self.save_btn = ttk.Button(button_frame, text="保存图像", command=self.save_image, width=12)
#         self.save_btn.pack(side=tk.LEFT, padx=10)
#         self.save_btn.config(state=tk.DISABLED)
#
#         # 重置按钮
#         self.reset_btn = ttk.Button(button_frame, text="重置调整", command=self.reset_adjustments, width=12)
#         self.reset_btn.pack(side=tk.LEFT, padx=10)
#         self.reset_btn.config(state=tk.DISABLED)
#
#         # ---------------------- 新增：保存位数选择（单选框） ----------------------
#         bit_select_frame = ttk.Frame(button_frame)
#         bit_select_frame.pack(side=tk.LEFT, padx=20)
#
#         # 提示标签
#         bit_label = ttk.Label(bit_select_frame, text="保存位数：")
#         bit_label.pack(side=tk.LEFT, padx=5)
#
#         # 24位RGB单选框（默认选中）
#         rb_24bit = ttk.Radiobutton(bit_select_frame, text="24位RGB", variable=self.save_bit_depth, value="24bit")
#         rb_24bit.pack(side=tk.LEFT, padx=5)
#
#         # 8位灰度单选框
#         rb_8bit = ttk.Radiobutton(bit_select_frame, text="8位灰度", variable=self.save_bit_depth, value="8bit")
#         rb_8bit.pack(side=tk.LEFT, padx=5)
#
#     def init_adjustment_parameters(self):
#         """初始化调整参数（不变）"""
#         # 原有参数
#         self.brightness = tk.IntVar(value=0)
#         self.contrast = tk.IntVar(value=100)
#         self.gamma = tk.DoubleVar(value=1.0)
#         self.hue = tk.IntVar(value=0)
#         self.saturation = tk.IntVar(value=100)
#         self.value = tk.IntVar(value=100)
#         self.red = tk.IntVar(value=0)
#         self.green = tk.IntVar(value=0)
#         self.blue = tk.IntVar(value=0)
#         self.blur_amount = tk.IntVar(value=0)
#         self.sharpen_amount = tk.IntVar(value=0)
#         self.edge_detection = tk.IntVar(value=0)
#         self.threshold = tk.IntVar(value=0)
#         self.gray_scale = tk.BooleanVar(value=False)
#         self.rotation = tk.IntVar(value=0)
#         self.zoom = tk.IntVar(value=100)
#         self.flip_horizontal = tk.BooleanVar(value=False)
#         self.flip_vertical = tk.BooleanVar(value=False)
#
#         # 传统图像增强参数
#         self.gray_corr_a = tk.DoubleVar(value=1.0)
#         self.gray_corr_b = tk.IntVar(value=0)
#         self.gray_corr_enable = tk.BooleanVar(value=False)
#         self.he_type = StringVar(value="全局HE")
#         self.clahe_clip = tk.DoubleVar(value=2.0)
#         self.he_enable = tk.BooleanVar(value=False)
#         self.gray_world_enable = tk.BooleanVar(value=False)
#         self.retinex_sigma = tk.IntVar(value=100)
#         self.retinex_enable = tk.BooleanVar(value=False)
#         self.stretch_in_low = tk.IntVar(value=0)
#         self.stretch_in_high = tk.IntVar(value=255)
#         self.stretch_enable = tk.BooleanVar(value=False)
#         self.smooth_type = StringVar(value="均值滤波")
#         self.smooth_kernel = tk.IntVar(value=3)
#         self.smooth_enable = tk.BooleanVar(value=False)
#         self.sharpen_type = StringVar(value="拉普拉斯")
#         self.sharpen_strength = tk.DoubleVar(value=1.0)
#         self.sharpen_enable = tk.BooleanVar(value=False)
#
#         # 高通滤波参数（不变，与原逻辑共用同一强度参数）
#         self.highpass_strength = tk.DoubleVar(value=1.0)
#         self.highpass_enable = tk.BooleanVar(value=False)
#
#         # 灰度级修正（伽马）参数
#         self.gamma_corr_value = tk.DoubleVar(value=1.0)
#         self.gamma_corr_enable = tk.BooleanVar(value=False)
#
#         # 创建滑动条
#         self.create_sliders()
#
#     def create_sliders(self):
#         """创建所有滑动条（不变）"""
#         # 基本调整
#         self.create_slider(self.basic_frame, "亮度", self.brightness, -100, 100, 1)
#         self.create_slider(self.basic_frame, "对比度", self.contrast, 0, 200, 1)
#         self.create_slider(self.basic_frame, "伽马校正", self.gamma, 0.1, 3.0, 0.1)
#         # 颜色调整
#         self.create_slider(self.color_frame, "色调", self.hue, -180, 180, 1)
#         self.create_slider(self.color_frame, "饱和度", self.saturation, 0, 200, 1)
#         self.create_slider(self.color_frame, "明度", self.value, 0, 200, 1)
#         self.create_slider(self.color_frame, "红色通道", self.red, -100, 100, 1)
#         self.create_slider(self.color_frame, "绿色通道", self.green, -100, 100, 1)
#         self.create_slider(self.color_frame, "蓝色通道", self.blue, -100, 100, 1)
#         # 滤镜效果
#         self.create_slider(self.filter_frame, "模糊程度", self.blur_amount, 0, 20, 1)
#         self.create_slider(self.filter_frame, "锐化程度", self.sharpen_amount, 0, 10, 1)
#         self.create_slider(self.filter_frame, "边缘检测", self.edge_detection, 0, 1, 1)
#         self.create_slider(self.filter_frame, "阈值处理", self.threshold, 0, 255, 1)
#         gray_check = ttk.Checkbutton(self.filter_frame, text="灰度图", variable=self.gray_scale)
#         gray_check.pack(anchor=tk.W, pady=5)
#         # 几何变换
#         self.create_slider(self.geometry_frame, "旋转角度", self.rotation, 0, 360, 1)
#         self.create_slider(self.geometry_frame, "缩放比例(%)", self.zoom, 10, 200, 1)
#         flip_h_check = ttk.Checkbutton(self.geometry_frame, text="水平翻转", variable=self.flip_horizontal)
#         flip_h_check.pack(anchor=tk.W, pady=5)
#         flip_v_check = ttk.Checkbutton(self.geometry_frame, text="垂直翻转", variable=self.flip_vertical)
#         flip_v_check.pack(anchor=tk.W, pady=5)
#         # 传统图像增强
#         te_frame = self.traditional_enhance_frame
#         ttk.Label(te_frame, text="=== 1. 灰度级修正（线性变换）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用灰度级修正", variable=self.gray_corr_enable).pack(anchor=tk.W, pady=2)
#         self.create_slider(te_frame, "斜率(对比度)", self.gray_corr_a, 0.1, 3.0, 0.1)
#         self.create_slider(te_frame, "截距(亮度)", self.gray_corr_b, -50, 50, 1)
#
#         ttk.Label(te_frame, text="=== 2. 灰度级修正（伽马）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用伽马校正", variable=self.gamma_corr_enable).pack(anchor=tk.W, pady=2)
#         self.create_slider(te_frame, "伽马值", self.gamma_corr_value, 0.1, 3.0, 0.1)
#
#         ttk.Label(te_frame, text="=== 3. 直方图均衡化 ===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用直方图均衡化", variable=self.he_enable).pack(anchor=tk.W, pady=2)
#         he_type_frame = ttk.Frame(te_frame)
#         he_type_frame.pack(anchor=tk.W, pady=2)
#         ttk.Label(he_type_frame, text="均衡化类型", width=15).pack(side=tk.LEFT)
#         he_type_combo = ttk.Combobox(he_type_frame, textvariable=self.he_type, values=["全局HE", "CLAHE"], state="readonly")
#         he_type_combo.pack(side=tk.LEFT)
#         self.create_slider(te_frame, "CLAHE对比度限制", self.clahe_clip, 1.0, 10.0, 0.1)
#
#         ttk.Label(te_frame, text="=== 4. 灰度世界算法（自动白平衡）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用灰度世界算法", variable=self.gray_world_enable).pack(anchor=tk.W, pady=2)
#
#         ttk.Label(te_frame, text="=== 5. Retinex算法（单尺度）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用Retinex", variable=self.retinex_enable).pack(anchor=tk.W, pady=2)
#         self.create_slider(te_frame, "高斯核Sigma", self.retinex_sigma, 50, 200, 1)
#
#         ttk.Label(te_frame, text="=== 6. 对比度拉伸 ===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用对比度拉伸", variable=self.stretch_enable).pack(anchor=tk.W, pady=2)
#         self.create_slider(te_frame, "输入低阈值", self.stretch_in_low, 0, 200, 1)
#         self.create_slider(te_frame, "输入高阈值", self.stretch_in_high, 55, 255, 1)
#
#         ttk.Label(te_frame, text="=== 7. 平滑滤波 ===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用平滑滤波", variable=self.smooth_enable).pack(anchor=tk.W, pady=2)
#         smooth_type_frame = ttk.Frame(te_frame)
#         smooth_type_frame.pack(anchor=tk.W, pady=2)
#         ttk.Label(smooth_type_frame, text="滤波类型", width=15).pack(side=tk.LEFT)
#         smooth_type_combo = ttk.Combobox(smooth_type_frame, textvariable=self.smooth_type,
#                                          values=["均值滤波", "中值滤波", "高斯滤波"], state="readonly")
#         smooth_type_combo.pack(side=tk.LEFT)
#         self.create_slider(te_frame, "核大小（奇数）", self.smooth_kernel, 1, 11, 1)
#
#         ttk.Label(te_frame, text="=== 8. 锐化滤波（拉普拉斯/Sobel）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用锐化滤波", variable=self.sharpen_enable).pack(anchor=tk.W, pady=2)
#         sharpen_type_frame = ttk.Frame(te_frame)
#         sharpen_type_frame.pack(anchor=tk.W, pady=2)
#         ttk.Label(sharpen_type_frame, text="锐化类型", width=15).pack(side=tk.LEFT)
#         sharpen_type_combo = ttk.Combobox(sharpen_type_frame, textvariable=self.sharpen_type,
#                                           values=["拉普拉斯", "Sobel X", "Sobel Y"], state="readonly")
#         sharpen_type_combo.pack(side=tk.LEFT)
#         self.create_slider(te_frame, "锐化强度", self.sharpen_strength, 0.1, 5.0, 0.1)
#
#         ttk.Label(te_frame, text="=== 9. 锐化滤波（高通）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
#         ttk.Checkbutton(te_frame, text="启用高通锐化", variable=self.highpass_enable).pack(anchor=tk.W, pady=2)
#         self.create_slider(te_frame, "高通强度", self.highpass_strength, 0.1, 5.0, 0.1)
#
#     def create_slider(self, parent, label_text, variable, from_, to, resolution):
#         """创建滑动条（不变）"""
#         frame = ttk.Frame(parent)
#         frame.pack(fill=tk.X, pady=3)
#
#         label = ttk.Label(frame, text=label_text, width=15)
#         label.pack(side=tk.LEFT, padx=5)
#
#         slider = tk.Scale(frame, variable=variable, from_=from_, to=to,
#                           orient=tk.HORIZONTAL, length=300, resolution=resolution)
#         slider.pack(side=tk.LEFT, padx=5)
#
#         value_label = ttk.Label(frame, textvariable=variable, width=10)
#         value_label.pack(side=tk.LEFT, padx=5)
#
#     def bind_adjustments(self):
#         """绑定调整事件（不变）"""
#         # 原有绑定
#         self.brightness.trace_add("write", self.update_image)
#         self.contrast.trace_add("write", self.update_image)
#         self.gamma.trace_add("write", self.update_image)
#         self.hue.trace_add("write", self.update_image)
#         self.saturation.trace_add("write", self.update_image)
#         self.value.trace_add("write", self.update_image)
#         self.red.trace_add("write", self.update_image)
#         self.green.trace_add("write", self.update_image)
#         self.blue.trace_add("write", self.update_image)
#         self.blur_amount.trace_add("write", self.update_image)
#         self.sharpen_amount.trace_add("write", self.update_image)
#         self.edge_detection.trace_add("write", self.update_image)
#         self.threshold.trace_add("write", self.update_image)
#         self.gray_scale.trace_add("write", self.update_image)
#         self.rotation.trace_add("write", self.update_image)
#         self.zoom.trace_add("write", self.update_image)
#         self.flip_horizontal.trace_add("write", self.update_image)
#         self.flip_vertical.trace_add("write", self.update_image)
#         # 传统增强绑定
#         self.gray_corr_a.trace_add("write", self.update_image)
#         self.gray_corr_b.trace_add("write", self.update_image)
#         self.gray_corr_enable.trace_add("write", self.update_image)
#         self.he_type.trace_add("write", self.update_image)
#         self.clahe_clip.trace_add("write", self.update_image)
#         self.he_enable.trace_add("write", self.update_image)
#         self.gray_world_enable.trace_add("write", self.update_image)
#         self.retinex_sigma.trace_add("write", self.update_image)
#         self.retinex_enable.trace_add("write", self.update_image)
#         self.stretch_in_low.trace_add("write", self.update_image)
#         self.stretch_in_high.trace_add("write", self.update_image)
#         self.stretch_enable.trace_add("write", self.update_image)
#         self.smooth_type.trace_add("write", self.update_image)
#         self.smooth_kernel.trace_add("write", self.update_image)
#         self.smooth_enable.trace_add("write", self.update_image)
#         self.sharpen_type.trace_add("write", self.update_image)
#         self.sharpen_strength.trace_add("write", self.update_image)
#         self.sharpen_enable.trace_add("write", self.update_image)
#         # 伽马校正绑定
#         self.gamma_corr_value.trace_add("write", self.update_image)
#         self.gamma_corr_enable.trace_add("write", self.update_image)
#         # 高通滤波绑定（不变）
#         self.highpass_strength.trace_add("write", self.update_image)
#         self.highpass_enable.trace_add("write", self.update_image)
#
#     # ---------------------- 加载图像（不变） ----------------------
#     def load_image(self):
#         try:
#             file_path = filedialog.askopenfilename(filetypes=[("图像文件", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
#             if file_path:
#                 self.image_path = file_path
#                 self.original_image = cv2.imread(file_path)
#                 self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
#                 self.original_height, self.original_width = self.original_image.shape[:2]
#                 self.reset_adjustments()
#                 self.display_image()
#                 self.save_btn.config(state=tk.NORMAL)
#                 self.reset_btn.config(state=tk.NORMAL)
#         except Exception as e:
#             messagebox.showerror("错误", f"加载图像失败: {str(e)}")
#
#     def display_image(self):
#         """显示图像（基于右侧固定容器尺寸）"""
#         if self.original_image is not None:
#             # 显示原图
#             original_img = self.resize_image(self.original_image)
#             original_photo = ImageTk.PhotoImage(image=original_img)
#             self.original_label.config(image=original_photo)
#             self.original_label.image = original_photo
#             # 显示处理后图像
#             self.update_image()
#
#     def resize_image(self, image):
#         """基于右侧固定容器尺寸缩放（不变）"""
#         container_width = self.original_container.winfo_width() or 550
#         container_height = self.original_container.winfo_height() or 350
#
#         height, width = image.shape[:2]
#         ratio = min(container_width / width, container_height / height)
#
#         new_size = (int(width * ratio), int(height * ratio))
#         resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
#
#         return Image.fromarray(resized_image)
#
#     # ---------------------- 几何变换（不变） ----------------------
#     def apply_geometric_transformations(self, img):
#         rotation = self.rotation.get()
#         if rotation != 0:
#             center = (self.original_width // 2, self.original_height // 2)
#             matrix = cv2.getRotationMatrix2D(center, rotation, 1)
#             img = cv2.warpAffine(img, matrix, (self.original_width, self.original_height))
#
#         zoom = self.zoom.get() / 100.0
#         if zoom != 1.0:
#             new_width = int(self.original_width * zoom)
#             new_height = int(self.original_height * zoom)
#             img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
#
#         flip_code = -1
#         if self.flip_horizontal.get() and self.flip_vertical.get():
#             flip_code = -1
#         elif self.flip_horizontal.get():
#             flip_code = 1
#         elif self.flip_vertical.get():
#             flip_code = 0
#         if flip_code != -1:
#             img = cv2.flip(img, flip_code)
#
#         return img
#
#     # ---------------------- 更新图像（不变） ----------------------
#     def update_image(self, *args):
#         if self.original_image is None:
#             return
#         try:
#             img = self.original_image.copy()
#
#             # 处理顺序（不变，高通滤波仍在原有位置）
#             img = self.adjust_brightness_contrast(img)
#             img = self.adjust_gamma(img)
#             img = self.adjust_color_channels(img)
#             img = self.adjust_hsv(img)
#             img = self.apply_filters(img)
#             img = self.apply_gray_level_correction(img)
#             img = self.apply_gamma_correction(img)
#             img = self.apply_contrast_stretch(img)
#             img = self.apply_smoothing_filter(img)
#             img = self.apply_sharpening_filter(img)
#             img = self.apply_highpass_filter(img)  # 调用修改后的高通滤波方法
#             img = self.apply_histogram_equalization(img)
#             img = self.apply_gray_world(img)
#             img = self.apply_retinex(img)
#             img = self.apply_geometric_transformations(img)
#
#             self.processed_image = img
#             processed_img = self.resize_image(img)
#             processed_photo = ImageTk.PhotoImage(image=processed_img)
#             self.processed_label.config(image=processed_photo)
#             self.processed_label.image = processed_photo
#
#         except Exception as e:
#             print(f"图像处理错误: {str(e)}")
#             messagebox.showerror("错误", f"图像处理失败: {str(e)}")
#
#     # ---------------------- 原有工具方法（修改save_image以支持位数选择） ----------------------
#     def adjust_brightness_contrast(self, img):
#         brightness = self.brightness.get()
#         contrast = self.contrast.get() / 100.0
#         if brightness != 0 or contrast != 1.0:
#             img = np.clip(contrast * img + brightness, 0, 255).astype(np.uint8)
#         return img
#
#     def adjust_gamma(self, img):
#         gamma = self.gamma.get()
#         if gamma != 1.0:
#             table = np.array([((i / 255.0) ** (1 / gamma)) * 255 for i in range(256)]).astype("uint8")
#             img = cv2.LUT(img, table)
#         return img
#
#     def adjust_color_channels(self, img):
#         r, g, b = cv2.split(img)
#         red = self.red.get()
#         if red != 0:
#             r = np.clip(r + red, 0, 255).astype(np.uint8)
#         green = self.green.get()
#         if green != 0:
#             g = np.clip(g + green, 0, 255).astype(np.uint8)
#         blue = self.blue.get()
#         if blue != 0:
#             b = np.clip(b + blue, 0, 255).astype(np.uint8)
#         return cv2.merge([r, g, b])
#
#     def adjust_hsv(self, img):
#         hue = self.hue.get()
#         saturation = self.saturation.get() / 100.0
#         value = self.value.get() / 100.0
#         if hue != 0 or saturation != 1.0 or value != 1.0:
#             hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
#             h, s, v = cv2.split(hsv)
#             h = (h + hue) % 180
#             s = np.clip(s * saturation, 0, 255).astype(np.uint8)
#             v = np.clip(v * value, 0, 255).astype(np.uint8)
#             img = cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2RGB)
#         return img
#
#     def apply_filters(self, img):
#         if self.gray_scale.get():
#             img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
#         blur = self.blur_amount.get()
#         if blur > 0:
#             img = cv2.GaussianBlur(img, (2 * blur + 1, 2 * blur + 1), 0)
#         sharpen = self.sharpen_amount.get()
#         if sharpen > 0:
#             kernel = np.array([[-1, -1, -1], [-1, 9 + sharpen, -1], [-1, -1, -1]])
#             img = np.clip(cv2.filter2D(img, -1, kernel), 0, 255).astype(np.uint8)
#         if self.edge_detection.get() == 1:
#             img = cv2.cvtColor(cv2.Canny(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), 100, 200), cv2.COLOR_GRAY2RGB)
#         threshold = self.threshold.get()
#         if threshold > 0:
#             _, img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), threshold, 255, cv2.THRESH_BINARY)
#             img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
#         return img
#
#     # ---------------------- 核心修改：支持24位/8位保存 ----------------------
#     def save_image(self):
#         if self.processed_image is None:
#             messagebox.showwarning("警告", "没有可保存的图像")
#             return
#         try:
#             # 1. 确定保存文件名（根据位数添加后缀）
#             if self.image_path:
#                 dir_name, file_name = os.path.split(self.image_path)
#                 base_name, ext = os.path.splitext(file_name)
#                 if self.save_bit_depth.get() == "8bit":
#                     default_path = os.path.join(dir_name, f"{base_name}_edited_8bit{ext}")
#                 else:
#                     default_path = os.path.join(dir_name, f"{base_name}_edited{ext}")
#             else:
#                 default_path = "edited_image_8bit.png" if self.save_bit_depth.get() == "8bit" else "edited_image.png"
#
#             # 2. 选择保存路径
#             save_path = filedialog.asksaveasfilename(defaultextension=".png",
#                                                      filetypes=[("PNG文件", "*.png"), ("JPEG文件", "*.jpg"),
#                                                                 ("BMP文件", "*.bmp")],
#                                                      initialfile=default_path)
#             if not save_path:
#                 return
#
#             # 3. 根据选择的位数处理图像
#             if self.save_bit_depth.get() == "8bit":
#                 # 8位：转为单通道灰度图（cv2自动识别为8位）
#                 img_to_save = cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2GRAY)
#                 cv2.imwrite(save_path, img_to_save)
#                 messagebox.showinfo("成功", f"8位灰度图已保存至:\n{save_path}")
#             else:
#                 # 24位：保留RGB三通道（原有逻辑）
#                 img_to_save = cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR)
#                 cv2.imwrite(save_path, img_to_save)
#                 messagebox.showinfo("成功", f"24位RGB图已保存至:\n{save_path}")
#
#         except Exception as e:
#             messagebox.showerror("错误", f"保存图像失败: {str(e)}")
#
#     # 传统图像增强方法（不变）
#     def apply_gray_level_correction(self, img):
#         if not self.gray_corr_enable.get():
#             return img
#         try:
#             a = self.gray_corr_a.get()
#             b = self.gray_corr_b.get()
#             corrected = np.clip(a * img + b, 0, 255).astype(np.uint8)
#             return corrected
#         except Exception as e:
#             print(f"灰度级修正错误: {str(e)}")
#             return img
#
#     def apply_gamma_correction(self, img):
#         if not self.gamma_corr_enable.get():
#             return img
#         try:
#             gamma = self.gamma_corr_value.get()
#             if gamma <= 0:
#                 gamma = 0.1
#             img_float = img.astype(np.float32) / 255.0
#             corrected = np.power(img_float, gamma) * 255.0
#             return corrected.astype(np.uint8)
#         except Exception as e:
#             print(f"伽马校正错误: {str(e)}")
#             return img
#
#     def apply_histogram_equalization(self, img):
#         if not self.he_enable.get():
#             return img
#         try:
#             he_type = self.he_type.get()
#             if len(img.shape) == 3:
#                 hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
#                 h, s, v = cv2.split(hsv)
#                 if he_type == "全局HE":
#                     v_eq = cv2.equalizeHist(v)
#                 else:
#                     clahe = cv2.createCLAHE(clipLimit=self.clahe_clip.get(), tileGridSize=(8, 8))
#                     v_eq = clahe.apply(v)
#                 return cv2.cvtColor(cv2.merge([h, s, v_eq]), cv2.COLOR_HSV2RGB)
#             else:
#                 if he_type == "全局HE":
#                     return cv2.equalizeHist(img)
#                 else:
#                     clahe = cv2.createCLAHE(clipLimit=self.clahe_clip.get(), tileGridSize=(8, 8))
#                     return clahe.apply(img)
#         except Exception as e:
#             print(f"直方图均衡化错误: {str(e)}")
#             return img
#
#     def apply_gray_world(self, img):
#         if not self.gray_world_enable.get() or len(img.shape) != 3:
#             return img
#         try:
#             r_mean = np.mean(img[:, :, 0])
#             g_mean = np.mean(img[:, :, 1])
#             b_mean = np.mean(img[:, :, 2])
#             gray_mean = (r_mean + g_mean + b_mean) / 3
#             img[:, :, 0] = np.clip(img[:, :, 0] * (gray_mean / r_mean), 0, 255).astype(np.uint8)
#             img[:, :, 1] = np.clip(img[:, :, 1] * (gray_mean / g_mean), 0, 255).astype(np.uint8)
#             img[:, :, 2] = np.clip(img[:, :, 2] * (gray_mean / b_mean), 0, 255).astype(np.uint8)
#             return img
#         except Exception as e:
#             print(f"灰度世界算法错误: {str(e)}")
#             return img
#
#     def apply_retinex(self, img):
#         if not self.retinex_enable.get():
#             return img
#         try:
#             sigma = self.retinex_sigma.get()
#             img_float = img.astype(np.float32) / 255.0
#             blur = cv2.GaussianBlur(img_float, (0, 0), sigma)
#             retinex = np.log1p(img_float) - np.log1p(blur)
#             retinex = (retinex - np.min(retinex)) / (np.max(retinex) - np.min(retinex))
#             return (retinex * 255).astype(np.uint8)
#         except Exception as e:
#             print(f"Retinex算法错误: {str(e)}")
#             return img
#
#     def apply_contrast_stretch(self, img):
#         if not self.stretch_enable.get():
#             return img
#         try:
#             in_low = self.stretch_in_low.get()
#             in_high = self.stretch_in_high.get()
#             if in_low >= in_high:
#                 in_low, in_high = 0, 255
#             stretched = np.clip((img - in_low) / (in_high - in_low) * 255, 0, 255).astype(np.uint8)
#             return stretched
#         except Exception as e:
#             print(f"对比度拉伸错误: {str(e)}")
#             return img
#
#     def apply_smoothing_filter(self, img):
#         if not self.smooth_enable.get():
#             return img
#         try:
#             kernel = self.smooth_kernel.get()
#             kernel = kernel if kernel % 2 == 1 else kernel + 1
#             kernel = max(1, kernel)
#
#             if self.smooth_type.get() == "均值滤波":
#                 return cv2.blur(img, (kernel, kernel))
#             elif self.smooth_type.get() == "中值滤波":
#                 return cv2.medianBlur(img, kernel)
#             elif self.smooth_type.get() == "高斯滤波":
#                 return cv2.GaussianBlur(img, (kernel, kernel), 0)
#         except Exception as e:
#             print(f"平滑滤波错误: {str(e)}")
#             return img
#
#     def apply_sharpening_filter(self, img):
#         if not self.sharpen_enable.get():
#             return img
#         try:
#             strength = self.sharpen_strength.get()
#             if self.sharpen_type.get() == "拉普拉斯":
#                 laplacian = cv2.Laplacian(img, cv2.CV_64F)
#                 img = np.clip(img - strength * laplacian, 0, 255).astype(np.uint8)
#             else:
#                 if self.sharpen_type.get() == "Sobel X":
#                     sobel = cv2.Sobel(img, cv2.CV_64F, dx=1, dy=0)
#                 else:
#                     sobel = cv2.Sobel(img, cv2.CV_64F, dx=0, dy=1)
#                 img = np.clip(img + strength * np.abs(sobel), 0, 255).astype(np.uint8)
#             return img
#         except Exception as e:
#             print(f"锐化滤波错误: {str(e)}")
#             return img
#
#     # ---------------------- 核心修改：替换高通滤波逻辑（高斯低通减影） ----------------------
#     def apply_highpass_filter(self, img):
#         if not self.highpass_enable.get():
#             return img
#         try:
#             strength = self.highpass_strength.get()
#             # 1. 对图像做高斯模糊，提取低频成分（与第二份代码逻辑一致）
#             gaussian = cv2.GaussianBlur(img, (5, 5), 0)
#             # 2. 加权混合：原图*(1+强度) - 低频图*强度 → 突出高频边缘
#             high_pass = cv2.addWeighted(img, 1.0 + strength, gaussian, -strength, 0)
#             # 3. 处理数值溢出，确保像素值在0-255范围
#             img = cv2.convertScaleAbs(high_pass)
#             return img
#         except Exception as e:
#             print(f"高通滤波错误: {str(e)}")
#             return img
#
#     def reset_adjustments(self):
#         """重置所有参数（不变）"""
#         self.brightness.set(0)
#         self.contrast.set(100)
#         self.gamma.set(1.0)
#         self.hue.set(0)
#         self.saturation.set(100)
#         self.value.set(100)
#         self.red.set(0)
#         self.green.set(0)
#         self.blue.set(0)
#         self.blur_amount.set(0)
#         self.sharpen_amount.set(0)
#         self.edge_detection.set(0)
#         self.threshold.set(0)
#         self.gray_scale.set(False)
#         self.rotation.set(0)
#         self.zoom.set(100)
#         self.flip_horizontal.set(False)
#         self.flip_vertical.set(False)
#
#         self.gray_corr_a.set(1.0)
#         self.gray_corr_b.set(0)
#         self.gray_corr_enable.set(False)
#         self.he_type.set("全局HE")
#         self.clahe_clip.set(2.0)
#         self.he_enable.set(False)
#         self.gray_world_enable.set(False)
#         self.retinex_sigma.set(100)
#         self.retinex_enable.set(False)
#         self.stretch_in_low.set(0)
#         self.stretch_in_high.set(255)
#         self.stretch_enable.set(False)
#         self.smooth_type.set("均值滤波")
#         self.smooth_kernel.set(3)
#         self.smooth_enable.set(False)
#         self.sharpen_type.set("拉普拉斯")
#         self.sharpen_strength.set(1.0)
#         self.sharpen_enable.set(False)
#
#         self.gamma_corr_value.set(1.0)
#         self.gamma_corr_enable.set(False)
#         self.highpass_strength.set(1.0)
#         self.highpass_enable.set(False)
#
#         # 重置保存位数选择（默认24位）
#         self.save_bit_depth.set("24bit")
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ImageEditor(root)
#     root.mainloop()


# ==============================================================================================================
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, StringVar
import cv2
import numpy as np
from PIL import Image, ImageTk
import os


class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenCV图像调整工具")
        self.root.geometry("1200x800")  # 初始窗口大小
        self.root.configure(bg="#f0f0f0")

        # 确保中文显示正常
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TScale", font=("SimHei", 10))

        # 图像变量（记录原图尺寸，避免缩放叠加）
        self.original_image = None
        self.original_height = 0  # 原图高度
        self.original_width = 0  # 原图宽度
        self.processed_image = None
        self.image_path = None

        # ---------------------- 新增：保存位数选择变量 ----------------------
        self.save_bit_depth = StringVar(value="24bit")  # 默认24位RGB

        # ---------------------- 核心修改：平滑滤波新增sigma参数（高斯滤波专用） ----------------------
        self.smooth_sigma = tk.DoubleVar(value=1.0)  # 高斯滤波标准差，0.1步进
        self.sigma_slider_frame = None  # 存储sigma滑动条容器，用于动态显示/隐藏

        # ---------------------- 核心修改1：左右分栏布局（左侧控制区+右侧图像区） ----------------------
        # 主分栏容器（可拖动调整宽度）
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左侧：控制区域（带滚动）
        self.left_frame = ttk.Frame(self.main_pane, width=500)
        self.main_pane.add(self.left_frame, weight=1)  # weight控制缩放比例

        # 右侧：图像对比区域（固定，不滚动）
        self.right_frame = ttk.Frame(self.main_pane, width=600)
        self.main_pane.add(self.right_frame, weight=2)

        # ---------------------- 左侧：滚动控制区 ----------------------
        # 滚动容器搭建
        scroll_canvas = tk.Canvas(self.left_frame, bg="#f0f0f0")
        scroll_scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=scroll_canvas.yview)
        self.scrollable_frame = ttk.Frame(scroll_canvas, padding=10)

        # 滚动范围绑定
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        )
        scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scroll_scrollbar.set)

        # 核心修改2：绑定鼠标滚轮事件（支持Windows/macOS）
        scroll_canvas.bind_all("<MouseWheel>", lambda e: self.on_mouse_wheel(e, scroll_canvas))  # Windows
        scroll_canvas.bind_all("<Button-4>", lambda e: self.on_mouse_wheel(e, scroll_canvas))   # macOS上滚
        scroll_canvas.bind_all("<Button-5>", lambda e: self.on_mouse_wheel(e, scroll_canvas))   # macOS下滚

        # 滚动组件布局
        scroll_canvas.pack(side="left", fill="both", expand=True)
        scroll_scrollbar.pack(side="right", fill="y")

        # 左侧控制区内容（按钮+参数调整）
        self.create_buttons()  # 按钮放在控制区最上方（已新增位数选择单选框）
        self.create_control_area()  # 参数调整放在按钮下方

        # ---------------------- 右侧：图像对比区域（固定） ----------------------
        self.create_display_area()  # 原图+处理后图放在右侧

        # 初始化参数和绑定事件
        self.init_adjustment_parameters()
        self.bind_adjustments()
        # 初始化时根据默认滤波类型（均值）隐藏sigma滑动条
        self.update_sigma_slider_visibility()

    def on_mouse_wheel(self, event, canvas):
        """鼠标滚轮滚动事件处理"""
        # Windows：event.delta为120（上滚）/-120（下滚）；macOS：event.num=4（上滚）/5（下滚）
        if event.delta:
            canvas.yview_scroll(-int(event.delta / 120), "units")  # Windows
        else:
            if event.num == 4:
                canvas.yview_scroll(-1, "units")  # macOS上滚
            elif event.num == 5:
                canvas.yview_scroll(1, "units")   # macOS下滚

    def create_display_area(self):
        """创建图像显示区域（右侧固定，原图+处理后图上下排列）"""
        display_frame = ttk.Frame(self.right_frame)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # ---------------------- 原图显示区域（固定容器尺寸） ----------------------
        original_frame = ttk.LabelFrame(display_frame, text="原图", padding=5)
        original_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 固定尺寸容器（避免图像拉伸）
        self.original_container = ttk.Frame(original_frame, width=550, height=350)
        self.original_container.pack_propagate(False)  # 禁止容器随内容缩放
        self.original_container.pack(fill=tk.BOTH, expand=True)

        self.original_label = ttk.Label(self.original_container)
        self.original_label.pack(fill=tk.BOTH, expand=True)

        # ---------------------- 处理后图像显示区域（与原图容器尺寸一致） ----------------------
        processed_frame = ttk.LabelFrame(display_frame, text="调整后", padding=5)
        processed_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.processed_container = ttk.Frame(processed_frame, width=550, height=350)
        self.processed_container.pack_propagate(False)
        self.processed_container.pack(fill=tk.BOTH, expand=True)

        self.processed_label = ttk.Label(self.processed_container)
        self.processed_label.pack(fill=tk.BOTH, expand=True)

    def create_control_area(self):
        """创建控制区域（左侧滚动区内）"""
        control_frame = ttk.LabelFrame(self.scrollable_frame, text="调整参数", padding=10)
        control_frame.pack(fill=tk.X, pady=10)

        self.notebook = ttk.Notebook(control_frame)
        self.notebook.pack(fill=tk.X, expand=True)

        # 标签页
        self.basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_frame, text="基本调整")
        self.color_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.color_frame, text="颜色调整")
        self.filter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.filter_frame, text="滤镜效果")
        self.geometry_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.geometry_frame, text="几何变换")
        self.traditional_enhance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.traditional_enhance_frame, text="传统图像增强")

    def create_buttons(self):
        """创建功能按钮（左侧滚动区最上方）- 新增“保存位数选择”单选框"""
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # 加载按钮
        self.load_btn = ttk.Button(button_frame, text="加载图像", command=self.load_image, width=12)
        self.load_btn.pack(side=tk.LEFT, padx=10)

        # 保存按钮
        self.save_btn = ttk.Button(button_frame, text="保存图像", command=self.save_image, width=12)
        self.save_btn.pack(side=tk.LEFT, padx=10)
        self.save_btn.config(state=tk.DISABLED)

        # 重置按钮
        self.reset_btn = ttk.Button(button_frame, text="重置调整", command=self.reset_adjustments, width=12)
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        self.reset_btn.config(state=tk.DISABLED)

        # ---------------------- 新增：保存位数选择（单选框） ----------------------
        bit_select_frame = ttk.Frame(button_frame)
        bit_select_frame.pack(side=tk.LEFT, padx=20)

        # 提示标签
        bit_label = ttk.Label(bit_select_frame, text="保存位数：")
        bit_label.pack(side=tk.LEFT, padx=5)

        # 24位RGB单选框（默认选中）
        rb_24bit = ttk.Radiobutton(bit_select_frame, text="24位RGB", variable=self.save_bit_depth, value="24bit")
        rb_24bit.pack(side=tk.LEFT, padx=5)

        # 8位灰度单选框
        rb_8bit = ttk.Radiobutton(bit_select_frame, text="8位灰度", variable=self.save_bit_depth, value="8bit")
        rb_8bit.pack(side=tk.LEFT, padx=5)

    def init_adjustment_parameters(self):
        """初始化调整参数（不变）"""
        # 原有参数
        self.brightness = tk.IntVar(value=0)
        self.contrast = tk.IntVar(value=100)
        self.gamma = tk.DoubleVar(value=1.0)
        self.hue = tk.IntVar(value=0)
        self.saturation = tk.IntVar(value=100)
        self.value = tk.IntVar(value=100)
        self.red = tk.IntVar(value=0)
        self.green = tk.IntVar(value=0)
        self.blue = tk.IntVar(value=0)
        self.blur_amount = tk.IntVar(value=0)
        self.sharpen_amount = tk.IntVar(value=0)
        self.edge_detection = tk.IntVar(value=0)
        self.threshold = tk.IntVar(value=0)
        self.gray_scale = tk.BooleanVar(value=False)
        self.rotation = tk.IntVar(value=0)
        self.zoom = tk.IntVar(value=100)
        self.flip_horizontal = tk.BooleanVar(value=False)
        self.flip_vertical = tk.BooleanVar(value=False)

        # 传统图像增强参数
        self.gray_corr_a = tk.DoubleVar(value=1.0)
        self.gray_corr_b = tk.IntVar(value=0)
        self.gray_corr_enable = tk.BooleanVar(value=False)
        self.he_type = StringVar(value="全局HE")
        self.clahe_clip = tk.DoubleVar(value=2.0)
        self.he_enable = tk.BooleanVar(value=False)
        self.gray_world_enable = tk.BooleanVar(value=False)
        self.retinex_sigma = tk.IntVar(value=100)
        self.retinex_enable = tk.BooleanVar(value=False)
        self.stretch_in_low = tk.IntVar(value=0)
        self.stretch_in_high = tk.IntVar(value=255)
        self.stretch_enable = tk.BooleanVar(value=False)
        self.smooth_type = StringVar(value="均值滤波")  # 默认均值滤波
        self.smooth_kernel = tk.IntVar(value=3)  # 核大小（整数，奇数）
        self.smooth_enable = tk.BooleanVar(value=False)
        self.sharpen_type = StringVar(value="拉普拉斯")
        self.sharpen_strength = tk.DoubleVar(value=1.0)
        self.sharpen_enable = tk.BooleanVar(value=False)

        # 高通滤波参数（不变，与原逻辑共用同一强度参数）
        self.highpass_strength = tk.DoubleVar(value=1.0)
        self.highpass_enable = tk.BooleanVar(value=False)

        # 灰度级修正（伽马）参数
        self.gamma_corr_value = tk.DoubleVar(value=1.0)
        self.gamma_corr_enable = tk.BooleanVar(value=False)

        # 创建滑动条
        self.create_sliders()

    def create_sliders(self):
        """创建所有滑动条（核心修改：平滑滤波区域新增sigma滑动条）"""
        # 基本调整
        self.create_slider(self.basic_frame, "亮度", self.brightness, -100, 100, 1)
        self.create_slider(self.basic_frame, "对比度", self.contrast, 0, 200, 1)
        self.create_slider(self.basic_frame, "伽马校正", self.gamma, 0.1, 3.0, 0.1)
        # 颜色调整
        self.create_slider(self.color_frame, "色调", self.hue, -180, 180, 1)
        self.create_slider(self.color_frame, "饱和度", self.saturation, 0, 200, 1)
        self.create_slider(self.color_frame, "明度", self.value, 0, 200, 1)
        self.create_slider(self.color_frame, "红色通道", self.red, -100, 100, 1)
        self.create_slider(self.color_frame, "绿色通道", self.green, -100, 100, 1)
        self.create_slider(self.color_frame, "蓝色通道", self.blue, -100, 100, 1)
        # 滤镜效果
        self.create_slider(self.filter_frame, "模糊程度", self.blur_amount, 0, 20, 1)
        self.create_slider(self.filter_frame, "锐化程度", self.sharpen_amount, 0, 10, 1)
        self.create_slider(self.filter_frame, "边缘检测", self.edge_detection, 0, 1, 1)
        self.create_slider(self.filter_frame, "阈值处理", self.threshold, 0, 255, 1)
        gray_check = ttk.Checkbutton(self.filter_frame, text="灰度图", variable=self.gray_scale)
        gray_check.pack(anchor=tk.W, pady=5)
        # 几何变换
        self.create_slider(self.geometry_frame, "旋转角度", self.rotation, 0, 360, 1)
        self.create_slider(self.geometry_frame, "缩放比例(%)", self.zoom, 10, 200, 1)
        flip_h_check = ttk.Checkbutton(self.geometry_frame, text="水平翻转", variable=self.flip_horizontal)
        flip_h_check.pack(anchor=tk.W, pady=5)
        flip_v_check = ttk.Checkbutton(self.geometry_frame, text="垂直翻转", variable=self.flip_vertical)
        flip_v_check.pack(anchor=tk.W, pady=5)
        # 传统图像增强
        te_frame = self.traditional_enhance_frame
        ttk.Label(te_frame, text="=== 1. 灰度级修正（线性变换）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用灰度级修正", variable=self.gray_corr_enable).pack(anchor=tk.W, pady=2)
        self.create_slider(te_frame, "斜率(对比度)", self.gray_corr_a, 0.1, 3.0, 0.1)
        self.create_slider(te_frame, "截距(亮度)", self.gray_corr_b, -50, 50, 1)

        ttk.Label(te_frame, text="=== 2. 灰度级修正（伽马）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用伽马校正", variable=self.gamma_corr_enable).pack(anchor=tk.W, pady=2)
        self.create_slider(te_frame, "伽马值", self.gamma_corr_value, 0.1, 3.0, 0.1)

        ttk.Label(te_frame, text="=== 3. 直方图均衡化 ===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用直方图均衡化", variable=self.he_enable).pack(anchor=tk.W, pady=2)
        he_type_frame = ttk.Frame(te_frame)
        he_type_frame.pack(anchor=tk.W, pady=2)
        ttk.Label(he_type_frame, text="均衡化类型", width=15).pack(side=tk.LEFT)
        he_type_combo = ttk.Combobox(he_type_frame, textvariable=self.he_type, values=["全局HE", "CLAHE"], state="readonly")
        he_type_combo.pack(side=tk.LEFT)
        self.create_slider(te_frame, "CLAHE对比度限制", self.clahe_clip, 1.0, 10.0, 0.1)

        ttk.Label(te_frame, text="=== 4. 灰度世界算法（自动白平衡）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用灰度世界算法", variable=self.gray_world_enable).pack(anchor=tk.W, pady=2)

        ttk.Label(te_frame, text="=== 5. Retinex算法（单尺度）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用Retinex", variable=self.retinex_enable).pack(anchor=tk.W, pady=2)
        self.create_slider(te_frame, "高斯核Sigma", self.retinex_sigma, 50, 200, 1)

        ttk.Label(te_frame, text="=== 6. 对比度拉伸 ===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用对比度拉伸", variable=self.stretch_enable).pack(anchor=tk.W, pady=2)
        self.create_slider(te_frame, "输入低阈值", self.stretch_in_low, 0, 200, 1)
        self.create_slider(te_frame, "输入高阈值", self.stretch_in_high, 55, 255, 1)

        # ---------------------- 核心修改：平滑滤波区域（新增sigma滑动条） ----------------------
        ttk.Label(te_frame, text="=== 7. 平滑滤波 ===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用平滑滤波", variable=self.smooth_enable).pack(anchor=tk.W, pady=2)
        # 滤波类型选择（绑定事件，切换时显示/隐藏sigma滑块）
        smooth_type_frame = ttk.Frame(te_frame)
        smooth_type_frame.pack(anchor=tk.W, pady=2)
        ttk.Label(smooth_type_frame, text="滤波类型", width=15).pack(side=tk.LEFT)
        smooth_type_combo = ttk.Combobox(smooth_type_frame, textvariable=self.smooth_type,
                                         values=["均值滤波", "中值滤波", "高斯滤波"], state="readonly")
        smooth_type_combo.pack(side=tk.LEFT)
        smooth_type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_sigma_slider_visibility())  # 切换类型触发滑块显示

        # 1. 核大小滑动条（均值/中值滤波用，整数步进1，确保奇数）
        self.create_slider(te_frame, "核大小（奇数）", self.smooth_kernel, 1, 11, 1)

        # 2. 新增sigma滑动条（高斯滤波专用，0.1步进，初始隐藏）
        self.sigma_slider_frame = ttk.Frame(te_frame)  # 用Frame包裹，方便整体显示/隐藏
        self.create_slider(self.sigma_slider_frame, "高斯Sigma（模糊程度）", self.smooth_sigma, 0.1, 10.0, 0.1)
        self.sigma_slider_frame.pack(anchor=tk.W, pady=2)  # 初始显示，后续在update中根据类型隐藏

        ttk.Label(te_frame, text="=== 8. 锐化滤波（拉普拉斯/Sobel）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用锐化滤波", variable=self.sharpen_enable).pack(anchor=tk.W, pady=2)
        sharpen_type_frame = ttk.Frame(te_frame)
        sharpen_type_frame.pack(anchor=tk.W, pady=2)
        ttk.Label(sharpen_type_frame, text="锐化类型", width=15).pack(side=tk.LEFT)
        sharpen_type_combo = ttk.Combobox(sharpen_type_frame, textvariable=self.sharpen_type,
                                          values=["拉普拉斯", "Sobel X", "Sobel Y"], state="readonly")
        sharpen_type_combo.pack(side=tk.LEFT)
        self.create_slider(te_frame, "锐化强度", self.sharpen_strength, 0.1, 5.0, 0.1)

        ttk.Label(te_frame, text="=== 9. 锐化滤波（高通）===", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(te_frame, text="启用高通锐化", variable=self.highpass_enable).pack(anchor=tk.W, pady=2)
        self.create_slider(te_frame, "高通强度", self.highpass_strength, 0.1, 5.0, 0.1)

    def create_slider(self, parent, label_text, variable, from_, to, resolution):
        """创建滑动条（不变）"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=3)

        label = ttk.Label(frame, text=label_text, width=15)
        label.pack(side=tk.LEFT, padx=5)

        slider = tk.Scale(frame, variable=variable, from_=from_, to=to,
                          orient=tk.HORIZONTAL, length=300, resolution=resolution)
        slider.pack(side=tk.LEFT, padx=5)

        value_label = ttk.Label(frame, textvariable=variable, width=10)
        value_label.pack(side=tk.LEFT, padx=5)

    # ---------------------- 核心新增：根据滤波类型显示/隐藏sigma滑动条 ----------------------
    def update_sigma_slider_visibility(self):
        """选择高斯滤波时显示sigma滑动条，其他类型隐藏"""
        if self.smooth_type.get() == "高斯滤波":
            self.sigma_slider_frame.pack(anchor=tk.W, pady=2)  # 显示sigma滑块
        else:
            self.sigma_slider_frame.pack_forget()  # 隐藏sigma滑块

    def bind_adjustments(self):
        """绑定调整事件（核心新增：sigma参数绑定更新）"""
        # 原有绑定
        self.brightness.trace_add("write", self.update_image)
        self.contrast.trace_add("write", self.update_image)
        self.gamma.trace_add("write", self.update_image)
        self.hue.trace_add("write", self.update_image)
        self.saturation.trace_add("write", self.update_image)
        self.value.trace_add("write", self.update_image)
        self.red.trace_add("write", self.update_image)
        self.green.trace_add("write", self.update_image)
        self.blue.trace_add("write", self.update_image)
        self.blur_amount.trace_add("write", self.update_image)
        self.sharpen_amount.trace_add("write", self.update_image)
        self.edge_detection.trace_add("write", self.update_image)
        self.threshold.trace_add("write", self.update_image)
        self.gray_scale.trace_add("write", self.update_image)
        self.rotation.trace_add("write", self.update_image)
        self.zoom.trace_add("write", self.update_image)
        self.flip_horizontal.trace_add("write", self.update_image)
        self.flip_vertical.trace_add("write", self.update_image)
        # 传统增强绑定
        self.gray_corr_a.trace_add("write", self.update_image)
        self.gray_corr_b.trace_add("write", self.update_image)
        self.gray_corr_enable.trace_add("write", self.update_image)
        self.he_type.trace_add("write", self.update_image)
        self.clahe_clip.trace_add("write", self.update_image)
        self.he_enable.trace_add("write", self.update_image)
        self.gray_world_enable.trace_add("write", self.update_image)
        self.retinex_sigma.trace_add("write", self.update_image)
        self.retinex_enable.trace_add("write", self.update_image)
        self.stretch_in_low.trace_add("write", self.update_image)
        self.stretch_in_high.trace_add("write", self.update_image)
        self.stretch_enable.trace_add("write", self.update_image)
        self.smooth_type.trace_add("write", self.update_image)  # 滤波类型变化触发更新
        self.smooth_kernel.trace_add("write", self.update_image)  # 核大小变化触发更新
        self.smooth_enable.trace_add("write", self.update_image)
        self.sharpen_type.trace_add("write", self.update_image)
        self.sharpen_strength.trace_add("write", self.update_image)
        self.sharpen_enable.trace_add("write", self.update_image)
        # 伽马校正绑定
        self.gamma_corr_value.trace_add("write", self.update_image)
        self.gamma_corr_enable.trace_add("write", self.update_image)
        # 高通滤波绑定（不变）
        self.highpass_strength.trace_add("write", self.update_image)
        self.highpass_enable.trace_add("write", self.update_image)
        # ---------------------- 核心新增：sigma参数绑定更新事件 ----------------------
        self.smooth_sigma.trace_add("write", self.update_image)

    # ---------------------- 加载图像（不变） ----------------------
    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("图像文件", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
            if file_path:
                self.image_path = file_path
                self.original_image = cv2.imread(file_path)
                self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                self.original_height, self.original_width = self.original_image.shape[:2]
                self.reset_adjustments()
                self.display_image()
                self.save_btn.config(state=tk.NORMAL)
                self.reset_btn.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("错误", f"加载图像失败: {str(e)}")

    def display_image(self):
        """显示图像（基于右侧固定容器尺寸）"""
        if self.original_image is not None:
            # 显示原图
            original_img = self.resize_image(self.original_image)
            original_photo = ImageTk.PhotoImage(image=original_img)
            self.original_label.config(image=original_photo)
            self.original_label.image = original_photo
            # 显示处理后图像
            self.update_image()

    def resize_image(self, image):
        """基于右侧固定容器尺寸缩放（不变）"""
        container_width = self.original_container.winfo_width() or 550
        container_height = self.original_container.winfo_height() or 350

        height, width = image.shape[:2]
        ratio = min(container_width / width, container_height / height)

        new_size = (int(width * ratio), int(height * ratio))
        resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

        return Image.fromarray(resized_image)

    # ---------------------- 几何变换（不变） ----------------------
    def apply_geometric_transformations(self, img):
        rotation = self.rotation.get()
        if rotation != 0:
            center = (self.original_width // 2, self.original_height // 2)
            matrix = cv2.getRotationMatrix2D(center, rotation, 1)
            img = cv2.warpAffine(img, matrix, (self.original_width, self.original_height))

        zoom = self.zoom.get() / 100.0
        if zoom != 1.0:
            new_width = int(self.original_width * zoom)
            new_height = int(self.original_height * zoom)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

        flip_code = -1
        if self.flip_horizontal.get() and self.flip_vertical.get():
            flip_code = -1
        elif self.flip_horizontal.get():
            flip_code = 1
        elif self.flip_vertical.get():
            flip_code = 0
        if flip_code != -1:
            img = cv2.flip(img, flip_code)

        return img

    # ---------------------- 更新图像（不变） ----------------------
    def update_image(self, *args):
        if self.original_image is None:
            return
        try:
            img = self.original_image.copy()

            # 处理顺序（不变，高通滤波仍在原有位置）
            img = self.adjust_brightness_contrast(img)
            img = self.adjust_gamma(img)
            img = self.adjust_color_channels(img)
            img = self.adjust_hsv(img)
            img = self.apply_filters(img)
            img = self.apply_gray_level_correction(img)
            img = self.apply_gamma_correction(img)
            img = self.apply_contrast_stretch(img)
            img = self.apply_smoothing_filter(img)  # 调用修改后的平滑滤波方法
            img = self.apply_sharpening_filter(img)
            img = self.apply_highpass_filter(img)  # 调用修改后的高通滤波方法
            img = self.apply_histogram_equalization(img)
            img = self.apply_gray_world(img)
            img = self.apply_retinex(img)
            img = self.apply_geometric_transformations(img)

            self.processed_image = img
            processed_img = self.resize_image(img)
            processed_photo = ImageTk.PhotoImage(image=processed_img)
            self.processed_label.config(image=processed_photo)
            self.processed_label.image = processed_photo

        except Exception as e:
            print(f"图像处理错误: {str(e)}")
            messagebox.showerror("错误", f"图像处理失败: {str(e)}")

    # ---------------------- 原有工具方法（修改apply_smoothing_filter使用sigma参数） ----------------------
    def adjust_brightness_contrast(self, img):
        brightness = self.brightness.get()
        contrast = self.contrast.get() / 100.0
        if brightness != 0 or contrast != 1.0:
            img = np.clip(contrast * img + brightness, 0, 255).astype(np.uint8)
        return img

    def adjust_gamma(self, img):
        gamma = self.gamma.get()
        if gamma != 1.0:
            table = np.array([((i / 255.0) ** (1 / gamma)) * 255 for i in range(256)]).astype("uint8")
            img = cv2.LUT(img, table)
        return img

    def adjust_color_channels(self, img):
        r, g, b = cv2.split(img)
        red = self.red.get()
        if red != 0:
            r = np.clip(r + red, 0, 255).astype(np.uint8)
        green = self.green.get()
        if green != 0:
            g = np.clip(g + green, 0, 255).astype(np.uint8)
        blue = self.blue.get()
        if blue != 0:
            b = np.clip(b + blue, 0, 255).astype(np.uint8)
        return cv2.merge([r, g, b])

    def adjust_hsv(self, img):
        hue = self.hue.get()
        saturation = self.saturation.get() / 100.0
        value = self.value.get() / 100.0
        if hue != 0 or saturation != 1.0 or value != 1.0:
            hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv)
            h = (h + hue) % 180
            s = np.clip(s * saturation, 0, 255).astype(np.uint8)
            v = np.clip(v * value, 0, 255).astype(np.uint8)
            img = cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2RGB)
        return img

    def apply_filters(self, img):
        if self.gray_scale.get():
            img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
        blur = self.blur_amount.get()
        if blur > 0:
            img = cv2.GaussianBlur(img, (2 * blur + 1, 2 * blur + 1), 0)
        sharpen = self.sharpen_amount.get()
        if sharpen > 0:
            kernel = np.array([[-1, -1, -1], [-1, 9 + sharpen, -1], [-1, -1, -1]])
            img = np.clip(cv2.filter2D(img, -1, kernel), 0, 255).astype(np.uint8)
        if self.edge_detection.get() == 1:
            img = cv2.cvtColor(cv2.Canny(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), 100, 200), cv2.COLOR_GRAY2RGB)
        threshold = self.threshold.get()
        if threshold > 0:
            _, img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), threshold, 255, cv2.THRESH_BINARY)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        return img

    # ---------------------- 核心修改：支持24位/8位保存 ----------------------
    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning("警告", "没有可保存的图像")
            return
        try:
            # 1. 确定保存文件名（根据位数添加后缀）
            if self.image_path:
                dir_name, file_name = os.path.split(self.image_path)
                base_name, ext = os.path.splitext(file_name)
                if self.save_bit_depth.get() == "8bit":
                    default_path = os.path.join(dir_name, f"{base_name}_edited_8bit{ext}")
                else:
                    default_path = os.path.join(dir_name, f"{base_name}_edited{ext}")
            else:
                default_path = "edited_image_8bit.png" if self.save_bit_depth.get() == "8bit" else "edited_image.png"

            # 2. 选择保存路径
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG文件", "*.png"), ("JPEG文件", "*.jpg"),
                                                                ("BMP文件", "*.bmp")],
                                                     initialfile=default_path)
            if not save_path:
                return

            # 3. 根据选择的位数处理图像
            if self.save_bit_depth.get() == "8bit":
                # 8位：转为单通道灰度图（cv2自动识别为8位）
                img_to_save = cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2GRAY)
                cv2.imwrite(save_path, img_to_save)
                messagebox.showinfo("成功", f"8位灰度图已保存至:\n{save_path}")
            else:
                # 24位：保留RGB三通道（原有逻辑）
                img_to_save = cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(save_path, img_to_save)
                messagebox.showinfo("成功", f"24位RGB图已保存至:\n{save_path}")

        except Exception as e:
            messagebox.showerror("错误", f"保存图像失败: {str(e)}")

    # 传统图像增强方法（不变）
    def apply_gray_level_correction(self, img):
        if not self.gray_corr_enable.get():
            return img
        try:
            a = self.gray_corr_a.get()
            b = self.gray_corr_b.get()
            corrected = np.clip(a * img + b, 0, 255).astype(np.uint8)
            return corrected
        except Exception as e:
            print(f"灰度级修正错误: {str(e)}")
            return img

    def apply_gamma_correction(self, img):
        if not self.gamma_corr_enable.get():
            return img
        try:
            gamma = self.gamma_corr_value.get()
            if gamma <= 0:
                gamma = 0.1
            img_float = img.astype(np.float32) / 255.0
            corrected = np.power(img_float, gamma) * 255.0
            return corrected.astype(np.uint8)
        except Exception as e:
            print(f"伽马校正错误: {str(e)}")
            return img

    def apply_histogram_equalization(self, img):
        if not self.he_enable.get():
            return img
        try:
            he_type = self.he_type.get()
            if len(img.shape) == 3:
                hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                h, s, v = cv2.split(hsv)
                if he_type == "全局HE":
                    v_eq = cv2.equalizeHist(v)
                else:
                    clahe = cv2.createCLAHE(clipLimit=self.clahe_clip.get(), tileGridSize=(8, 8))
                    v_eq = clahe.apply(v)
                return cv2.cvtColor(cv2.merge([h, s, v_eq]), cv2.COLOR_HSV2RGB)
            else:
                if he_type == "全局HE":
                    return cv2.equalizeHist(img)
                else:
                    clahe = cv2.createCLAHE(clipLimit=self.clahe_clip.get(), tileGridSize=(8, 8))
                    return clahe.apply(img)
        except Exception as e:
            print(f"直方图均衡化错误: {str(e)}")
            return img

    def apply_gray_world(self, img):
        if not self.gray_world_enable.get() or len(img.shape) != 3:
            return img
        try:
            r_mean = np.mean(img[:, :, 0])
            g_mean = np.mean(img[:, :, 1])
            b_mean = np.mean(img[:, :, 2])
            gray_mean = (r_mean + g_mean + b_mean) / 3
            img[:, :, 0] = np.clip(img[:, :, 0] * (gray_mean / r_mean), 0, 255).astype(np.uint8)
            img[:, :, 1] = np.clip(img[:, :, 1] * (gray_mean / g_mean), 0, 255).astype(np.uint8)
            img[:, :, 2] = np.clip(img[:, :, 2] * (gray_mean / b_mean), 0, 255).astype(np.uint8)
            return img
        except Exception as e:
            print(f"灰度世界算法错误: {str(e)}")
            return img

    def apply_retinex(self, img):
        if not self.retinex_enable.get():
            return img
        try:
            sigma = self.retinex_sigma.get()
            img_float = img.astype(np.float32) / 255.0
            blur = cv2.GaussianBlur(img_float, (0, 0), sigma)
            retinex = np.log1p(img_float) - np.log1p(blur)
            retinex = (retinex - np.min(retinex)) / (np.max(retinex) - np.min(retinex))
            return (retinex * 255).astype(np.uint8)
        except Exception as e:
            print(f"Retinex算法错误: {str(e)}")
            return img

    def apply_contrast_stretch(self, img):
        if not self.stretch_enable.get():
            return img
        try:
            in_low = self.stretch_in_low.get()
            in_high = self.stretch_in_high.get()
            if in_low >= in_high:
                in_low, in_high = 0, 255
            stretched = np.clip((img - in_low) / (in_high - in_low) * 255, 0, 255).astype(np.uint8)
            return stretched
        except Exception as e:
            print(f"对比度拉伸错误: {str(e)}")
            return img

    # ---------------------- 核心修改：平滑滤波方法（使用sigma参数） ----------------------
    def apply_smoothing_filter(self, img):
        if not self.smooth_enable.get():
            return img
        try:
            kernel = self.smooth_kernel.get()
            # 确保核大小为奇数（原有逻辑）
            kernel = kernel if kernel % 2 == 1 else kernel + 1
            kernel = max(1, kernel)

            # 根据滤波类型选择参数
            if self.smooth_type.get() == "均值滤波":
                return cv2.blur(img, (kernel, kernel))
            elif self.smooth_type.get() == "中值滤波":
                return cv2.medianBlur(img, kernel)
            elif self.smooth_type.get() == "高斯滤波":
                # 高斯滤波使用新增的sigma参数（0.1步进）
                sigma = self.smooth_sigma.get()
                return cv2.GaussianBlur(img, (kernel, kernel), sigma)
        except Exception as e:
            print(f"平滑滤波错误: {str(e)}")
            return img

    def apply_sharpening_filter(self, img):
        if not self.sharpen_enable.get():
            return img
        try:
            strength = self.sharpen_strength.get()
            if self.sharpen_type.get() == "拉普拉斯":
                laplacian = cv2.Laplacian(img, cv2.CV_64F)
                img = np.clip(img - strength * laplacian, 0, 255).astype(np.uint8)
            else:
                if self.sharpen_type.get() == "Sobel X":
                    sobel = cv2.Sobel(img, cv2.CV_64F, dx=1, dy=0)
                else:
                    sobel = cv2.Sobel(img, cv2.CV_64F, dx=0, dy=1)
                img = np.clip(img + strength * np.abs(sobel), 0, 255).astype(np.uint8)
            return img
        except Exception as e:
            print(f"锐化滤波错误: {str(e)}")
            return img

    # ---------------------- 核心修改：替换高通滤波逻辑（高斯低通减影） ----------------------
    def apply_highpass_filter(self, img):
        if not self.highpass_enable.get():
            return img
        try:
            strength = self.highpass_strength.get()
            # 1. 对图像做高斯模糊，提取低频成分（与第二份代码逻辑一致）
            gaussian = cv2.GaussianBlur(img, (5, 5), 0)
            # 2. 加权混合：原图*(1+强度) - 低频图*强度 → 突出高频边缘
            high_pass = cv2.addWeighted(img, 1.0 + strength, gaussian, -strength, 0)
            # 3. 处理数值溢出，确保像素值在0-255范围
            img = cv2.convertScaleAbs(high_pass)
            return img
        except Exception as e:
            print(f"高通滤波错误: {str(e)}")
            return img

    def reset_adjustments(self):
        """重置所有参数（新增：重置sigma参数）"""
        self.brightness.set(0)
        self.contrast.set(100)
        self.gamma.set(1.0)
        self.hue.set(0)
        self.saturation.set(100)
        self.value.set(100)
        self.red.set(0)
        self.green.set(0)
        self.blue.set(0)
        self.blur_amount.set(0)
        self.sharpen_amount.set(0)
        self.edge_detection.set(0)
        self.threshold.set(0)
        self.gray_scale.set(False)
        self.rotation.set(0)
        self.zoom.set(100)
        self.flip_horizontal.set(False)
        self.flip_vertical.set(False)

        self.gray_corr_a.set(1.0)
        self.gray_corr_b.set(0)
        self.gray_corr_enable.set(False)
        self.he_type.set("全局HE")
        self.clahe_clip.set(2.0)
        self.he_enable.set(False)
        self.gray_world_enable.set(False)
        self.retinex_sigma.set(100)
        self.retinex_enable.set(False)
        self.stretch_in_low.set(0)
        self.stretch_in_high.set(255)
        self.stretch_enable.set(False)
        self.smooth_type.set("均值滤波")  # 重置为均值滤波
        self.smooth_kernel.set(3)  # 重置核大小
        self.smooth_sigma.set(1.0)  # 重置sigma参数（新增）
        self.smooth_enable.set(False)
        self.sharpen_type.set("拉普拉斯")
        self.sharpen_strength.set(1.0)
        self.sharpen_enable.set(False)

        self.gamma_corr_value.set(1.0)
        self.gamma_corr_enable.set(False)
        self.highpass_strength.set(1.0)
        self.highpass_enable.set(False)

        # 重置保存位数选择（默认24位）
        self.save_bit_depth.set("24bit")
        # 重置后隐藏sigma滑块
        self.update_sigma_slider_visibility()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()