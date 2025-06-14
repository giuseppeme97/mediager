from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
import ffmpeg
import subprocess
import json
from datetime import datetime


class VideoCore():
    @staticmethod
    def read_video(file: str) -> object:
        return ffmpeg.probe(file)

    @staticmethod
    def get_year_from_video(video: object) -> str:
        return str(video['streams'][0]['tags']['creation_time'])[0:4]
    
    @staticmethod
    def get_date_from_video(file: str) -> str:
        try:
            # Esegui ffprobe per ottenere i metadati
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_entries', 'format_tags=creation_time',
                file
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            metadata = json.loads(result.stdout)

            # Estrai la data di creazione
            creation_time = metadata['format']['tags']['creation_time']
            dt = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H-%M-%S')
        except Exception as e:
            return f"Errore durante l'estrazione della data: {e}"


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
