# Author: suenerve
# I demand my credits to the code wherever it's used.
# This code is licensed under a NON-commercial use.
# Open issues at: https://github.com/suenerve/DSV/issues/new
# NOTE : Spamming Discord's API is against TOS, You may get your account suspended and I am not responsible. For a further caution, use an alt's token and a higher delay.

import random
import string 
import requests
import os
import time
import json
import itertools
import threading
import signal
from colorama import Fore,init
import datetime
from configparser import ConfigParser
import sys
init(autoreset=True)
__version__ = "Author: suenerve DSV 1.9"
__github__= "https://github.com/suenerve"
dir_path = os.path.dirname(os.path.realpath(__file__))
configur = ConfigParser()
configur.read(os.path.join(dir_path, f"config.ini"))
tokens_list = os.path.join(dir_path, f"tokens.txt")
integ_0 = 0
unauthorized_tokens = set()
ratelimited_tokens = set()
last_attempt_mode = False
sys_url = "https://discord.com/api/v9/users/@me"
URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"
DEACTIVATE = False

def handler(signal_received, frame):
    global DEACTIVATE
    print('\nSIGINT or CTRL-C detected. Exiting gracefully')
    DEACTIVATE = True

signal.signal(signal.SIGINT, handler)

class Checker:
    def __init__(self):
        self.session = requests.Session()

    def check(self, name):
        global available_usernames, integ_0, DEACTIVATE, last_attempt_mode
        if DEACTIVATE:
            return
        body = {"username": name}
        while not DEACTIVATE:
            time.sleep(Delay)
            proxy = get_request_proxy()
            try:
                endpoint = self.session.post(get_request_url(), headers=s_sys_h(), json=body, timeout=10, **get_request_kwargs(proxy))
                json_endpoint = endpoint.json()
                if endpoint.status_code == 401 and sat_multi_token == True:
                    if integ_0 not in unauthorized_tokens:
                        unauthorized_tokens.add(integ_0)
                        print(f"{Lb}[!]{Fore.RED} Token {integ_0} got unauthorized.")
                        mark_token_unauthorized(integ_0)
                    with lock:
                        integ_0 = (integ_0 +1) % len(avail_tokens(tokens_list))
                    username_info, discriminator_info = get_user_info()
                    print(f"{Lb}[!]{Ly} Rotating to token index: {integ_0} connected as: {username_info}#{discriminator_info}")
                    continue
                if endpoint.status_code == 429:
                    if sat_multi_token == True:
                        current_token_idx = integ_0
                        ratelimited_tokens.add(current_token_idx)
                        if len(ratelimited_tokens) == len(avail_tokens(tokens_list)):
                            if not last_attempt_mode:
                                print(f"{Lb}[!]{Fore.RED} All tokens rate limited. Checking one last time before going to sleep...")
                                last_attempt_mode = True
                                ratelimited_tokens.clear()
                            else:
                                print(f"{Lb}[!]{Fore.RED} All tokens exhausted. Sleeping for 3600s (1 hour)...")
                                time.sleep(3600)
                                ratelimited_tokens.clear()
                                last_attempt_mode = False
                                print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} Woke up! Resuming...")
                        with lock:
                            integ_0 = (integ_0 +1) % len(avail_tokens(tokens_list))
                        username_info, discriminator_info = get_user_info()
                        print(f"{Lb}[!]{Fore.YELLOW} Rate limited. Rotating to token index: {integ_0} connected as: {username_info}#{discriminator_info}")
                    else:
                        print(f"{Lb}[!]{Fore.YELLOW} Rate limited. Waiting {Delay}s before retrying...")
                        time.sleep(Delay)
                    continue
                break
            except requests.exceptions.RequestException as e:
                if configur.getboolean("sys","PROXY_MODE"):
                    print(f"{Lb}[!]{Fore.YELLOW} Proxy connection error ({e}), switching proxy...")
                    continue
                else:
                    print(f"{Lb}[?]{Fore.RED} Request error: {e} | Skipping '{name}'")
                    return
        if DEACTIVATE:
            return
        if json_endpoint.get("taken") is not None:
            if json_endpoint["taken"] is False:
                print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} '{name}' available.")
                ch_send_webhook(name)
                save(name)
                with lock:
                    available_usernames.append(name)
            elif json_endpoint["taken"] is True:
                print(f"{Lb}[-]{Fore.RED} '{name}' taken.")
                save_unavailable(name)
        else:
            msg = endpoint.json().get('message', 'Unknown error')
            if 'verify' in msg.lower() and sat_multi_token == True:
                if integ_0 not in unauthorized_tokens:
                    unauthorized_tokens.add(integ_0)
                    print(f"{Lb}[!]{Fore.RED} Token {integ_0} got unverified (needs phone verification).")
                    mark_token_unauthorized(integ_0)
                with lock:
                    integ_0 = (integ_0 +1) % len(avail_tokens(tokens_list))
                username_info, discriminator_info = get_user_info()
                print(f"{Lb}[!]{Ly} Rotating to token index: {integ_0} connected as: {username_info}#{discriminator_info}")
                checker.check(name)
                return
            print(f"{Lb}[?]{Fore.RED} Error validating '{name}': {msg} |DSV: Make sure you have a valid token or proxy.")

checker = Checker()
def s_sys_h():
   try:
      if configur.getboolean("sys","PROXY_MODE"):
         return {
            "Content-Type": "Application/json",
            "Orgin": "https://discord.com/"
         }
   except Exception:
      pass
   if configur.getboolean("sys","MULTI_TOKEN") == True:
      return {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",
    "Authorization":avail_tokens(tokens_list)[integ_0]
    }
   elif configur.getboolean("sys","MULTI_TOKEN") == False:
      return{
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",
    "Authorization":configur.get("sys","TOKEN")
    }
   else:
      return {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",
    "Authorization":configur.get("sys","TOKEN")
    }

def sys_c_t():
   try:
      if configur.getboolean("sys","PROXY_MODE"):
         if not proxies:
            print(f"{Lb}[!]{Fore.RED} Proxy mode enabled but no proxies were loaded.")
            exit()
         return
   except Exception:
      pass
   if configur.get("sys","TOKEN") != "":
      pass
   elif configur.get("sys","TOKEN") == "" and configur.getboolean("sys","MULTI_TOKEN") == False:
        print(f"{Lb}[!]{Fore.RED} No token found. You must paste your token inside the 'config.ini' file, in front of the value 'TOKEN'.")
        exit()
   elif configur.getboolean("sys","MULTI_TOKEN") == True and not avail_tokens(tokens_list)[0]:
       print(f"{Lb}[!]{Fore.RED} No tokens found. You must paste your tokens inside the 'tokens.txt' file.")
       exit()
   elif configur.getboolean("sys","MULTI_TOKEN") is not True and configur.getboolean("sys","MULTI_TOKEN") is not False and configur.get("sys","TOKEN") == "":
       print(f"{Lb}[!]{Fore.RED} Invalid config detected. Please re-check the config file, `config.ini` and your settings.")
       exit()

available_usernames = []
av_list = os.path.join(dir_path, f"available_usernames.txt")
unav_list = os.path.join(dir_path, f"unavailable_usernames.txt")
checked_list = os.path.join(dir_path, f"checked_usernames.txt")
sample_0 = r"_."
Lb = Fore.LIGHTBLACK_EX
Ly = Fore.LIGHTYELLOW_EX
Delay = configur.getfloat("config","default_delay")
proxy_mode = False
checked_usernames = set()
proxies = []
proxy_cycle = None
proxy_list_path = os.path.join(dir_path, "proxies.txt")
lock = threading.Lock()

def setconf():
   global string_0
   global digits_0
   global punctuation_0
   global webhook_0
   global sat_string
   global sat_digits
   global sat_multi_token
   global sat_punct
   global sat_webhook
   global proxy_mode
   global sat_proxy_mode
   global proxy_list_path
   global proxy_cycle
   global proxies
   sat_webhook = configur.get("sys","WEBHOOK_URL")
   sat_string = configur.getboolean("config","string")
   sat_digits = configur.getboolean("config","digits")
   sat_punct = configur.getboolean("config","punctuation")
   sat_multi_token = configur.getboolean("sys","MULTI_TOKEN")
   try:
      proxy_mode = configur.getboolean("sys","PROXY_MODE")
   except Exception:
      proxy_mode = False
   sat_proxy_mode = proxy_mode
   proxy_file = configur.get("sys","PROXY_FILE", fallback="proxies.txt")
   proxy_list_path = os.path.join(dir_path, proxy_file)
   if proxy_mode:
      proxies = load_proxies(proxy_list_path)
      if not proxies:
         print(f"{Lb}[!]{Fore.RED} Error: No proxies were loaded from {proxy_list_path}")
         exit()
      proxy_cycle = itertools.cycle(proxies)
   if sat_webhook =="":
      webhook_0 = False
   elif sat_webhook !="":
      webhook_0 = True
   if sat_string == True:
      string_0 = string.ascii_lowercase
   elif sat_string == False:
      string_0 = ""
   else:
      string_0 = string.ascii_lowercase
      sat_string = True
   if sat_digits == True:
      digits_0 = string.digits
   elif sat_digits == False:
      digits_0 = ""
   else:
      digits_0 = string.digits
      sat_digits = True
   if sat_punct == True:
      punctuation_0 = sample_0
   elif sat_punct == False:
      punctuation_0 = ""
   else:
      punctuation_0 = sample_0
      sat_punct = True
   if sat_punct == False and sat_digits == False and sat_string == False:
      punctuation_0 = sample_0
      digits_0 = string.digits
      string_0 = string.ascii_lowercase

def get_user_info():
    """Safely get user information with error handling"""
    try:
        if configur.getboolean("sys","PROXY_MODE"):
            return 'PROXY', 'MODE'
    except Exception:
        pass
    try:
        response = requests.get(sys_url, headers=s_sys_h())
        user_data = response.json()
        username = user_data.get('username', 'UNKNOWN_USER')
        discriminator = user_data.get('discriminator', '0000')
        return username, discriminator
    except Exception:
        return 'ERROR', '0000'


def get_request_url():
    try:
        if configur.getboolean("sys","PROXY_MODE"):
            return "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
    except Exception:
        pass
    return URL


def load_proxies(path):
    with open(path, 'r', encoding='utf-8') as pf:
        return [line.strip() for line in pf if line.strip()]


def get_request_proxy():
    try:
        if not configur.getboolean("sys","PROXY_MODE"):
            return None
    except Exception:
        return None
    if not proxies or proxy_cycle is None:
        return None
    proxy = next(proxy_cycle)
    if proxy is not None:
        proxy_str = str(proxy).strip()
        if proxy_str.lower().startswith(('http://', 'https://', 'socks4://', 'socks5://')):
            if '@' in proxy_str:
                return proxy_str
            else:
                # Try to parse if it's ip:port:user:pass after http://
                parts = proxy_str.split('://', 1)[1].split(':')
                if len(parts) == 4:
                    ip, port, user, passwd = parts
                    return f"http://{user}:{passwd}@{ip}:{port}"
                else:
                    return proxy_str
        else:
            # Plain ip:port or ip:port:user:pass
            parts = proxy_str.split(':')
            if len(parts) == 4:
                ip, port, user, passwd = parts
                return f"http://{user}:{passwd}@{ip}:{port}"
            elif len(parts) == 2:
                return f"http://{proxy_str}"
            else:
                return f"http://{proxy_str}"
    return proxy


def get_request_kwargs(proxy):
    if proxy:
        return {"proxies": {"http": proxy, "https": proxy}}
    return {}


def main():
    setconf()
    sys_c_t()
    ask_continue_progress()
    # Safely get user info for title and display
    username, discriminator = get_user_info()
    os.system(f"title {__version__} - Connected as {username}#{discriminator}")
    
    print(f"""{Fore.LIGHTYELLOW_EX}
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
  {Fore.LIGHTCYAN_EX}Connected as {username}{Ly}#{Fore.LIGHTCYAN_EX}{discriminator}{Fore.LIGHTYELLOW_EX}
                            
  {Fore.LIGHTYELLOW_EX}░██░████     ░██████      ░██    ░██           {Fore.LIGHTCYAN_EX}1-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Generate random users(menu){Fore.LIGHTBLACK_EX}]{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}░███              ░██     ░██    ░██           {Fore.LIGHTCYAN_EX}2-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Check a specific list{Fore.LIGHTBLACK_EX}]{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}░██          ░███████     ░██    ░██           {Fore.LIGHTCYAN_EX}3-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Generate letters only{Fore.LIGHTBLACK_EX}]{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}░██         ░██   ░██     ░██   ░███           {Fore.LIGHTCYAN_EX}4-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Generate semi 3c/l{Fore.LIGHTBLACK_EX}]{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}░██          ░█████░██     ░█████░██            {Fore.LIGHTCYAN_EX}Config.ini:{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}░██                              ░██            {Fore.LIGHTCYAN_EX}Digits: {Fore.YELLOW}{sat_digits}{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}░███████                    ░███████            {Fore.LIGHTCYAN_EX}String: {Fore.YELLOW}{sat_string}{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}                                                {Fore.LIGHTCYAN_EX}Punctuation: {Fore.YELLOW}{sat_punct}{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}                                                {Fore.LIGHTCYAN_EX}Multi-Token: {Fore.YELLOW}{sat_multi_token}{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}                                                {Fore.LIGHTCYAN_EX}Proxy Mode: {Fore.YELLOW}{sat_proxy_mode}{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}                                                {Fore.LIGHTCYAN_EX}Webhook: {Fore.YELLOW}{webhook_0}{Fore.LIGHTYELLOW_EX}
  {Fore.LIGHTYELLOW_EX}                                                {Fore.LIGHTCYAN_EX}Delay: {Fore.YELLOW}{Delay}{Fore.LIGHTYELLOW_EX}

  {Fore.LIGHTYELLOW_EX}Discord Username's availability validator.
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
""")
    proc0()
    
def setdelay():
   global Delay
   print(f"{Lb}[!]{Ly} Default delay is: {Delay}s (config.ini){Lb}")
   d_input = input(f"{Lb}[{Ly}Edit Delay (Press Enter to skip){Lb}]:> ")
   if d_input=="" or d_input.isspace():
      return
   else:   
    try:
      int(d_input)
      Delay = int(d_input)
    except ValueError:
      print(f"{Lb}[!]{Fore.RED}Error: You must enter a valid integer. No strings.")
      setdelay()

def proc0():
    m_input = input(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}RAY{Fore.LIGHTBLACK_EX}]:> {Fore.LIGHTYELLOW_EX}").lower()
    if m_input=="exit":
        sys.exit(0)
    if m_input=="":
        proc0()
    elif m_input=="2":
        setdelay()
        opt2load()
    elif m_input=="1":
       setdelay()
       opt1load()
    elif m_input=="3":
       setdelay()
       opt3load()
    elif m_input=="4":
       setdelay()
       opt4load()
    else:
        proc0()

def validate_names(opt,usernames):
   # All options should validate usernames with the same request path.
   if isinstance(usernames, list):
       for username in usernames:
           if DEACTIVATE:
               break
           checker.check(username)
   else:
       checker.check(usernames)

def avail_tokens(path):
   with open(path, 'r') as at:
        tokens = at.read().splitlines()
   return [t.split()[0] for t in tokens if t.strip()]

def mark_token_unauthorized(token_index):
   try:
       with open(tokens_list, 'r') as f:
           lines = f.readlines()
       if token_index < len(lines):
           line = lines[token_index].strip()
           if 'unauthorized' not in line.lower():
               lines[token_index] = line + ' unauthorized\n'
           with open(tokens_list, 'w') as f:
               f.writelines(lines)
   except Exception as e:
       print(f"{Lb}[!]{Fore.RED} Error marking token unauthorized: {e}")

def exit():
   input(f"{Fore.YELLOW}Press Enter to exit.")
   sys.exit(0)

def checkavail(): 
   if len(available_usernames) < 1:
      print(f"{Lb}[!]{Fore.RED} Error: No available usernames found.")
      exit()
   else:
      return

def opt2load():
    global av_list
    global dir_path
    list_path = os.path.join(dir_path, f"usernames.txt")
    print(f"{Lb}[!]{Ly}Checking 'usernames.txt' for a valid list...")
    try:
     with open(list_path) as file:
      usernames = [line.strip() for line in file if line.strip() not in checked_usernames]
     if len(checked_usernames) > 0:
      print(f"{Lb}[!]{Ly}Skipping {len(checked_usernames)} already checked usernames.")
     validate_names(2,usernames)
     checkavail()
     print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
     exit()
    except FileNotFoundError:
       print(f"{Lb}[!]{Fore.RED} Error: Couldn't find the list (usernames.txt). Please make sure to create a valid list file in the same directory: \n({dir_path}\\)")
       exit()

def opt1load():
   opt1_input:int = input(f"{Lb}[{Ly}How many letters in a username{Lb}]:> ")
   try:
    int(opt1_input)
    if int(opt1_input) >32 or int(opt1_input) <2:
       print(f"{Lb}[!]{Fore.RED} Error: The username must contain at least 2 letters, and not more than 32 letters.")
       opt1load()
    opt2_input:int = input(f"{Lb}[{Ly}How many usernames to generate{Lb}]:> ")
    opt1func(int(opt2_input),int(opt1_input))
   except ValueError:
      print(f"{Lb}[!]{Fore.RED} Error: You must enter a valid integer. No strings.")
      opt1load()

def opt3load():
   opt1_input:int = input(f"{Lb}[{Ly}How many letters in a username{Lb}]:> ")
   try:
    int(opt1_input)
    if int(opt1_input) >32 or int(opt1_input) <2:
       print(f"{Lb}[!]{Fore.RED} Error: The username must contain at least 2 letters, and not more than 32 letters.")
       opt3load()
    opt2_input:int = input(f"{Lb}[{Ly}How many usernames to generate{Lb}]:> ")
    opt3func(int(opt2_input),int(opt1_input))
   except ValueError:
      print(f"{Lb}[!]{Fore.RED} Error: You must enter a valid integer. No strings.")
      opt3load()

def opt4load():
   opt1_input:int = input(f"{Lb}[{Ly}How many characters in a username (including dot/underscore){Lb}]:> ")
   try:
    int(opt1_input)
    if int(opt1_input) >32 or int(opt1_input) <2:
       print(f"{Lb}[!]{Fore.RED} Error: The username must contain at least 2 characters, and not more than 32 characters.")
       opt4load()
    opt2_input:int = input(f"{Lb}[{Ly}How many usernames to generate{Lb}]:> ")
    opt4func(int(opt2_input),int(opt1_input))
   except ValueError:
      print(f"{Lb}[!]{Fore.RED} Error: You must enter a valid integer. No strings.")
      opt4load()

def load_checked_usernames():
   global checked_usernames
   try:
       if os.path.exists(checked_list):
           with open(checked_list, 'r') as f:
               checked_usernames = set(line.strip() for line in f if line.strip())
   except Exception:
       pass

def ask_continue_progress():
   global checked_usernames
   if os.path.exists(checked_list) and os.path.getsize(checked_list) > 0:
       resp = input(f"{Lb}[?]{Ly} Continue from previous progress? (y/n): ").lower().strip()
       if resp == 'y' or resp == 'yes':
           load_checked_usernames()
           print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} Loaded {len(checked_usernames)} previously checked usernames.")
       elif resp == 'n' or resp == 'no':
           try:
               os.remove(av_list)
               os.remove(unav_list)
               os.remove(checked_list)
               checked_usernames.clear()
               print(f"{Lb}[!]{Ly} Cleared previous progress. Starting fresh.")
           except Exception:
               pass
   else:
       load_checked_usernames()

def save(content:string):
   with open(av_list, "a") as file:
        file.write(f"\n{content}")
   with open(checked_list, "a") as file:
        file.write(f"\n{content}")
   checked_usernames.add(content)

def save_unavailable(content:string):
   with open(unav_list, "a") as file:
        file.write(f"\n{content}")
   with open(checked_list, "a") as file:
        file.write(f"\n{content}")
   checked_usernames.add(content)

def ch_send_webhook(val0:str):
   if webhook_0 == True:
    webhook = Discord(url=sat_webhook)
    try:
     webhook.post(
       username="Ray",
       avatar_url="https://files.catbox.moe/3agiqv.webp",
       embeds=[
    {
      "title": f"Username: `{val0}` is available :white_check_mark:.",
      "timestamp": str(datetime.datetime.now(datetime.timezone.utc)),
      "footer": {
        "text": "Discord multi token username checker"
      },
      "author": {
        "name": "Ray - Username Found",
        "url": "",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/5290/5290982.png"
      },
      "thumbnail": {
        "url": ""
      },
      "fields": [],
      "color": 16777215
    }
  ],
    )
    except Exception as s:
       print(f"{Lb}[!]{Fore.RED} Error: Something went wrong while sending the webhook request. Exception: {s} | DSV: Make sure you have a valid webhook URL")
   else:
      return

def opt1func(v1,v2):
   generated = 0
   attempts = 0
   max_attempts = v1 * 10
   while generated < v1 and attempts < max_attempts:
    name = get_names(int(v2))
    if name not in checked_usernames:
      validate_names(1,name)
      generated += 1
    attempts += 1
   checkavail()
   print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
   exit()

def opt3func(v1,v2):
   generated = 0
   attempts = 0
   max_attempts = v1 * 10
   while generated < v1 and attempts < max_attempts:
    name = get_names_letters_only(int(v2))
    if name not in checked_usernames:
      validate_names(1,name)
      generated += 1
    attempts += 1
   checkavail()
   print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
   exit()

def opt4func(v1,v2):
   generated = 0
   attempts = 0
   max_attempts = v1 * 10
   while generated < v1 and attempts < max_attempts:
    name = get_names_with_dots(int(v2))
    if name not in checked_usernames:
      validate_names(1,name)
      generated += 1
    attempts += 1
   checkavail()
   print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
   exit()

def get_names(length: int) ->str:
   return ''.join(random.sample(string_0 + digits_0 + punctuation_0, length))

def get_names_letters_only(length: int) ->str:
   return ''.join(random.sample(string.ascii_lowercase, length))

def get_names_with_dots(length: int) ->str:
   chars = string.ascii_lowercase + string.digits
   base_name = list(random.choices(chars, k=length))
   # Randomly choose underscore or dot
   choice = random.choice(['underscore', 'dot'])
   # Replace one random position with the special char
   pos = random.randint(0, length-1)
   special = '_' if choice == 'underscore' else '.'
   base_name[pos] = special
   return ''.join(base_name)

# Source of this class: https://github.com/10mohi6/discord-webhook-python/blob/master/discordwebhook/discordwebhook.py
class Discord:
    def __init__(self, *, url):
        self.url = url
    def post(
        self,
        *,
        content=None,
        username=None,
        avatar_url=None,
        tts=False,
        file=None,
        embeds=None,
        allowed_mentions=None
    ):
        if content is None and file is None and embeds is None:
            raise ValueError("required one of content, file, embeds")
        data = {}
        if content is not None:
            data["content"] = content
        if username is not None:
            data["username"] = username
        if avatar_url is not None:
            data["avatar_url"] = avatar_url
        data["tts"] = tts
        if embeds is not None:
            data["embeds"] = embeds
        if allowed_mentions is not None:
            data["allowed_mentions"] = allowed_mentions
        if file is not None:
            return requests.post(
                self.url, {"payload_json": json.dumps(data)}, files=file
            )
        else:
            return requests.post(
                self.url, json.dumps(data), headers={"Content-Type": "application/json"}
            )

if __name__ == "__main__":
    main()
    