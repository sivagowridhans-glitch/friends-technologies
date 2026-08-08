"""
Local test script — Test Image folder-ல் இருக்குற ஏதாவது ஒரு
table image file name-ஐ கீழ 'sample_table.png' இடத்துல மாத்துங்க.
"""
import base64
from server import image_to_excel

IMAGE_PATH = "sample_table.png"  # <-- உங்க Test Image file peru இங்க போடுங்க

with open(IMAGE_PATH, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

result = image_to_excel(img_b64, "test_output.xlsx")
print(result)
