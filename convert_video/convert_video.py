import logging
import os
import shutil
import subprocess
import json
from config import BASE_DIR


class MetaDataVideo:
    def __init__(self, filename):
        self.filename = filename
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', filename]
        output = subprocess.check_output(cmd).decode('utf-8')
        data = json.loads(output)
        self.file_size = int(data["format"]['size'])
        self.bit_rate = int(data["format"]['bit_rate'])


async def convert_video(size_file, bitrate, filename):
    path = filename.replace('//', '/').rstrip('/')
    filename = os.path.normpath(os.path.join(*path.split('/')))
    if size_file > 52428000:
        proc = (size_file - 52428000) / (52428000 / 100)
        bbb = bitrate - ((bitrate / 100) * proc)
        bitrate = int(int(bbb) / 1024)
        if bitrate < 0:
            bitrate = 128
        ffmpeg_command = ['ffmpeg', '-i', filename, '-b:v', f'{bitrate}k', '-y', f'{BASE_DIR}\convert_video.mp4']
        logging.info(f"convert video: {ffmpeg_command}")
        try:
            subprocess.run(ffmpeg_command)
        except Exception as ex:
            logging.info(f"error convert: {size_file}")
            return
        shutil.copy(f'{BASE_DIR}\convert_video.mp4', filename)
        os.remove(f'{BASE_DIR}\convert_video.mp4')