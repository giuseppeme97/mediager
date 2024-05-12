import ffmpeg
from pprint import pprint
import os
import shutil
import datetime

cartella = "/Users/giuseppe/Desktop/Video"
contenuto_cartella = os.listdir(cartella)
solo_file = [f for f in contenuto_cartella if os.path.isfile(os.path.join(cartella, f))]
with_errors = []

for file in solo_file:
    print(file)
    try:
        vid = ffmpeg.probe(f"{cartella}/{file}")
        anno = str(vid['streams'][0]['tags']['creation_time'])[0:4]

        if not os.path.exists(f"{cartella}/{anno}"):
            os.makedirs(f"{cartella}/{anno}")

        shutil.move(f"{cartella}/{file}", f"{cartella}/{anno}")
        print(f"Spostato {file} in {anno}")
        
    except:
        print("Errore con", file)  
            
