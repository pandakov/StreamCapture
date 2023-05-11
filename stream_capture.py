import time
from datetime import datetime
from functools import partial
from os import getenv
from zoneinfo import ZoneInfo

import cv2
import schedule
import telepot


def get_stream_frame(stream_url: str) -> cv2.UMat:
    """Get frame from stream"""
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Cannot load stream")
        return None
    _, frame = cap.read()
    cap.release()
    return frame


def save_stream_frame(stream_url: str, path: str) -> bool:
    """Save frame from stream to file"""
    frame = get_stream_frame(stream_url)
    if frame is None:
        return False
    try:
        cv2.imwrite(path, frame)
    except Exception as e:
        print("Error saving image: ", e)
        return False
    return True


def send_stream_frame(stream_url: str, bot: telepot.Bot, chat_id: str) -> bool:
    """Send frame from stream by bot"""
    captured = save_stream_frame(stream_url, "tmp.jpg")
    if not captured:
        return False
    try:
        bot.sendPhoto(chat_id, "tmp.jpg")
    except Exception as e:
        print("Error sending photo: ", e)
        return False
    return True


def get_capture(
    stream_url: str,
    bot: telepot.Bot,
    chat_id: str,
    timezone: str = "Europe/Moscow",
    img_path: str = "img",
):
    """Job for scheduler"""
    dt_string = datetime.now(ZoneInfo(timezone)).strftime("%Y-%m-%d__%H-%M")
    fname = f"{img_path}/{dt_string}.jpg"
    captured = save_stream_frame(stream_url, fname)
    if captured:
        try:
            bot.sendPhoto(chat_id, open(fname, "rb"))
        except Exception as e:
            print("Error sending photo: ", e)
    else:
        try:
            bot.sendMessage(chat_id, "Cannot load stream")
        except Exception as e:
            print("Error sending message: ", e)
        print("Cannot load stream")


if __name__ == "__main__":
    # Load environment variables
    print("Loading environment variables...", end=" ")
    bot_token = str(getenv("BOT_TOKEN"))
    chat_id = str(getenv("CHAT_ID"))
    stream_url = str(getenv("STREAM_URL"))
    capture_time = str(getenv("CAPTURE_TIME"))
    print("done")

    # Create bot
    print("Creating bot...", end=" ")
    bot = telepot.Bot(bot_token)
    bot.sendMessage(
        chat_id,
        f"Bot started for capture frames from stream\n\n{stream_url}\n\nevery day at {capture_time} (UTC)",
    )
    print("done")

    # Create job for scheduler
    job = partial(get_capture, stream_url, bot, chat_id)

    # Test job
    print("Testing bot...")
    job()
    print("done")

    # Creating scheduler
    schedule.every().day.at(capture_time).do(job)

    # Run scheduler
    print("Starting scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(10)
