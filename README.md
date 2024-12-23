## About
This is a house rental Telegram bot that aims to help:
Students to find suitable housing
Houseowners to rent out their housings to students.
## Installation
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

## Create a New Database
To crate a new database, follow the tutorial at [w3schools](https://www.w3schools.com/postgresql/index.php)

## Add your database, bot token and your account id into the program
Open ".env" file and apply these changes:
1. Change .env.example into .env
2. Input your account id (you can take it from @userinfobot) for ADMINS
3. Input your bot token for BOT_TOKEN
4. Input your database URL as follows:
```bash
DATABASE_URL = "postgresql://DB_USER:DB_PASSWORD@localhost/DB_NAME"
```
## Run the bot using the following command:
```bash
python bot.py
```
## Run the docker using the following command:
1. Open a terminal or command prompt on your computer.
2. Navigate to the directory where your ```docker-compose.yml``` file is located.
3. Type ```docker-compose up``` and press Enter.
```bash
docker-compose up
```

