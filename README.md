# Thought Keeper

Thought Keeper is a Telegram bot designed to make your life easier by converting audio messages into text. This bot is
perfect for those who need to quickly capture their thoughts, ideas, or important information without the hassle of
typing.

## Features

- **Voice to Text Conversion**: Converts your voice messages and audio files into written text.
- **Efficient and Fast**: Quickly processes audio messages, saving you valuable time.
- **User Authentication**: Ensures that only authorized users can access the bot. This will prevent unexpected
  OpenAI bills.
- **Support for Multiple Audio Formats**: Handles various audio formats and converts them into a compatible format
  for transcription. Recordings from other apps are allowed as well.
- **Simple and User-Friendly**: Easy to use with straightforward commands.

## How to Use

1. **Start the Bot**: Send `/start` to initiate the bot.
2. **Send an Audio Message**: Record your voice message or upload an audio file.
3. **Receive Transcription**: The bot transcribes your audio and replies with the text.

## Requirements

- Python 3.8 or higher
- Libraries: `python-telegram-bot`, `python-dotenv`, `openai`, `pydub`

## Installation

1. Clone the repository.
2. Install the required libraries: `pip install -r requirements.txt`
3. Set up your environment variables in a `.env` file:
    - `TELEGRAM_BOT_API_KEY`: Your Telegram bot API key.
    - `OPENAI_API_KEY`: Your OpenAI API key with Whisper-1 access.
    - `ALLOWED_USERS`: JSON array of allowed user IDs as integers.
4. Run the bot: `python telegram_bot_server.py`

## How to deploy to a Raspberry Pi

1. Clone the project to your Raspberry Pi
2. Set up a recent python version with `pyenv`, this might take a while.
3. Install the requirements
4. At this point you can just run the script with python or follow along to get automatic start of the server on
   reboots, crashes, etc.
5. `sudo nano /etc/systemd/system/telegram_bot.service`
   ```shell
    [Unit]
    Description=Telegram Bot Service
    After=network.target
    
    [Service]
    Type=simple
    User=pi
    WorkingDirectory=<path of the telegram bot folder>
    ExecStart=/home/pi/.pyenv/shims/python <absolute path of the python script>
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
    ```
6. `sudo systemctl enable telegram_bot.service`
7. `sudo systemctl start telegram_bot.service`
8. `sudo systemctl status telegram_bot.service`, you should see `active` status
9. `journalctl -u telegram_bot.service` to see the logs of the bot

## Security

- The bot is configured to work only with a predefined list of users.
- All interactions are logged for security purposes.

## How to set up the Telegram bot

1. Use the `@BotFather` to create your bot. Provide it a unique ID that also shows that it's private.
2. Pick a name for your bot, something simple like "Thought Keeper" that I picked.
3. Set up the about and description sections.
4. Set up the start and help commands (the actual command logic is in the code, just inform it that we support these
   commands and a short about of it)
5. Put a picture for your bot, can be generated with Dall-E.

## Contributing

Contributions to improve Thought Keeper are welcome. Please fork the repository and submit a pull request with your
changes.

## License

Thought Keeper is open-source and free to use under the MIT License.
