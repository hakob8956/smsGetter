# SMS Notification System

This project consists of four main components:

1. **smsBot**: A Python-based Telegram bot.
2. **smsClientAndroid**: An Android application for sending notifications or messages to the smsServer.
3. **smsServer**: A Python Flask server that handles incoming messages from the smsClientAndroid and interacts with the smsBot.
4. **smsHealth**: A Python Flask server that monitors the health status of the other components and services.

## Getting Started

Below are the setup instructions for each component of the system.

### smsBot

#### Requirements

- Python 3
- Telegram Bot API Token

#### Configuration

First, you need to fill in the `config.json` with the necessary details:

```json
{
  "server_url": "server_url",
  "telegram_key": "telegram_key",
  "authKey": "authKey",
  "monitor_url": "monitor_url"
}
```

Replace `server_url`, `telegram_key`, `authKey`, and `monitor_url` with your actual values to ensure the bot can communicate effectively with the smsServer.

#### Running the Bot

To run the smsBot, use the following command:

```bash
python3 main.py
```

### smsClientAndroid

#### Requirements

- Android Studio
- Java SDK

#### Configuration

In `AppSettings.java`, set the server URL and server authentication value:

```java
public static final String SERVER_URL_VALUE = "SERVER_URL";
public static final String SERVER_AUTH_VALUE = "SERVER_AUTH_VALUE";
public static final String HEALTH_URL_VALUE = "HEALTH_URL/mobile";
```

Replace `SERVER_URL`, `SERVER_AUTH_VALUE`, and `HEALTH_URL` with the correct values for your setup.

#### Running the Client

Open the project in Android Studio, build the APK, and run it on your Android device or emulator.

### smsServer

#### Requirements

- Python 3
- Flask

#### Configuration

Create a `config.ini` file with the necessary database and authentication key settings:

```ini
[DEFAULT]
ConnectionStringMongoDb = YourMongoDbConnectionString
AuthTgKey = YourTelegramAuthKey
```

Replace `YourMongoDbConnectionString` and `YourTelegramAuthKey` with your actual MongoDB connection string and Telegram authentication key.

### smsHealth

#### Requirements

- Python 3
- Flask

#### Configuration

Create a `config.json` file with the necessary service URLs and authentication key settings:

```json
{
  "SERVICES": {
    "mongodb": "YourMongoDbConnectionString",
    "server": "http://yourserver.com/health"
  },
  "TELEGRAM_BOT_TOKEN": "YourTelegramBotToken",
  "AUTH_KEY": "YourAuthKey"
}
```

Replace `YourMongoDbConnectionString`, `YourTelegramBotToken`, and `YourAuthKey` with your actual MongoDB connection string, Telegram authentication token, and auth key.

#### Running the Servers

To start the smsServer and smsHealth, run the following command:

```bash
flask --app main.py run --host=0.0.0.0 --port=xxxx
```

Replace `xxxx` with the port number you want the server to listen on.

## Additional Information

For detailed information about each component, please refer to the individual documentation provided in the subdirectories of each module.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your improvements.
