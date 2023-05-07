import cv2
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import telepot

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
    parser.add_argument("-b", "--bot", help="telegram bot token")
    parser.add_argument("-c", "--chat", help="telegram chat id")
    args = parser.parse_args()

    if args.url is None:
        print("Need stream url")
        exit(1)

    # Get current datetime
    dt_string = datetime.now(ZoneInfo(args.timezone)).strftime("%Y-%m-%d__%H-%M")

    # Save image from stream
    fname = f"{args.path}/{dt_string}.jpg"
    save_stream_frame(args.url, fname)

    # Send image by bot
    if args.bot is not None and args.chat is not None:
        bot = telepot.Bot(args.bot)
        bot.sendPhoto(args.chat, open(fname, 'rb'))
