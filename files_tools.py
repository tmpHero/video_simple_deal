import os

def read_folder_videos(folder_path: str) -> list[str]|None:
    if not os.path.exists(folder_path):
        return
    return [os.path.join(folder_path, p) for p in os.listdir(folder_path) if p.endswith(".mp4")]

    


if __name__ == "__main__":
    folder_path = "datasets"
    videos = read_folder_videos(folder_path)
    print(videos)