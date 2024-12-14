# tonfarms.py

import base64
import json
import os
import random
import sys
import time
from urllib.parse import parse_qs, unquote, urlparse
from datetime import datetime, timedelta
import requests
import inquirer  # Import inquirer
from colorama import init, Fore, Style
from utils.banner import show_banner  # Import show_banner từ utils/banner.py

# Khởi tạo colorama
init(autoreset=True)

class TonFarms:
    def __init__(self, proxy=None):
        self.headers = {
            'origin': 'https://game.tonfarms.com',
            'referer': 'https://game.tonfarms.com/',
            'host':'api.tonfarms.com',
            'sec-ch-ua': 'Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129", "Microsoft Edge WebView2";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        self.proxy = proxy
        self.session = requests.Session()
        if self.proxy:
            self.session.proxies = {
                "http": self.proxy,
                "https": self.proxy,
            }

    def log(self, level, message_parts):
        """
        Hàm log với nhiều màu sắc cho từng phần trong dòng log.
        level: Mức độ log ('INFO', 'WARNING', 'ERROR', 'DEBUG', 'SUCCESS', 'FAILURE', 'NOTICE')
        message_parts: Danh sách các tuple (màu, text)
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level_color = {
            'INFO': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'DEBUG': Fore.CYAN,
            'SUCCESS': Fore.LIGHTGREEN_EX,
            'FAILURE': Fore.LIGHTRED_EX,
            'NOTICE': Fore.MAGENTA
        }.get(level, Fore.WHITE)
        
        # Tạo chuỗi log với nhiều màu sắc
        log_message = ' | '.join([f"{color}{text}{Style.RESET_ALL}" for color, text in message_parts])
        print(f"{level_color}[{now}] [{level}] | {log_message}{Style.RESET_ALL}")

    def make_request(self, method, url, headers=None, json_data=None, data=None, params=None):
        retry_count = 0
        while True:
            try:
                if method.upper() == "GET":
                    response = self.session.get(url, headers=headers, params=params, timeout=10)
                elif method.upper() == "POST":
                    response = self.session.post(url, headers=headers, json=json_data, data=data, params=params, timeout=10)
                elif method.upper() == "PUT":
                    response = self.session.put(url, headers=headers, json=json_data, data=data, timeout=10)
                else:
                    raise ValueError("Invalid HTTP method.")

                if response.status_code >= 500:
                    if retry_count >= 4:
                        self.log('ERROR', [(Fore.RED, f"Server Error {response.status_code}"), (Fore.WHITE, f": {response.text}")])
                        return None
                    retry_count += 1
                    self.log('WARNING', [(Fore.YELLOW, f"Server Error {response.status_code}"), (Fore.WHITE, f". Retrying ({retry_count}/4)...")])
                    time.sleep(2)
                elif response.status_code >= 400:
                    self.log('ERROR', [(Fore.RED, f"Client Error {response.status_code}"), (Fore.WHITE, f": {response.text}")])
                    return None
                else:
                    return response
            except requests.exceptions.RequestException as e:
                if retry_count >= 4:
                    self.log('ERROR', [(Fore.RED, "Request failed after 4 retries"), (Fore.WHITE, f": {e}")])
                    return None
                retry_count += 1
                self.log('WARNING', [(Fore.YELLOW, "Request exception"), (Fore.WHITE, f": {e}. Retrying ({retry_count}/4)...")])
                time.sleep(2)

    def signin(self, payload, token):
        url = 'https://api.tonfarms.com/api/v1/signin'
        headers = {**self.headers}
        
        if token:
            headers['authorization'] = f"Bearer {token}"

        res = self.make_request('POST', url, headers=headers, json_data=payload)
        if res:
            data = res.json()
            if data.get('success'):
                return data
        return None

    def checkin(self, token):
        url = 'https://api.tonfarms.com/api/v1/achievement/checkin'
        headers = {**self.headers, 'authorization': f"Bearer {token}"}
        res = self.make_request('GET', url, headers=headers)
        if res:
            data = res.json()
            if data.get('success'):
                dats = data.get('data')
                day = dats.get('day')
                energy = dats.get('energy')
                star = dats.get('star')
                coin = dats.get('coin')
                ton = dats.get('ton')
                self.log('INFO', [
                    (Fore.CYAN, f"Checkin day {day} Done"),
                    (Fore.BLUE, f", Reward : {energy} Energy | {star} Star | {coin} Coin | {ton} TON")
                ])
                return energy
        return None

    def start_game(self, token):
        url = 'https://api.tonfarms.com/api/v1/game/start'
        headers = {**self.headers, 'authorization': f"Bearer {token}"}
        res = self.make_request('GET', url, headers=headers)
        if res:
            data = res.json()
            if data.get('success'):
                return data.get('data')
        return None

    def claim_game(self, token, payload):
        url = 'https://api.tonfarms.com/api/v1/game/get'
        headers = {**self.headers, 'authorization': f"Bearer {token}"}
        res = self.make_request('POST', url, headers=headers, json_data=payload)
        if res:
            data = res.json()
            if data.get('success'):
                dats = data.get('data')
                amount = dats.get('amount', 0)
                ton = dats.get('ton', 0)
                bonus_level = dats.get('bonus_level', 0)
                bonus_share = dats.get('bonus_share', 0)
                total_coin = dats.get('total_coin', 0)
                total_ton = dats.get('total_ton', 0)
                self.log('INFO', [
                    (Fore.GREEN, f"Play game Done"),
                    (Fore.BLUE, f", Reward : {amount} Point & {ton} TON")
                ])
                self.log('INFO', [
                    (Fore.MAGENTA, f"Bonus Point, Level : {bonus_level} Point | Share : {bonus_share} Point")
                ])
                self.log('INFO', [
                    (Fore.CYAN, f"Total Coin : {total_coin} Point | Total TON : {total_ton} TON")
                ])

    def get_tasks(self, token):
        url = 'https://api.tonfarms.com/api/v1/quest/list'
        headers = {**self.headers, 'authorization': f"Bearer {token}"}
        res = self.make_request('POST', url, headers=headers, json_data={})
        if res:
            data = res.json()
            if data.get('success'):
                dats = data.get('data')
                for item in dats:
                    quest_id = item.get('id', 0)
                    name = item.get('name', '')
                    reward_amount = item.get('reward_amount')
                    is_completed = item.get('is_completed')
                    is_claimed = item.get('is_claimed')
                    if is_claimed:
                        self.log('INFO', [
                            (Fore.GREEN, f"Task {name} Done!!")
                        ])
                    else:
                        payload = {"quest_id": quest_id}
                        time.sleep(3)
                        self.verify_task(token, payload)

    def verify_task(self, token, payload):
        url = 'https://api.tonfarms.com/api/v1/quest/verify'
        headers = {**self.headers, 'authorization': f"Bearer {token}"}
        res = self.make_request('POST', url, headers=headers, json_data=payload)
        if res:
            data = res.json()
            if data.get('success'):
                dats = data.get('data')
                name = dats.get('name')
                reward_amount = dats.get('reward_amount')
                type_ = dats.get('type')
                if type_ == 0:
                    self.log('INFO', [
                        (Fore.CYAN, f"Task {name} Done"),
                        (Fore.BLUE, f", Reward : {reward_amount} Point")
                    ])

    def join_clan(self, token):
        url = 'https://api.tonfarms.com/api/v1/clan/join'
        headers = {**self.headers, 'authorization': f"Bearer {token}"}
        payload = {"clan_id": "dSq68C"}
        res = self.make_request('POST', url, headers=headers, json_data=payload)
        if res:
            data = res.json()
            if data.get('success'):
                self.log('INFO', [
                    (Fore.GREEN, "Join Clan Done")
                ])

def gets(id, tokens):
    return tokens.get(str(id))

def save(id, token, tokens):
    tokens[str(id)] = token
    with open("tokens.json", "w") as f:
        json.dump(tokens, f, indent=4)

def update(id, new_token, tokens):
    if str(id) in tokens:
        tokens[str(id)] = new_token
        with open("tokens.json", "w") as f:
            json.dump(tokens, f, indent=4)
    else:
        return None

def delete_all_tokens():
    with open("tokens.json", "w") as f:
        json.dump({}, f, indent=4)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_queries(filename='data.txt'):
    try:
        with open(filename, 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print(Fore.RED + f"File {filename} not found." + Style.RESET_ALL)
        return []
    except Exception as e:
        print(Fore.RED + f"Failed to load {filename}: {str(e)}" + Style.RESET_ALL)
        return []

def load_proxies(filename='proxy.txt'):
    try:
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except FileNotFoundError:
        print(Fore.RED + f"File {filename} not found." + Style.RESET_ALL)
        return []
    except Exception as e:
        print(Fore.RED + f"Failed to load {filename}: {str(e)}" + Style.RESET_ALL)
        return []

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query.get('user', '{}')))
    parsed_query['user'] = user_data
    return parsed_query

def print_delay(delay):
    print()
    while delay > 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"\r[{now}] | Waiting Time: {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds", end='')
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print(Fore.GREEN + "\nWaiting Done, Starting....\n" + Style.RESET_ALL)

def main():
    # Hiển thị logo từ banner.py
    show_banner()

    # Tạo menu lựa chọn
    questions = [
        inquirer.List(
            'mode',
            message="Chọn chế độ chạy chương trình",
            choices=['Chạy mà không sử dụng proxy', 'Chạy với proxy cho mỗi tài khoản'],
        )
    ]
    answers = inquirer.prompt(questions)

    if not answers:
        print(Fore.RED + "Không nhận được lựa chọn. Thoát chương trình." + Style.RESET_ALL)
        sys.exit(1)

    mode = answers['mode']
    use_proxy = False
    if mode == 'Chạy với proxy cho mỗi tài khoản':
        use_proxy = True

    # Xóa tất cả token trước khi bắt đầu
    delete_all_tokens()
    start_time = time.time()
    delay = 8 * 3600  # 8 giờ
    clear_terminal()
    queries = load_queries()
    proxies = load_proxies()

    if not queries:
        print(Fore.RED + "No queries to process. Exiting..." + Style.RESET_ALL)
        return

    if use_proxy:
        if not proxies:
            print(Fore.RED + "No proxies available. Exiting..." + Style.RESET_ALL)
            return
        if len(proxies) < len(queries):
            print(Fore.YELLOW + "Number of proxies is less than number of accounts. Some accounts sẽ không có proxy." + Style.RESET_ALL)

    tokens = {}
    if os.path.exists("tokens.json"):
        with open("tokens.json", "r") as f:
            tokens = json.load(f)

    sum_queries = len(queries)
    for index, query in enumerate(queries, start=1):
        parsed = parse_query(query)
        user = parsed.get('user', {})
        user_id = user.get('id')
        username = user.get('username', '')
        
        proxy = None
        if use_proxy:
            if index - 1 < len(proxies):
                proxy = proxies[index - 1]
            else:
                proxy = None  # Không có proxy tương ứng
        
        ton_farms = TonFarms(proxy=proxy)

        # Extract chỉ IP từ proxy
        if proxy:
            parsed_proxy = urlparse(proxy)
            proxy_ip = parsed_proxy.hostname if parsed_proxy.hostname else proxy.split(':')[0]
            proxy_info = f" | Proxy: {proxy_ip}"
        else:
            proxy_info = ""

        # Thay thế "SxG" bằng "OnTop"
        ton_farms.log('INFO', [
            (Fore.BLUE, f"OnTop======= Account {index}/{sum_queries}"),
            (Fore.CYAN, f" [ {username} ]"),
            (Fore.MAGENTA, f"{proxy_info} ========OnTop")
        ])
        payload = {
            'avatar': user.get('photo_url'),
            'firstname': user.get('first_name'),
            'lastname': user.get('last_name'),
            'telegram_id': user.get('id'),
            'username': user.get('username')
        }
        token = gets(user_id, tokens)
        data_sign = ton_farms.signin(payload, token)
        if data_sign:
            data = data_sign.get('data', {})
            access_token = data.get('access_token')
            if token is None:
                save(user_id, access_token, tokens)
            else:
                update(user_id, access_token, tokens)
            is_checkin_today = data.get('is_checkin_today', True)
            coin = data.get('coin', 0)
            ton = data.get('ton', 0)
            energy = data.get('energy', 0)
            clan_id = data.get('clan_id', 0)
            level = data.get('level', 0)
            ton_farms.log('INFO', [
                (Fore.GREEN, f"Coin : {coin}"),
                (Fore.BLUE, f" | TON : {ton}"),
                (Fore.CYAN, f" | Energy : {energy}"),
                (Fore.MAGENTA, f" | Level : {level}")
            ])

            if not is_checkin_today:
                energys = ton_farms.checkin(access_token)

            if clan_id == 0:
                ton_farms.join_clan(access_token)

            ton_farms.log('INFO', [
                (Fore.GREEN, "Start Task")
            ])
            ton_farms.get_tasks(access_token)

            if energy > 1:
                ton_farms.log('INFO', [
                    (Fore.GREEN, "Start Game")
                ])
                for i in range(energy - 1):
                    ton_farms.log('INFO', [
                        (Fore.BLUE, f"Playing Game {i + 1}")
                    ])
                    data_start = ton_farms.start_game(access_token)
                    time.sleep(30)
                    if data_start:
                        id_game = data_start.get('id', 0)
                        ton_game = data_start.get('ton', 0)
                        amount = random.randint(120, 150)
                        payload_game = {"amount": amount, "id": id_game, "ton": ton_game}
                        ton_farms.claim_game(access_token, payload_game)
        else:
            ton_farms.log('ERROR', [
                (Fore.RED, f"Signin failed for user {username}.")
            ])

    end_time = time.time()
    total = delay - (end_time - start_time)
    if total > 0:
        print_delay(total)

if __name__ == "__main__":
    main()
