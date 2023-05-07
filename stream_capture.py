import cv2
from datetime import datetime
from zoneinfo import ZoneInfo
import telepot
import schedule
import time
from os import getenv

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

def send_stream_frame(stream_url: str, bot: telepot.Bot, chat_id: str) -> bool:
    '''Send frame from stream by bot'''
    captured = save_stream_frame(stream_url, 'tmp.jpg')
    if not captured:
        return False
    try:
        bot.sendPhoto(chat_id, 'tmp.jpg')
    except Exception as e:
        print('Error sending photo: ', e)
        return False
    return True

def job(stream_url: str, bot: telepot.Bot, chat_id: str, img_path: str, timezone: str):
    '''Job for scheduler'''
    dt_string = datetime.now(ZoneInfo(timezone)).strftime("%Y-%m-%d__%H-%M")
    fname = f"{img_path}/{dt_string}.jpg"
    frame = get_stream_frame(stream_url)
    if frame is not None:
        try:
            cv2.imwrite(fname, frame)
        except Exception as e:
            print('Error saving photo: ', e)
        try:
            bot.sendPhoto(chat_id, open(fname, 'rb'))
        except Exception as e:
            print('Error sending photo: ', e)
    else:
        print("Cannot load stream")

if __name__ == "__main__":
    # Load environment variables
    print('Loading environment variables...', end=' ')
    bot_token = str(getenv('BOT_TOKEN'))
    chat_id = str(getenv('CHAT_ID'))
    stream_url = str(getenv('STREAM_URL'))
    img_path = str(getenv('IMG_PATH'))
    timezone = str(getenv('TIMEZONE'))
    capture_time = str(getenv('CAPTURE_TIME'))
    print('done')

    # Create bot
    print('Creating bot...', end=' ')
    bot = telepot.Bot(bot_token)
    print('done')

    # Schedule
    schedule.every().day.at(capture_time).do(job, stream_url, bot, chat_id, img_path, timezone)

    # Scheduler
    print('Starting scheduler...')
    while True:
        schedule.run_pending()
        time.sleep(10)