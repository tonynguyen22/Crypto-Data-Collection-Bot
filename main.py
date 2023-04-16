import os
import telebot
from telebot import types 
import requests 
import text
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tabulate import tabulate
from numerize import numerize

#Start the bot
API_KEY = '5656374342:AAGEr_eZpxND_kwnDPpB3EcX2vEtst4sdS4'
bot = telebot.TeleBot(API_KEY)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
  
def get_data(symbol):
  url = "https://api.coingecko.com/api/v3/coins/"+symbol.lower()+"/ohlc?vs_currency=usd&days=max"
  res = requests.get(url) 
  return_data = []
  for each in res.json():
    return_data.append(float(each[4]))
  return np.array(return_data)
  
def button_gen(buttons):
  markup = types.ReplyKeyboardMarkup(row_width=5)
  for x in buttons:
      markup.add(types.KeyboardButton(x)) 
  return markup

#/start command
@bot.message_handler(commands=['start'])
def start(message): 
  message = bot.send_message(message.chat.id, text.choose_option_msg) 

#/basicinfo
@bot.message_handler(commands=['basicinfo'])
def basicinfo(message):
  markup = types.ReplyKeyboardRemove(selective=False)
  message = bot.send_message(message.chat.id, text.enter_coin_msg,reply_markup=markup)
  bot.register_next_step_handler(message,basicinfoHelper)
def basicinfoHelper(message):
  try:
    result = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+message.text.lower()+"&order=market_cap_desc").json()[0]
    dict = {
    'Symbol Test': result.get('symbol'),
    'Name': result.get('name'),
    'Current Price': result.get('current_price'),
    'Price change 24h': round(float(result.get('price_change_24h')),2),
    'Price change 24h (%)': round(float(result.get('price_change_percentage_24h')),2),
    'Volume': numerize.numerize(int(result.get('total_volume')))
    }
    df = pd.DataFrame.from_dict(dict,orient ='index')
    table = tabulate(df, tablefmt ="double_grid")
    message = bot.send_message(message.chat.id, f'<pre>{table}</pre>', parse_mode="HTML")
    message = bot.send_message(message.chat.id, text.choose_nextoption_msg) 
  except Exception as e:
    print(e)
    message = bot.send_message(message.chat.id,text.invalid_symbol_msg)
    bot.register_next_step_handler(message,basicinfoHelper)

#/marketcap
@bot.message_handler(commands=['marketcap'])
def marketcap(message):
  markup = types.ReplyKeyboardRemove(selective=False)
  message = bot.send_message(message.chat.id, text.enter_coin_msg,reply_markup=markup)
  bot.register_next_step_handler(message,marketcapHelper)
def marketcapHelper(message):
  try:
    result = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+message.text.lower()+"&order=market_cap_desc").json()[0]
    dict = {
    'Market Cap': numerize.numerize(int(result.get('market_cap'))),
    'Market Cap Rank': result.get('market_cap_rank'),
    'Market Cap Change 24h': numerize.numerize(float(result.get('market_cap_change_24h'))),
    'Market Cap Change 24h (%)': round(float(result.get('market_cap_change_percentage_24h')),2)  
    }
    df = pd.DataFrame.from_dict(dict,orient ='index')
    table = tabulate(df, tablefmt ="double_grid")
    message = bot.send_message(message.chat.id, f'<pre>{table}</pre>', parse_mode="HTML")
    message = bot.send_message(message.chat.id, text.choose_nextoption_msg) 
  except Exception as e:
    print(e)
    message = bot.send_message(message.chat.id,text.invalid_symbol_msg)
    bot.register_next_step_handler(message,marketcap)

#/highlow
@bot.message_handler(commands=['highlow'])
def highlow(message):
  markup = types.ReplyKeyboardRemove(selective=False)
  message = bot.send_message(message.chat.id, text.enter_coin_msg,reply_markup=markup)
  bot.register_next_step_handler(message,highlowHelper)
def highlowHelper(message):
  try:
    result = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+message.text.lower()+"&order=market_cap_desc").json()[0]
    dict = {
    'High 24h': str(result.get('high_24h')),
    'Low 24h': str(result.get('low_24h')) 
    }
    df = pd.DataFrame.from_dict(dict,orient ='index')
    table = tabulate(df, tablefmt ="double_grid")
    message = bot.send_message(message.chat.id, f'<pre>{table}</pre>', parse_mode="HTML")
    message = bot.send_message(message.chat.id, text.choose_nextoption_msg) 
  except Exception as e:
    print(e)
    message = bot.send_message(message.chat.id,text.invalid_symbol_msg)
    bot.register_next_step_handler(message,marketcap)

#/athatl
@bot.message_handler(commands=['athatl'])
def athatl(message):
  markup = types.ReplyKeyboardRemove(selective=False)
  message = bot.send_message(message.chat.id, text.enter_coin_msg,reply_markup=markup)
  bot.register_next_step_handler(message,athatlHelper)
def athatlHelper(message):
  try:
    result = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+message.text.lower()+"&order=market_cap_desc").json()[0]
    dict = {
    'All-time high': round(int(result.get('ath')),2),
    'Change since ATH (%)': round(float(result.get('ath_change_percentage')),2),
    'All-time low': round(int(result.get('atl')),2),
    'Change since ATL (%)': round(float(result.get('atl_change_percentage')),2)  
    }
    df = pd.DataFrame.from_dict(dict,orient ='index')
    table = tabulate(df, tablefmt ="double_grid")
    message = bot.send_message(message.chat.id, f'<pre>{table}</pre>', parse_mode="HTML")
    message = bot.send_message(message.chat.id, text.choose_nextoption_msg) 
  except Exception as e:
    print(e)
    message = bot.send_message(message.chat.id,text.invalid_symbol_msg)
    bot.register_next_step_handler(message,athatl)

#/chart
@bot.message_handler(commands=['chart'])
def chart(message):
  markup = types.ReplyKeyboardRemove(selective=False)
  message = bot.send_message(message.chat.id, text.enter_coin_msg,reply_markup=markup)
  bot.register_next_step_handler(message,chartHelper)
def chartHelper(message):
  try:
    plt.plot(get_data(message.text.lower()))
    plt.ylabel("Price") 
    plt.xticks([])
    plt.title("Crypto Chart")
    plt.savefig('chart.png')
    photo = open('chart.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    plt.clf()
    message = bot.send_message(message.chat.id, text.choose_nextoption_msg) 
  except Exception as e:
    print(e)
    message = bot.send_message(message.chat.id,text.invalid_symbol_msg)
    bot.register_next_step_handler(message,chart)
    
#/list
#@bot.message_handler(commands=['list'])
#def list(message):
#  result = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false").json()[0]
  
bot.infinity_polling()
