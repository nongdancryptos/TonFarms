# utils/banner.py

import shutil
from colorama import Fore, Style, init
import re

# Khởi tạo colorama với autoreset để tự động reset màu sau mỗi print
init(autoreset=True)

def strip_ansi_codes(text):
    """
    Hàm loại bỏ các mã màu ANSI khỏi chuỗi.
    """
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def center_text(text, terminal_width):
    """
    Hàm căn giữa một dòng văn bản dựa trên độ rộng terminal.
    """
    stripped_text = strip_ansi_codes(text)
    text_length = len(stripped_text)
    if text_length >= terminal_width:
        return text  # Không căn giữa nếu dòng quá dài
    padding = (terminal_width - text_length) // 2
    return ' ' * padding + text

def show_banner():
    logo = f"""
{Fore.LIGHTBLUE_EX} ██████╗ ███╗   ██╗    ████████╗ ██████╗ ██████╗ 
{Fore.LIGHTBLUE_EX}██╔═══██╗████╗  ██║    ╚══██╔══╝██╔═══██╗██╔══██╗
{Fore.LIGHTBLUE_EX}██║   ██║██╔██╗ ██║       ██║   ██║   ██║██████╔╝
{Fore.LIGHTBLUE_EX}██║   ██║██║╚██╗██║       ██║   ██║   ██║██╔═══╝ 
{Fore.LIGHTBLUE_EX}╚██████╔╝██║ ╚████║       ██║   ╚██████╔╝██║     
{Fore.LIGHTBLUE_EX} ╚═════╝ ╚═╝  ╚═══╝       ╚═╝    ╚═════╝ ╚═╝     
{Style.RESET_ALL}
"""

    header = f"""
{Fore.LIGHTGREEN_EX}
=======================================
=      TonFarms Automation Tool       =
=   -------------------------------   =
=      https://t.me/OnTopAirdrop      =
=======================================
{Style.RESET_ALL}
"""

    # Lấy độ rộng terminal
    terminal_size = shutil.get_terminal_size((80, 20))  # Mặc định 80 nếu không thể lấy
    terminal_width = terminal_size.columns

    # Xử lý từng dòng trong logo và header
    banner_lines = logo.split('\n') + header.split('\n')
    centered_banner = ""

    for line in banner_lines:
        if line.strip() == "":
            centered_banner += "\n"
            continue
        centered_line = center_text(line, terminal_width)
        centered_banner += centered_line + "\n"

    print(centered_banner)
