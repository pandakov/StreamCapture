import cv2
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse

def get_stream_frame(stream_url: str) -> cv2.UMat:
    '''Get frame from stream'''
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Cannot load stream")
        return None
    _, frame = cap.read()
    cap.release()
    return frame

def save_stream_frame(stream_url: str, path: str) -> bool:
    '''Save frame from stream to file'''
    frame = get_stream_frame(stream_url)
    if frame is None:
        return False
    cv2.imwrite(path, frame)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="url to stream")
    parser.add_argument("-p", "--path", help="path to save image", default="img")
    parser.add_argument("-t", "--timezone", help="timezone", default="Europe/Moscow")
    args = parser.parse_args()
    if args.url is None:
        print("Need stream url")
        exit(1)
    dt_string = datetime.now(ZoneInfo(args.timezone)).strftime("%Y-%m-%d__%H-%M")
    save_stream_frame(args.url, f"{args.path}/{dt_string}.jpg")
