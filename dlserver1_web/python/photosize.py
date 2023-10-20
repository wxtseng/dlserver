import sys
from PIL import Image

files = sys.argv[1:]
for f in files:
    img = Image.open(f)  # 此处修正
    (w, h) = img.size
    print('w=%d, h=%d' % (w, h))
    img.show()

    new_img = img.resize((224, 224))
    new_img.show()
    new_img.save("/home/dlserver1/dlserver1_web/python/compsize.png")
print("oksize")