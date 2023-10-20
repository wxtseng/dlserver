from PIL import Image
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import sys
import numpy as np
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

mycursorselect = mydb.cursor()
# 資料寫入的 SQL 語法！
sql1 = "SELECT `imgclass` FROM `uploadclassimg` Order by `upcimgid` DESC limit 1"
# 送出執行結果
mycursorselect.execute(sql1)
# 列出這次執行的數據處理結果！
result = mycursorselect.fetchone()
if result is not None:
    imgclass_json = result[0]
    data = json.loads(imgclass_json)
else:
    print("未找到資料")
data_dict = {item['value']: item['value'] for item in data}
result = [data_dict.get(item['value'], item['value']) for item in data]
#print(result)
# 從參數讀取圖檔路徑
files = sys.argv[1:]
# 載入訓練好的模型
sql2 = "SELECT `modelfile` FROM `modelupdata` Order by `allmodelid` DESC limit 1"
mycursorselect.execute(sql2)
result2 = mycursorselect.fetchone()
damodel = json.loads(result2[0])
damodel = json.loads(damodel)
for item in damodel:
    usemodel = item['model']
#print(usemodel)
net = load_model('/home/dlserver1/dlserver1_web/python/bsza7.h5')
#net = load_model(f'/home/dlserver1/dlserver1_web/python/model/{usemodel}')
cls_list = result
data_list = [] #製作json格式
# 辨識每一張圖
for f in files:
    img = image.load_img(f, target_size=(224, 224))
    if img is None:
        continue
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    pred = net.predict(x)[0]
    top_inds = pred.argsort()[::-1][:5]
    print(f)
    for i, index in enumerate(top_inds):
        if index < len(pred) and index < len(cls_list):
            print('{:.3f} {}'.format(pred[index], cls_list[index]))
            #製作json格式
            data_item = { "rank":i+1 ,"itype": cls_list[index],"Similarity": '{:.3f}'.format(pred[index])}
            data_list.append(data_item)

json_data = json.dumps(data_list)  # 使用 indent 参数使 JSON 格式化输出更易读
json_data = json_data.replace('\n', '')
json_data = json_data.replace(' ', '')
json_data = json_data.replace('\\', '')
# 打印或处理 json_data
print(json_data)
txt_filename = '/home/dlserver1/dlserver1_web/python/output.txt'
# 将 JSON 数据保存到 TXT 文件
with open(txt_filename, 'w') as txt_file:
    txt_file.write(json_data)
print(f"JSON data has been saved to {txt_filename}")

# 資料上傳資料庫
# 目前資料表所在位置
#mycursor = mydb.cursor()
# 資料寫入的 SQL 語法！
sql = "INSERT INTO uploadimage (`updatatype`) VALUES (%s)"
data_tuple = (json.dumps(json_data),)
# 在目前的資料表所在位置執行底下的 SQL 與數據
mycursorselect.execute(sql, data_tuple)
# 送出執行結果
mydb.commit()
# 列出這次執行的數據處理結果！
print(mycursorselect.rowcount, "筆資料已匯入")
mycursorselect.close()
mydb.close()