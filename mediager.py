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
                os.rename(f"{self.folder}/{file}",
                          f"{self.folder}/{final_date}{ext}")
                
    def check_rename_videos_by_date(self):
        for file in self.get_files_list(self.folder):
            if not file.startswith('.') and self.is_valid_file(file):
                print(file)
                _, ext = os.path.splitext(f"{self.folder}/{file}")
                try:
                    final_date = VideoCore.get_date_from_video(f"{self.folder}/{file}")
                    print(f"Rinomino {self.folder}/{file} in {self.folder}/{final_date}{ext}")
                except:
                    print("Data non estraibile da:", file)

    def rename_videos_by_date(self):
        for file in self.get_files_list(self.folder):
            if not file.startswith('.') and self.is_valid_file(file):
                print(file)
                _, ext = os.path.splitext(f"{self.folder}/{file}")
                try:
                    final_date = VideoCore.get_date_from_video(f"{self.folder}/{file}")
                    os.rename(f"{self.folder}/{file}", f"{self.folder}/{final_date}{ext}")
                except:
                    print("Data non estraibile da:", file)

    def show_menu(self) -> int:
        print("\n*** Mediager ***")
        print("0 - Esci")
        print("1 - Rinomina foto per data")
        print("2 - Controlla rinominazione video per data")
        print("3 - Rinomina video per data")
        print("4 - Controlla foto duplicate")
        print("5 - Controlla video duplicati")
        return int(input("-> "))

    def start(self) -> None:
        while True:
            actions = {
                0: sys.exit,
                1: self.rename_photos_by_date,
                2: self.check_rename_videos_by_date,
                3: self.rename_videos_by_date,
                4: self.check_duplicate_photos,
                5: self.check_duplicate_videos
            }
            actions.get(self.show_menu(), lambda x: print("Comando non valido."))()


if __name__ == "__main__":
    # mediager = Mediager("./ok")
    mediager = Mediager("/Volumes/SSK SSD/Video/Montaggi")
    mediager.start()
