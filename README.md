# Flow3 Auto Bot
*Flow3 Auto Bot is an automation script to perform various tasks on the SolixDepin platform, such as registration, login, completing tasks, and mining.*
- Register : [HERE](https://app.flow3.tech/sign-up?ref=BBpc9vlkXP)

## Features
1. **Clear Task**: complete available tasks.
2. **Mining**: Perform automatic mining to earn points.
3. **Batch Processing**: Process multiple accounts at once in batches using asynchronous programming.
4. **Add Referrer**: SOON

## Requirements
- Python 3.8 or latest

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Fxyt/flow3.git
   cd flow3
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Configuration
1. Create an `token.txt` file and fill RefreshToken
  - Log in to Flow3
  - Open your browser's developer tools (F12) or Inspect
  - Go to the
      -> Application
      -> Flow3
      -> Extension Storage
      -> local
      -> refresh_token
<p align="center">
    <img width="800" alt="image" src="img2.png">
</p>

2. Fill your RefreshToken in token.txt like this
   ```bash
   eyJRefreshToken...1
   eyJRefreshToken...2
   eyJRefreshToken...3
   ```

## How to use
Run the main script:
   ```bash
   python bot.py
   ```
   if in VPS or Linux:
   ```bash
   python3 bot.py
   ```
## Output Example
<p align="center">
    <img width="600" alt="image" src="img1.png">
</p>

## Dependencies
- **Asyncio** - A Python library used to write asynchronous code. It allows the program to handle multiple tasks concurrently, such as making API requests or performing background tasks without blocking the main thread.
- **AioHTTP** - An asynchronous HTTP client/server library for Python. It is used to make non-blocking HTTP requests, which is essential for interacting with APIs in an efficient way.
- **Loguru** - A modern logging library for Python. It simplifies logging by providing an easy-to-use interface and advanced features like structured logging, log rotation, and better formatting for debugging.
