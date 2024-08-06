import os
from core import PhotoCore, VideoCore
import shutil
from collections import defaultdict
import sys

class Mediager():
    def __init__(self, folder: str) -> None:
        self.folder = folder

    def set_folder(self, folder: str) -> None:
        self.folder = folder

    def get_files_list(self, folder: str) -> list:
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(self.folder, f))]    

    def is_valid_file(self, file: str) -> bool:
        return file not in (".DS_Store")
    
    def get_void_counters(self) -> tuple:
        return [], defaultdict(int)

    def check_duplicate_photos(self):
        all_photos, counts = self.get_void_counters()
        flag = False
        for file in self.get_files_list(self.folder):
            if self.is_valid_file(file):
                image = PhotoCore.read_image(f"{self.folder}/{file}")
                exif = PhotoCore.extract_exif_from_image(image)
                final_date = PhotoCore.get_date_from_exif(exif)         
                all_photos.append({"original": file, "final": final_date})
                counts[final_date] += 1

        for element in sorted(all_photos, key=lambda x: x["final"]):
            if counts[element["final"]] > 1:
                flag = True
                print(element)
        
        if not flag:
            print("Nessuna foto duplicata.")
                    
    def check_duplicate_videos(self):
        pass
    
    def rename_photos_by_date(self) -> None:
        for file in self.get_files_list(self.folder):
            if self.is_valid_file(file):
                _, ext = os.path.splitext(f"{self.folder}/{file}")
                image = PhotoCore.read_image(f"{self.folder}/{file}")
                exif = PhotoCore.extract_exif_from_image(image)
                final_date = PhotoCore.get_date_from_exif(exif)         
                os.rename(f"{self.folder}/{file}", f"{self.folder}/{final_date}{ext}")
            
    def rename_videos_by_date(self):
        pass

    def move_photo_by_year(self):
        pass

    def move_videos_by_year(self):
        for file in self.get_files_list(self.folder):
            video = VideoCore.read_video(file)
            year = VideoCore.get_year_from_video(video) 

            new_folder = f"{self.folder}/{year}"

            if not os.path.exists(new_folder):
                os.makedirs(new_folder)

            shutil.move(f"{self.folder}/{file}", new_folder)
            print(f"Spostato {file} in {year}.")

    def show_menu(self) -> int:
        print("\n*** Mediager ***")
        print("0 - Esci")
        print("1 - Rinomina foto per data")
        print("2 - Sposta foto per anno")
        print("3 - Rinomina video  per data")
        print("4 - Sposta video per anno")
        print("5 - Controlla foto duplicate")
        print("6 - Controlla video duplicati")
        return int(input("-> "))

    def start(self) -> None:
        while True:
            actions = {
                0: sys.exit,
                1: self.rename_photos_by_date,
                2: self.move_photo_by_year,
                3: self.rename_videos_by_date,
                4: self.move_videos_by_year,
                5: self.check_duplicate_photos,
                6: self.check_duplicate_videos
            }
            actions.get(self.show_menu(), lambda x: print("Comando non valido."))()
            

if __name__ == "__main__":
    mediager = Mediager("./ok")
    mediager.start()


