import random
from PIL import Image, ImageEnhance
import os
import shutil
import mysql.connector
import json
import requests
#連線資料庫
mydb = mysql.connector.connect(
  host="localhost",
  user="dlserver1",
  password="2050014",
  database="dlserver1"
)
# 資料上傳資料庫
# 目前資料表所在位置
mycursor = mydb.cursor()
# 資料寫入的 SQL 語法！
sql = "SELECT `imgclass` FROM `uploadclassimg` Order by `upcimgid` DESC limit 1"
# 送出執行結果
mycursor.execute(sql)
# 列出這次執行的數據處理結果！
result = mycursor.fetchone()
mycursor.close()
mydb.close()
data = json.loads(result[0])
#data = json.loads(data)
# 現在你可以使用鍵來存取值
for item in data:
    itype = item['value']
    print(itype)
    input_folder = f"/home/dlserver1/dlserver1_web/imagetrain/readypic/{itype}"
    output_folder_rotation = f"/home/dlserver1/dlserver1_web/all/train/{itype}"
    output_folder_exposure = f"/home/dlserver1/dlserver1_web/all/train/{itype}"
    output_folder_dark = f"/home/dlserver1/dlserver1_web/all/train/{itype}"
    output_folder_gray = f"/home/dlserver1/dlserver1_web/all/train/{itype}"
    selected_images_folder = f"/home/dlserver1/dlserver1_web/all/valid/{itype}"
    # 確保輸出文件存在
    if not os.path.exists(output_folder_rotation):
        os.makedirs(output_folder_rotation)

    if not os.path.exists(output_folder_exposure):
        os.makedirs(output_folder_exposure)

    if not os.path.exists(output_folder_dark):
        os.makedirs(output_folder_dark)

    if not os.path.exists(output_folder_gray):
        os.makedirs(output_folder_gray)

    if not os.path.exists(selected_images_folder):
        os.makedirs(selected_images_folder)

    # 初始化递增数字
    shared_index = 0
    
    # 逐度旋转并保存图像
    for angle in range(0, 180, 30):
        for filename in os.listdir(input_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                input_path = os.path.join(input_folder, filename)
                image = Image.open(input_path)
                image = image.convert('L')
                # 剪裁图像到大小 224x224
                width, height = image.size
                # 定义要裁剪的区域，左上角和右下角坐标
                left = (width - 224) // 2
                top = (height - 224) // 2
                right = (width + 224) // 2
                bottom = (height + 224) // 2
                image = image.crop((left, top, right, bottom))
                
                # 旋转图像并保存
                rotated_image = image.rotate(angle)
                output_filename_rotation = f"{shared_index:03d}_{filename}"  # 使用共享的递增数字
                output_path_rotation = os.path.join(output_folder_rotation, output_filename_rotation)
                rotated_image.save(output_path_rotation)
                
                # 递增共享的数字
                shared_index += 1
    
    print("完成旋转！")
    
    # 设置曝光度调整因子（小于1降低曝光度，大于1增加曝光度）
    exposure_factor = 2
    
    # 批量处理图像并保存到同一文件夹
    for filename in os.listdir(output_folder_rotation):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_path = os.path.join(output_folder_rotation, filename)
            image = Image.open(input_path)
    
            # 调整曝光度
            enhancer = ImageEnhance.Brightness(image)
            adjusted_image = enhancer.enhance(exposure_factor)
    
            # 创建新文件名，添加一个递增的数字
            base_filename, _ = os.path.splitext(filename)
            output_filename_exposure = f"{shared_index:03d}_{base_filename}.png"  # 使用共享的递增数字
            output_path_exposure = os.path.join(output_folder_exposure, output_filename_exposure)
            adjusted_image.save(output_path_exposure)
            
            # 递增共享的数字
            shared_index += 1
    
    print("完成曝光度调整并继续使用共享的递增数字！")
    
    
    # 设置曝光度调整因子（小于1降低曝光度，大于1增加曝光度）
    expoure_f1212 = 0.5
    
    # 暗暗批量处理图像并保存到同一文件夹
    for filename in os.listdir(output_folder_rotation):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_path = os.path.join(output_folder_rotation, filename)
            image = Image.open(input_path)
    
            # 暗暗调整曝光度
            enhancer = ImageEnhance.Brightness(image)
            adjusted_image = enhancer.enhance(expoure_f1212)
    
            # 暗暗创建新文件名，添加一个递增的数字
            base1_filename1, _ = os.path.splitext(filename)
            output_filename_exposure = f"{shared_index:03d}_{base1_filename1}.png"  # 使用共享的递增数字
            output_path_exposure = os.path.join(output_folder_dark, output_filename_exposure)
            adjusted_image.save(output_path_exposure)
            
            # 暗暗递增共享的数字
            shared_index += 1
    
    print("完成曝光度调整暗暗！")
    
    # 批量处理图像并保存为灰度图像
    for filename in os.listdir(output_folder_dark):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_path = os.path.join(output_folder_dark, filename)
            image = Image.open(input_path)
            
            # 转换为灰度图像
            grayscale_image = image.convert("L")
            
            # 创建新文件名，添加一个递增的数字
            base2_filename2, _ = os.path.splitext(filename)
            output_filename_gray = f"{shared_index:03d}_{base2_filename2}.png"  # 使用共享的递增数字
            output_path_gray = os.path.join(output_folder_gray, output_filename_gray)
            grayscale_image.save(output_path_gray)
            
            # 递增共享的数字
            shared_index += 1
    
    print("完成转换为灰度图像！")
    
    # 获取输出文件夹中所有图像文件的列表
    output_image_files = [filename for filename in os.listdir(output_folder_rotation) if filename.endswith((".jpg", ".png"))]
    
    # 随机选择图像
    random.shuffle(output_image_files)
    selected_images = output_image_files[:int(0.3 * len(output_image_files))]  # 选择30%的图像
    
    # 移动选定的图像到另一个文件夹
    for filename in selected_images:
        input_path = os.path.join(output_folder_rotation, filename)
        output_path = os.path.join(selected_images_folder, filename)
        shutil.move(input_path, output_path)
    
    print("完成选定的图像的移动！")
os.system("python3 /home/dlserver1/dlserver1_web/python/train50.py >/home/dlserver1/dlserver1_web/python/model/out.log 2>/home/dlserver1/dlserver1_web/python/model/err.log")