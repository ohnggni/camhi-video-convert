import os
import time
import subprocess
from datetime import datetime
import shutil

WATCH_DIR = "/home/ohnggni/camhi"  # 모니터링할 디렉토리
FFMPEG_PATH = "/usr/bin/ffmpeg"    # FFmpeg 경로
TIME_THRESHOLD = 180  # 3분 = 180초

def is_old_enough(file_path):
    """파일이 현재 시간보다 3분 이상 이전에 생성되었는지 확인"""
    current_time = time.time()
    file_mtime = os.path.getmtime(file_path)
    return (current_time - file_mtime) > TIME_THRESHOLD

def convert_to_mkv(file_path):
    """265 파일을 mkv로 변환"""
    output_path = file_path.replace(".265", ".mkv")
    command = [
        FFMPEG_PATH,
        "-y",                      # 동일한 파일 덮어쓰기
        "-i", file_path,           # 입력 파일
        "-c", "copy",              # 재인코딩 없이 컨테이너만 변경
        output_path
    ]
    try:
        print(f"[{datetime.now()}] Converting: {file_path} -> {output_path}")
        subprocess.run(command, check=True)
        print(f"[{datetime.now()}] Conversion complete: {output_path}")
        os.remove(file_path)  # 변환 후 원본 파일 삭제
        print(f"[{datetime.now()}] Deleted original file: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] FFmpeg error: {e}")
    except Exception as e:
        print(f"[{datetime.now()}] Unexpected error: {e}")

def move_to_parent_dir(file_path):
    """변환된 MKV 파일을 한 단계 상위 디렉토리로 이동"""
    parent_dir = os.path.dirname(os.path.dirname(file_path))  # 상위 디렉토리 경로 계산
    destination_path = os.path.join(parent_dir, os.path.basename(file_path))  # 최종 이동 경로
    try:
        shutil.move(file_path, destination_path)
        print(f"[{datetime.now()}] Moved: {file_path} -> {destination_path}")
    except Exception as e:
        print(f"[{datetime.now()}] Failed to move {file_path}: {e}")

def monitor_directory(directory):
    """디렉토리를 모니터링하며 변환 및 이동 작업 수행"""
    print(f"[{datetime.now()}] Monitoring directory: {directory}")
    processed_files = set()

    while True:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".265"):
                    file_path = os.path.join(root, file)
                    if file_path not in processed_files and is_old_enough(file_path):
                        # MKV 변환
                        converted_file = convert_to_mkv(file_path)
                        if converted_file:
                            # 상위 디렉토리로 이동
                            move_to_parent_dir(converted_file)
                        processed_files.add(file_path)
        time.sleep(30)  # 30초마다 디렉토리 확인

if __name__ == "__main__":
    monitor_directory(WATCH_DIR)
