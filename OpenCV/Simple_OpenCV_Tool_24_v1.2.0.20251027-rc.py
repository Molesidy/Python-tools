import cv2
import numpy as np
import os

def image_processing(input_image_path):
    """
    图像处理核心函数：按 高斯滤波→高通锐化→双边滤波 顺序处理（不转换RGB）
    :param input_image_path: 输入JPG图片的路径
    :return: 处理成功返回True，失败返回False
    """

    # 主要改变参数 highpass_strength(高通锐化参数) ,其他参数默认不变

    # ---------------------- 1. 初始化配置（沿用原代码默认参数） ----------------------
    # 高斯滤波参数
    gaussian_kernel = 3  # 核大小（奇数）
    gaussian_sigma = 1.0  # 高斯标准差
    # 高通锐化参数
    highpass_strength = 5.0  # 锐化强度
    # 双边滤波参数
    bilateral_d = 6  # 邻域直径
    bilateral_sigma_color = 50  # 颜色相似度Sigma
    bilateral_sigma_space = 50  # 空间相似度Sigma

    # ---------------------- 2. 准备输出文件夹 ----------------------
    output_dir = "output_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # ---------------------- 3. 读取输入图片（不转换为RGB，保持BGR） ----------------------
    img_bgr = cv2.imread(input_image_path)  # 直接读取为BGR cv2.imwrite（默认支持 BGR）,OpenCV 读取图片时默认使用BGR通道顺序（蓝色、绿色、红色）,通道顺序无影响
    if img_bgr is None:
        print(f"错误：无法读取图片，请检查路径是否正确（仅支持JPG格式）")
        return False

    # ---------------------- 4. 按顺序应用滤波处理（直接处理BGR） ----------------------
    # 步骤1：高斯滤波
    gaussian_filtered = cv2.GaussianBlur(img_bgr, (gaussian_kernel, gaussian_kernel), gaussian_sigma)
    print("(1) 高斯滤波处理完成（默认参数：核大小3，Sigma=1.0）")

    # 步骤2：高通锐化
    gaussian_lowpass = cv2.GaussianBlur(gaussian_filtered, (5, 5), 0)  # 生成低通图像
    highpass_filtered = cv2.addWeighted(
        gaussian_filtered, 1.0 + highpass_strength,
        gaussian_lowpass, -highpass_strength,
        0  # 偏移量
    )
    highpass_filtered = cv2.convertScaleAbs(highpass_filtered)  # 确保像素值在0-255
    print("(2) 高通锐化处理完成（默认参数：强度5.0）")

    # 步骤3：双边滤波
    bilateral_filtered = cv2.bilateralFilter(
        highpass_filtered,
        d=bilateral_d,
        sigmaColor=bilateral_sigma_color,
        sigmaSpace=bilateral_sigma_space
    )
    print("(3) 双边滤波处理完成（默认参数：邻域直径6，颜色Sigma=50，空间Sigma=50）")

    # ---------------------- 5. 保存处理后的图片（直接保存BGR，无需转换） ----------------------
    input_filename = os.path.basename(input_image_path)
    filename_without_ext = os.path.splitext(input_filename)[0]
    output_filename = f"{filename_without_ext}_processed.jpg"
    output_path = os.path.join(output_dir, output_filename)

    # 直接保存BGR格式（cv2.imwrite默认支持BGR）
    save_success = cv2.imwrite(output_path, bilateral_filtered)

    if save_success:
        print(f"\n🎉 图片处理完成！已保存至：{output_path}")
        return True
    else:
        print(f"错误：图片保存失败，请检查输出文件夹权限")
        return False

if __name__ == "__main__":
    input_path = input("请输入需要处理的JPG图片路径（例如：test.jpg 或 ./images/test.jpg）：")
    if not input_path.lower().endswith((".jpg", ".jpeg")):
        print("错误：仅支持JPG/JPEG格式的图片，请重新输入")
    else:
        image_processing(input_path)

