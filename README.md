##About
This is a house rental Telegram bot that aims to help:
Students to find suitable housing
Houseowners to rent out their housings to students.
##Installation
1. Install [Python 3.10](https://www.python.org/downloads/release/python-31010/)
2. Open console and clone the repository:
   ```bash
   git clone https://github.com/Shahzodolimjonov/Rent-Housing.git
   ```
3. Install a virtual environment:
   ```bash
   python -m venv venv
   ```
   ```bash
   .\venv\Scripts\activate
   ```
5. Install the required Python packages using pip:
   ```bash
   pip install
   ```
   
Install the required packages using the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
```
## Create a New Bot
To create a new Telegram bot, follow these steps:

1. Open [BotFather](https://t.me/BotFather) on Telegram.  
2. Click "Start" to begin the setup.  
3. Type `/newbot` and follow the instructions to create your bot.  
4. Once completed, you will receive a **Bot Token**. Save this token securely.

##Create a New Database
```bash
DATABASE_URL = "postgresql://DB_USER:DB_PASSWORD@localhost/DB_NAME"
```
##Run the bot using the following command:
```bash
python bot.py
```
Run the docker using the following command:
```bash
docker-compose up
```

