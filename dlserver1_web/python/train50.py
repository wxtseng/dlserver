from tensorflow.keras import backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
#import matplotlib.pyplot as plt
import tensorflow as tf
import os
import json
import time
import random
import string
import mysql.connector
import requests
#連線資料庫
#mydb = mysql.connector.connect(
  #host="localhost",
  #user="dlserver1",
  #password="2050014",
  #database="dlserver1"
#)

# 資料路徑
DATASET_PATH  = '/home/dlserver1/dlserver1_web/all'

# 影像大小
IMAGE_SIZE = (224, 224)
import os

# 定義儲存影像類別名稱的列表
class_names = []

# 指定包含影像的資料夾路徑

# 遍歷資料夾內的文件和子資料夾
for subdir, dirs, files in os.walk(DATASET_PATH):
    for file in files:
        # 獲取文件的完整路径
        file_path = os.path.join(subdir, file)
        # 獲取文件所在的目錄（即類別名稱）
        class_name = os.path.basename(subdir)
        # 如果類別名稱不在清單中，則新增
        if class_name not in class_names:
            class_names.append(class_name)

# 打印偵測到的影像類別數量
#print("图像类别数量:", class_names)

# 影像類別數
NUM_CLASSES = len(class_names)

# 若 GPU 記憶體不足，可調降 batch size 或凍結更多層網路
BATCH_SIZE = 8

# 凍結網路層數
FREEZE_LAYERS = 2

# Epoch 數
NUM_EPOCHS = 10

# 模型輸出儲存的檔案
#WEIGHTS_FINAL = 'aatest.h5'

# 透過 data augmentation 產生訓練與驗證用的影像資料
train_datagen = ImageDataGenerator(rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   channel_shift_range=10,
                                   horizontal_flip=True,
                                   fill_mode='nearest')
train_batches = train_datagen.flow_from_directory(DATASET_PATH + '/train',
                                                  target_size=IMAGE_SIZE,
                                                  interpolation='bicubic',
                                                  class_mode='categorical',
                                                  shuffle=True,
                                                  batch_size=BATCH_SIZE)

valid_datagen = ImageDataGenerator()
valid_batches = valid_datagen.flow_from_directory(DATASET_PATH + '/valid',
                                                  target_size=IMAGE_SIZE,
                                                  interpolation='bicubic',
                                                  class_mode='categorical',
                                                  shuffle=False,
                                                  batch_size=BATCH_SIZE)

# 輸出各類別的索引值python 
for cls, idx in train_batches.class_indices.items():
    print('Class #{} = {}'.format(idx, cls))

# 以訓練好的 ResNet50 為基礎來建立模型，
# 捨棄 ResNet50 頂層的 fully connected layers
net = ResNet50(include_top=False, weights='imagenet', input_tensor=None,
               input_shape=(IMAGE_SIZE[0],IMAGE_SIZE[1],3))
x = net.output
x = Flatten()(x)

# 增加 DropOut layer
x = Dropout(0.5)(x)

# 增加 Dense layer，以 softmax 產生個類別的機率值
output_layer = Dense(NUM_CLASSES, activation='softmax', name='softmax')(x)

# 設定凍結與要進行訓練的網路層
net_final = Model(inputs=net.input, outputs=output_layer)
for layer in net_final.layers[:FREEZE_LAYERS]:
    layer.trainable = False
for layer in net_final.layers[FREEZE_LAYERS:]:
    layer.trainable = True

# 使用 Adam optimizer，以較低的 learning rate 進行 fine-tuning

net_final.compile(optimizer=Adam(lr=1e-4),
                  loss='categorical_crossentropy', metrics=['accuracy'])

#net_final.compile(optimizer=Adam(learning_rate=1e-5),loss='categorical_crossentropy', metrics=['accuracy'])

# 輸出整個網路結構
#print(net_final.summary())
# 訓練模型
data_list = [] #製作json格式
# 隨機檔案命名
filename_length =5
def generate_random_filename(length):
    characters =  string.ascii_lowercase+string.digits
    filename =''.join(random.choice(characters) for _ in range(length))+'.h5'
    return filename
random_filename = generate_random_filename(filename_length)
folder_path='/home/dlserver1/dlserver1_web/python/model/'
file_path1 = os.path.join(folder_path, random_filename)
#WEIGHTS_FINAL='train.h5'

checkpoint = tf.keras.callbacks.ModelCheckpoint(folder_path+ random_filename, save_freq='epoch',verbose=1)
# 資料上傳資料庫
#mycursor = mydb.cursor()
#sql = "INSERT INTO modelupdata (modelfile) VALUES (%s)"
#data_tuple = (json.dumps(random_filename),)
#mycursor.execute(sql, data_tuple)
#mydb.commit()
#print(mycursor.rowcount, "筆資料已匯入")
print(random_filename)
txth5name=os.path.splitext( random_filename)[0]
txtpath=folder_path+random_filename                   
txt_filename =folder_path+ txth5name+'.txt'
with open(txt_filename, 'w') as txt_file:
    print(f"JSON data has been saved to {txt_filename}")
class CustomCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, NUM_EPOCHS, logs=None):
            files = [os.path.join(folder_path, file) for file in os.listdir     (folder_path)]
            files = [file for file in files if os.path.isfile(file)]

            if os.path.exists(txtpath):
                print("模型已存在，持續训練中")
                modeltraining=1
                if files:
                    latest_file = max(files, key=os.path.getctime)
                    latest_file_timestamp = os.path.getctime(latest_file)
                    latest_file_name = os.path.basename(latest_file)
                    print("最新文件:", latest_file_name)
                    print(time.strftime('%Y/%m/%d-%H:%M:%S',time.localtime  (latest_file_timestamp)))
                    modeltime=time.strftime('%Y/%m/%d-%H:%M:%S',time.localtime  (latest_file_timestamp))
                    start_time = time.time()
                    net_final.fit(train_batches,
                        steps_per_epoch = train_batches.samples // BATCH_SIZE,
                        validation_data = valid_batches,
                        validation_steps = valid_batches.samples // BATCH_SIZE,
                        epochs = NUM_EPOCHS)
                    end_time = time.time()
                    total_training_time = end_time - start_time
                    print("已訓練時間：", time.strftime("%H:%M:%S", time.gmtime(total_training_time)), "秒")
                    duration=time.strftime("%H:%M:%S", time.gmtime(total_training_time))
                    data_item ={"modeltraining":modeltraining,"epoch":NUM_EPOCHS,"model":random_filename,"time":modeltime,"duration":duration}
                    data_list.append(data_item)
                    json_data = json.dumps(data_list)  
                    json_data = json_data.replace('\n', '')
                    json_data = json_data.replace(' ', '')
                    json_data = json_data.replace('\\', '')
                    print(json_data)
                    #txth5name=os.path.splitext(random_filename)[0]
                    
                    #txt_filename = txth5name+'.txt'
                    # 将 JSON 数据保存到 TXT 文件
                    with open(txt_filename, 'w') as txt_file:
                        txt_file.write(json_data)
                        #sql1 = "UPDATE modelupdata SET   modelfile = %s   ORDER BY allmodelid DESC LIMIT 1"
                        #update_data = (json.dumps(json_data),)
                        #mycursor.execute(sql1,update_data)
                        #mydb.commit()
                        #print(new_record_id, "zz筆資料已匯入")
                
                        
                    print(f"JSON data has been saved to {txt_filename}")
                    
            else :modeltraining=0       
custom_callback = CustomCallback()
# 儲存訓練好的模型
#net_final.save(WEIGHTS_FINAL)
history = net_final.fit(
    train_batches,
    steps_per_epoch=train_batches.samples // BATCH_SIZE,
    validation_data=valid_batches,
    validation_steps=valid_batches.samples // BATCH_SIZE,
    epochs=NUM_EPOCHS,
    callbacks=[checkpoint, custom_callback]
)



