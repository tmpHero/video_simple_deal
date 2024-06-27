"""
ContentDetector:使用HSV色彩空间中像素变化的加权平均值来检测镜头变化。

ThresholdDetector:使用RGB的平均像素强度(渐入/渐出)检测缓慢的过渡

AdaptiveDetector:对HSV色彩空间的差异执行滚动平均。在某些情况下，这可以改善对快速动作的处理。

HistogramDetector:使用YUV空间中Y通道的直方图差异来查找快速切割。

HashDetector:使用感知哈希来计算相邻帧之间的相似性。
"""
from scenedetect import detect, split_video_ffmpeg, ContentDetector, ThresholdDetector, AdaptiveDetector, HistogramDetector, HashDetector
import os
import logging


def time_to_str(time: float) -> str:
    return f"{int(time//3600):02d}:{int(time%3600//60):02d}:{time%60:0>6.3f}"

def str_to_time(time_str: str) -> float:
    return sum((int(x) if i != 0 else float(x)) * 60**i for i, x in enumerate(reversed(time_str.split(":"))))

# tuple[scenedetect.frame_timecode.FrameTimecode]
def get_voide_time(voide_frame_info: tuple) -> float:
    start_time = voide_frame_info[0].get_timecode()
    end_time = voide_frame_info[-1].get_timecode()
    return str_to_time(end_time) - str_to_time(start_time)

# def detect_scenes(input_video: str, output_dir: str, clear_short_video: None|float = None, DetectionAlgorithms: object=ContentDetector) -> bool:
def detect_scenes(*argv) -> bool:
    print(f"argv: {argv}")
    input_video, output_dir, clear_short_video, DetectionAlgorithms = argv[0]
    if not os.path.exists(input_video):
        logging.error(f"File: {input_video} ???")
        return False
    scene_list = detect(input_video, DetectionAlgorithms(), show_progress=True)
    if clear_short_video:
        scene_list = [scene_lst for scene_lst in scene_list if get_voide_time(scene_lst) > clear_short_video]

    split_video_ffmpeg(input_video, scene_list, output_dir=output_dir, show_progress=True)

    return True



import argparse

def run(argv: argparse.Namespace ):
    
    video_path = argv.input_video
    output_dir = argv.output_dir
    clear_short_video = argv.clear_short_video
    DetectionAlgorithms = argv.DetectionAlgorithms
    detect_scenes(
        video_path, 
        output_dir, 
        clear_short_video, 
        DetectionAlgorithms
    )
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="视频场景检测")
    parser.add_argument("-i", "--input_video", type=str, required=True)
    parser.add_argument("-o", "--output_dir", type=str, default="output/")
    parser.add_argument("-s", "--clear_short_video", type=float, default=10.0)
    parser.add_argument("-d", "--DetectionAlgorithms", type=object, default=ContentDetector)
    args = parser.parse_args()

    run(args)

