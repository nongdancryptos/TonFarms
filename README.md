### [TON FARMS]

 Đăng ký tại đây: [[TON FARMS]](https://t.me/tonsfarm_bot?start=r_JVFV1876)
 
 Nhập mã mời nhận thêm point: 
 ```bash
JVFV1876
```
### TonFarms Automation Tool
## Chức năng:
1. **Đăng nhập**: Chương trình sẽ đăng nhập vào từng tài khoản và lưu trữ token vào `tokens.json`.
2. **Check-in**: Nếu tài khoản chưa check-in hôm nay, chương trình sẽ thực hiện check-in để nhận năng lượng.
3. **Tham gia clan**: Nếu tài khoản chưa tham gia clan, chương trình sẽ thực hiện tham gia.
4. **Thực hiện nhiệm vụ (tasks)**: Chương trình sẽ lấy danh sách nhiệm vụ và xác minh chúng.
5. **Chơi game**: Nếu tài khoản có đủ năng lượng, chương trình sẽ thực hiện chơi game và nhận thưởng.

## 1. Cấu Trúc Thư Mục

Đảm bảo rằng bạn có cấu trúc thư mục như sau:

```bash
TonFarms/
├── tonfarms.py
├── utils/
│   ├── __init__.py
│   └── banner.py
├── data.txt
├── proxy.txt
├── tokens.json
└── requirements.txt
```

- **tonfarms.py**: Tệp chính chứa mã nguồn Python.
- **utils/**: Thư mục chứa các tệp tiện ích.
  - **init.py**: Tệp rỗng để biến thư mục thành một package Python.
  - **banner.py**: Tệp chứa hàm hiển thị banner với màu sắc.
- **data.txt**: Tệp chứa danh sách truy vấn hoặc thông tin tài khoản.
- **proxy.txt**: Tệp chứa danh sách proxy (nếu sử dụng).
- **tokens.json**: Tệp lưu trữ token đã được đăng nhập.
- **requirements.txt**: Tệp liệt kê các thư viện cần thiết.

## 2. Yêu Cầu Hệ Thống

- Python 3.6 trở lên
- pip (trình quản lý gói của Python)

## 3. Cài Đặt Thư Viện Cần Thiết

Để cài đặt các thư viện cần thiết, bạn cần sử dụng pip và tệp `requirements.txt`. Dưới đây là các bước chi tiết:

1. Mở Command Prompt (Windows) hoặc Terminal (macOS/Linux).
2. Điều hướng đến thư mục dự án TonFarms/.
**Ví dụ:**
   ```bash
   cd D:\Node\TELEGRAM\TonFarms
   ```
3. Tạo và kích hoạt môi trường ảo (tùy chọn nhưng khuyến nghị):

   - Trên Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - Trên macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. Cài đặt các thư viện cần thiết:

   ```bash
   pip install -r requirements.txt
   ```

## 4. Chuẩn Bị Tệp Dữ Liệu

### data.txt:

Tệp này chứa query id. Mỗi dòng trong tệp này đại diện cho một tài khoản.

**Ví dụ:**

```
user1_data_here
```

### proxy.txt (Nếu sử dụng):

Tệp này chứa danh sách proxy. Mỗi dòng chứa một proxy.

**Ví dụ:**

```
http://user:pass@ip:port
```

### tokens.json:

Tệp này sẽ được tạo tự động sau khi bạn chạy chương trình lần đầu tiên để lưu trữ token đã đăng nhập. Bạn không cần tạo thủ công.

## 5. Chạy Chương Trình

Sau khi đã cài đặt thư viện và chuẩn bị các tệp dữ liệu, bạn có thể chạy chương trình `tonfarms.py` bằng các bước sau:

1. Mở Command Prompt (Windows) hoặc Terminal (macOS/Linux).
2. Điều hướng đến thư mục TonFarms/.
**Ví dụ:**
   ```bash
   cd D:\Node\TELEGRAM\TonFarms
   ```

3. Chạy chương trình:

   ```bash
   python tonfarms.py
   ```

## 6. Hướng Dẫn Sử Dụng

Khi bạn chạy chương trình, một banner sẽ hiển thị cùng với menu lựa chọn chế độ chạy chương trình:

### Chọn chế độ chạy:
- **Chạy mà không sử dụng proxy**: Chương trình sẽ xử lý các tài khoản mà không sử dụng proxy.
- **Chạy với proxy cho mỗi tài khoản**: Chương trình sẽ sử dụng proxy riêng cho mỗi tài khoản (nếu có sẵn).
- 
- ## Donations
If you would like to support the development of this project, you can make a donation using the following addresses:

- **Solana**: `3rYhoVL8g28iwjGQq8hKw4bvVmBGhyC8DEbKAwzmy4wn`
- **EVM**: `0x431588aff8ea1becb1d8188d87195aa95678ba0a`
- **BTC**: `bc1pu30mhlegcajqq23ff30vrlnlnsmv0ha6ufwaenv0em4ap8dfzyrqwsvjx5`
- Chúng tôi rất vui được chia sẻ các mã script và tài nguyên mã nguồn miễn phí đến cộng đồng làm airdrop. Nếu bạn thấy các công cụ và tài liệu của chúng tôi hữu ích và muốn ủng hộ chúng tôi tiếp tục phát triển và duy trì các dự án này, bạn có thể đóng góp hỗ trợ qua hình thức donate.
- Mỗi đóng góp của bạn sẽ giúp chúng tôi duy trì chất lượng dịch vụ và tiếp tục cung cấp những tài nguyên giá trị cho cộng đồng làm airdrop. Chúng tôi chân thành cảm ơn sự hỗ trợ và ủng hộ của bạn!
# Cảm ơn bạn 😘😘😘

<div style="display: flex; gap: 20px;">
  <img src="https://raw.githubusercontent.com/nongdancryptos/image/refs/heads/main/qr-momo.jpg" alt="QR Momo" height="340" />
  <img src="https://raw.githubusercontent.com/nongdancryptos/image/refs/heads/main/qr-binance.jpg" alt="QR Binance" height="340" />
</div>

## Contributing

Feel free to open issues or submit pull requests if you have improvements or bug fixes.

# WARNING
⚠️ "User assumes all responsibility and risk associated with the use of this bot/program script."

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
