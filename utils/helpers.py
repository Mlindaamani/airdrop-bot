from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from mysql.connector import connect
import os
from telegram import Update
from telegram.ext import ConversationHandler
from captcha import CaptchaGenerator


load_dotenv('.env')
generator = CaptchaGenerator(captcha_size_num=5)

load_dotenv('.env')

(JOIN_TELEGRAM,
 JOIN_TWITTER,
 JOIN_LINKEDIN,
 JOIN_INSTAGRAM,
 JOIN_FACEBOOK
 ) = range(5)

LINKS = {
    JOIN_TELEGRAM: 'https://t.me/joinchat/AAAAAFY3Hf2JvH2n3Y1Y4Q',
    JOIN_TWITTER: 'https://twitter.com/techwithtim',
    JOIN_LINKEDIN: 'https://www.linkedin.com/in/tim-ruscica-4b2a651b0/',
    JOIN_INSTAGRAM: 'https://www.instagram.com/tech_with_tim/',
    JOIN_FACEBOOK: 'https://www.facebook.com/TechWithTim'

}


def create_reply_markup():
    keyboard = [
        [InlineKeyboardButton("Join Telegram", url=LINKS[JOIN_TELEGRAM])],
        [InlineKeyboardButton("Follow on Twitter", url=LINKS[JOIN_TWITTER])],
        [InlineKeyboardButton("Connect on LinkedIn",
                              url=LINKS[JOIN_LINKEDIN])],
        [InlineKeyboardButton("Follow on Instagram",
                              url=LINKS[JOIN_INSTAGRAM])],
        [InlineKeyboardButton("Like on Facebook", url=LINKS[JOIN_FACEBOOK])]
    ]
    return InlineKeyboardMarkup(keyboard)


def gen_math_captcha_image(difficult_level=2, multicolor=False, allow_multiplication=True, margin=False):
    math_model = generator.gen_math_captcha_image(
        difficult_level=difficult_level,
        multicolor=multicolor,
        allow_multiplication=allow_multiplication,
        margin=margin
    )
    math_image = math_model.image
    math_equation_results = math_model.equation_result
    math_image.save('captcha_maze/math.png')
    return math_equation_results


def gen_captcha_image(difficult_level=2, multicolor=False, margin=False):
    image_model = generator.gen_captcha_image(
        difficult_level=difficult_level,
        multicolor=multicolor,
        margin=margin)
    image = image_model.image
    image_characters = image_model.characters
    image.save('captcha_maze/image.png')
    return image_characters


def create_inline_markup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text='Join Telegram Group',
                                 callback_data='telegram'),
            InlineKeyboardButton(text='Join Twitter', callback_data='twitter')
        ],

        [
            InlineKeyboardButton(text='Join Instagram',
                                 callback_data='instagram'),
            InlineKeyboardButton(text='Send ETH Wallet',
                                 callback_data='wallet')
        ]
    ])


def add_bsc_address(update: Update, context):
    update.message.reply_text(
        "Please send your binance smart chain address to continue")
    return ConversationHandler.END


def verify_eth_address(update: Update, context):

    update.message.reply_text(
        "Please send a screenshot of your ethereum wallet to continue")
    return ConversationHandler.END


def verify_bsc_address(update: Update, context):
    user = update.message.from_user
    update.message.reply_text(
        "Please send a screenshot of your binance smart chain wallet to continue")
    return ConversationHandler.END


def verify_twitter(update: Update, context):
    update.message.reply_text(
        "Please send a screenshot of your twitter profile to continue")
    return ConversationHandler.END


def verify_linkedin(update: Update, context):
    update.message.reply_text(
        "Please send a screenshot of your linkedin profile to continue")
    return ConversationHandler.END


def verify_instagram(update: Update, context):
    update.message.reply_text(
        "Please send a screenshot of your instagram profile to continue")
    return ConversationHandler.END


def verify_facebook(update: Update, context):
    update.message.reply_text(
        "Please send a screenshot of your facebook profile to continue")
    return ConversationHandler.END


def unban_user(update: Update, context):
    user = update.message.from_user
    user_id = user.id
    user_name = user.first_name
    user_username = user.username
    user_email = user.email
    user_phone_number = user.phone_number
    user_location = user.location
    add_user(user_name, user_username, user_email,
             user_phone_number, user_location)
    update.message.reply_text(
        "You have been unbanned from our community. You can now participate in our events and win amazing prizes.")
    return ConversationHandler.END


def ban_user(update: Update, context):
    user = update.message.from_user
    user_id = user.id
    delete_user(user_id)
    update.message.reply_text(
        "You have been banned from our community. You can no longer participate in our events.")
    return ConversationHandler.END


def generate_invite_link(update: Update, context):
    user = update.message.from_user
    user_name = user.first_name
    user_username = user.username
    user_email = user.email
    user_phone_number = user.phone_number
    user_location = user.location
    add_user(user_name, user_username, user_email,
             user_phone_number, user_location)
    update.message.reply_text(
        "Here is your invite link: https://t.me/joinchat/AAAAAFY3Hf2JvH2n3Y1Y4Q")
    return ConversationHandler.END


def get_connection():
    return connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv('DATABASE_NAME'))


def create_database():
    connection = connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv("DATABASE_PASSWORD"))
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS " +
                   os.getenv('DATABASE_NAME'))
    cursor.close()
    connection.close()
    return "Database created successfully"


def create_table():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), username VARCHAR(255), email VARCHAR(255), phone_number VARCHAR(255), location VARCHAR(255))")
    connection.commit()
    cursor.close()
    connection.close()
    return "Table created successfully"


def get_user_by_id(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user if user else "User not found!"


def get_users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users


def add_user(name, username, email, phone_number, location):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, username, email, phone_number, location) VALUES (%s, %s, %s, %s, %s)",
                   (name, username, email, phone_number, location))
    connection.commit()
    cursor.close()
    connection.close()
    return "User added successfully"


def update_user(id, name, username, email, phone_number, location):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET name=%s, username=%s, email=%s, phone_number=%s, location=%s WHERE id=%s",
                   (name, username, email, phone_number, location, id))
    connection.commit()
    cursor.close()
    connection.close()
    return "User updated successfully"


def delete_user(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return "User deleted successfully"


def delete_all_users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users")
    connection.commit()
    cursor.close()
    connection.close()
    return "All users deleted successfully"


def get_user_by_username(username):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user if user else "User not found!"


def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user if user else "User not found!"


def get_user_by_phone_number(phone_number):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE phone_number=%s",
                   (phone_number,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user if user else "User not found!"


def get_user_by_location(location):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE location=%s", (location,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user if user else "User not found!"


def get_user_by_name(name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE name=%s", (name,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user if user else "User not found!"


def get_refferals():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE reffered_by IS NOT NULL")
    refferals = cursor.fetchall()
    cursor.close()
    connection.close()
    return refferals


def close_airdrop():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET airdrop_status = 'closed'")
    connection.commit()
    cursor.close()
    connection.close()
    return "Airdrop closed successfully"


def open_airdrop():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET airdrop_status = 'open'")
    connection.commit()
    cursor.close()
    connection.close()
    return "Airdrop opened successfully"


def get_airdrop_status():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE airdrop_status = 'open'")
    airdrop_status = cursor.fetchone()
    cursor.close()
    connection.close()
    return airdrop_status


def get_participants():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE airdrop_status = 'open'")
    participants = cursor.fetchall()
    cursor.close()
    connection.close()
    return participants


def get_banned_users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE airdrop_status = 'closed'")
    banned_users = cursor.fetchall()
    cursor.close()
    connection.close()
    return banned_users


def get_reffered_users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE reffered_by IS NOT NULL")
    reffered_users = cursor.fetchall()
    cursor.close()
    connection.close()
    return reffered_users


def get_unreffered_users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE reffered_by IS NULL")
    unreffered_users = cursor.fetchall()
    cursor.close()
    connection.close()
    return unreffered_users


def export_participants_in_csv_file():
    participants = get_participants()
    with open('participants.csv', 'w') as file:
        for participant in participants:
            file.write(f'{participant[0]},{participant[1]},{participant[2]},{
                       participant[3]},{participant[4]},{participant[5]}\n')
    return "Participants exported successfully"


def export_banned_users_in_csv_file():
    banned_users = get_banned_users()
    with open('banned_users.csv', 'w') as file:
        for banned_user in banned_users:
            file.write(f'{banned_user[0]},{banned_user[1]},{banned_user[2]},{
                       banned_user[3]},{banned_user[4]},{banned_user[5]}\n')
    return "Banned users exported successfully"


def export_reffered_users_in_csv_file():
    reffered_users = get_reffered_users()
    with open('reffered_users.csv', 'w') as file:
        for reffered_user in reffered_users:
            file.write(f'{reffered_user[0]},{reffered_user[1]},{reffered_user[2]},{
                       reffered_user[3]},{reffered_user[4]},{reffered_user[5]}\n')
    return "Reffered users exported successfully"


def export_unreffered_users_in_csv_file():
    unreffered_users = get_unreffered_users()
    with open('unreffered_users.csv', 'w') as file:
        for unreffered_user in unreffered_users:
            file.write(f'{unreffered_user[0]},{unreffered_user[1]},{unreffered_user[2]},{
                       unreffered_user[3]},{unreffered_user[4]},{unreffered_user[5]}\n')
    return "Unreffered users exported successfully"
