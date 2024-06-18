from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
import ffmpeg

class VideoCore():
    @staticmethod
    def read_video(file: str) -> object:
        return ffmpeg.probe(file)
    
    @staticmethod
    def get_year_from_video(video: object) -> str:
        return str(video['streams'][0]['tags']['creation_time'])[0:4]


class PhotoCore():
    @staticmethod
    def read_image(file: str) -> object:
        register_heif_opener()
        return Image.open(file)
    
    @staticmethod
    def extract_exif_from_image(image: object) -> dict:
        return {ExifTags.TAGS[k]: v for k, v in image.getexif().items() if k in ExifTags.TAGS}

    @staticmethod
    def format_raw_date(raw_date: str) -> str:
        return f"{raw_date[0].replace(':', '-')} {raw_date[1].replace(':', '-')}"
    
    @staticmethod
    def get_date_from_exif(exif: dict) -> str:
        return PhotoCore.format_raw_date(str(exif['DateTime']).split(" "))