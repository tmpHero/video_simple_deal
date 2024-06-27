from threading import Thread
import logging
from cv_deal_video import *
from files_tools import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
detection_algorithms_list: list[object] = [ContentDetector, ThresholdDetector, AdaptiveDetector, HistogramDetector, HashDetector]


set_work_threads: int = 0
set_clear_short_time: float = 0
use_detection_algorithms_index: int = 0
videos_datasets: list = []
audio_number: int = 0
is_mix: bool = True


def check_input_dataset() -> bool:
    global videos_datasets, audio_number

    try:
        datasets_path = input("Enter the data set path .[default: datasets]:").replace(" ", "") or "datasets" 
        videos_datasets = read_folder_videos(datasets_path)
        audio_number = len(videos_datasets)
        if videos_datasets is None or audio_number == 0:
            logging.error(f"File: {datasets_path} ???")
            return False
    except ValueError:
        logging.error(f"File: {datasets_path} ??? Please re-enter")
        return False
    
    
    return True


def check_input() -> bool:
    global is_mix, set_work_threads, set_clear_short_time, use_detection_algorithms_index

    try:
        is_mix = (input("Whether to mix ?(y/n)[default: y]:").replace(" ", "") or "y") == "y"
        set_work_threads = int(input(f"Set thread count[default: Audio number: {audio_number}]:").replace(" ", "") or f'{audio_number}')
        set_clear_short_time = float(input(f"Set clear short time[default: 5.000 s]:").replace(" ", "") or 5)
        logging.info("""
                    Detection Algorithms:
            ContentDetector  (0): 使用HSV色彩空间中像素变化的加权平均值来检测镜头变化。
            ThresholdDetector(1): 使用RGB的平均像素强度(渐入/渐出)检测缓慢的过渡
            AdaptiveDetector (2): 对HSV色彩空间的差异执行滚动平均。在某些情况下，这可以改善对快速动作的处理。
            HistogramDetector(3): 使用YUV空间中Y通道的直方图差异来查找快速切割。
            HashDetector     (4): 使用感知哈希来计算相邻帧之间的相似性。
        """)
        use_detection_algorithms_index = int(input(f"Detection Algorithms(0, ..., 4)[default: 0]: ").replace(' ', '') or 0)
        if use_detection_algorithms_index < 0 or use_detection_algorithms_index > 4:
            logging.error("Input Error, please re-enter")
            return False
    except ValueError:
        logging.error("Input Error, please re-enter")
        return False

    return True


"""
    version: v1.0
    Author: 2024-06-26
"""

import ctypes

# 定义 SetConsoleTitle 函数的参数类型
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleTitleW("Scene cutting")
del kernel32

from concurrent.futures import ThreadPoolExecutor

if __name__ == '__main__':
    logging.info("Starting...")
    logging.info("version: v1.0")

    while (not check_input_dataset()) :
        pass

    while (not check_input()):
        pass    

    use_detection_algorithms = detection_algorithms_list[use_detection_algorithms_index]

    max_work_threads: int = min(set_work_threads, audio_number)

    logging.info(f"Audio number: {audio_number}")
    logging.info(f"All audio paths: {videos_datasets}")
    logging.info(f"Max work threads: {max_work_threads}")
    logging.info(f"Clear short time: {set_clear_short_time:6.3f}s")
    logging.info(f"Detection Algorithms: {use_detection_algorithms}")


    # detect_scenes
    with ThreadPoolExecutor(max_workers=max_work_threads) as executor:
        executor.map(detect_scenes, [
            [video_path, f'output/output_{cnt}' if not is_mix else "output_mix", set_clear_short_time, use_detection_algorithms]
            for video_path, cnt in zip(videos_datasets, range(audio_number))
        ])
        

    
    logging.info(f"All Done: {f'output' if not is_mix else "output_mix"}")

    input(f"Whether to open the output result ?(y/n)[default: y]: ") or "y" == "y" and \
    os.system(f"start {f'output' if not is_mix else 'output_mix'}")





