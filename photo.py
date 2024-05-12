from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from pprint import pprint
import os
from collections import defaultdict

register_heif_opener()
cartella = "./2024"
files = [f for f in os.listdir(cartella) if os.path.isfile(os.path.join(cartella, f))]
#print(len(files))
all = []
conteggio = defaultdict(int)

for i, file in enumerate(files):
    if file == ".DS_Store":
        continue
    _, ext = os.path.splitext(f"{cartella}/{file}")
    img = Image.open(f"{cartella}/{file}")
    exif = { ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in ExifTags.TAGS }
    raw = str(exif['DateTime']).split(" ")
    date = raw[0]
    time = raw[1]
    final = f"{date.replace(":", "-")} {time.replace(":", "-")}"
    all.append({"original": file, "final": f"{final}{ext}"})
    conteggio[f"{final}{ext}"] += 1
    #print(i, f"{final}{ext}")
    os.rename(f"{cartella}/{file}", f"{cartella}/{final}{ext}")

# for e in sorted(all, key=lambda x: x["final"]):
#     if conteggio[e["final"]] > 1:
#         print(e)