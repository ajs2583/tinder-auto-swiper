# Tinder Auto-Swiper 🤖❤️

This Python automation tool uses Selenium to log into Tinder via Facebook and automatically swipe right (like) on profiles.

## Features

- Logs into Tinder using your Facebook credentials
- Automates swiping right every few seconds
- Uses environment variables to protect your login details

## Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/ajs2583/tinder-auto-swiper.git
cd tinder-auto-swiper
```

### 2. Set up the Environment

Make sure you have Python 3 and Google Chrome installed.

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Facebook login credentials:

```env
FACEBOOK_PHONE_NUMBER=your_facebook_email_or_phone
FACEBOOK_PASSWORD=your_facebook_password
```

### 4. Run the Script

```bash
python main.py
```

Use `Ctrl+C` to stop the bot.

## Requirements

Install dependencies with:

```bash
pip install selenium python-dotenv
```

## ⚠️ Disclaimer

This project is intended for **educational purposes only**.

Using automation tools like this may violate Tinder's [Terms of Service](https://policies.tinder.com/terms). Use responsibly and at your own risk.

Facebook and Tinder login flows may change over time and break the script — maintenance is up to you.

## Author

Created by Andrew Sliva  
[GitHub Profile](https://github.com/ajs2583)
