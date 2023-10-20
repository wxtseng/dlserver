import sys
from PIL import Image

files = sys.argv[1:]
for f in files:
    img = Image.open(f)
    img = img.convert('RGB')
    width, height = img.size
    left = (width - 224) // 2
    top = (height - 224) // 2
    right = (width + 224) // 2
    bottom = (height + 224) // 2
    region = img.crop((left, top, right, bottom))
    region.save('/home/dlserver1/dlserver1_web/python/compcut.png')
print("okcut")