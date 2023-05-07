# Web stream frame capture docker image

This docker image is used to capture frames from a web stream and save them to a folder as images and send them to a telegram chat with a bot.

## Usage

### Docker

```bash
docker run -d -v /img:/app/img -e BOT_TOKEN=bot_token -e CHAT_ID=chat_id -e STREAM_URL=url -e CAPTURE_TIME=time image_name
```
That will run the image in the background and capture frames from the stream every day at `time` and save them to the /img folder and send them to the telegram chat with the bot.