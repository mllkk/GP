#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import socket
import ssl
import re
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime



# 1) Log klasörü ve handler ayarları
LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)

# 2) Handler: her gece yarısı dönecek, 7 gün yedek tutacak
handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, datetime.now().strftime("%Y-%m-%d") + ".log"),
    when="midnight",      # gece yarısı rotate
    interval=1,           # 1 gün
    backupCount=7,        # son 7 günü sakla
    encoding="utf-8",
    utc=False             # yerel zamana göre döndür
)
handler.suffix = "%Y-%m-%d"  # yedek dosya adlarında tarih formatı

# 3) Formatter ve logger
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger()  # root logger
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def get_http_server_header(host, port, use_ssl=False, timeout=15):
    try:
        logger.info(f"Connecting to {host}:{port} (SSL={use_ssl}, timeout={timeout}s)")
        sock = socket.create_connection((host, port), timeout=timeout)
    except socket.timeout:
        logger.error(f"Connection timed out after {timeout}s")
        return None
    except socket.error as e:
        logger.error(f"Connection error: {e}")
        return None

    if use_ssl:
        logger.info("Wrapping socket with SSL/TLS")
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=host)

    request = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"User-Agent: Tomcat-EOL-Checker/1.0\r\n"
        f"\r\n"
    )
    logger.info("Sending HTTP GET request")
    sock.send(request.encode('ascii'))

    response = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
    except socket.timeout:
        logger.warning("Read timeout; proceeding with received data")
    finally:
        sock.close()

    text = response.decode('iso-8859-1', errors='ignore')
    match = re.search(r"^Server:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    if match:
        server_header = match.group(1).strip()
        logger.info(f"Found Server header: {server_header}")
        return server_header
    else:
        logger.error("Server header not found")
        return None

def parse_tomcat_version(server_header):
    coyote = re.search(r"Apache-Coyote/([\d\.]+)", server_header)
    if coyote:
        return coyote.group(1)
    tomcat = re.search(r"Apache[- ]Tomcat/([\d\.]+)", server_header, re.IGNORECASE)
    if tomcat:
        return tomcat.group(1)
    return None

def is_version_eol(version_str):
    parts = version_str.split('.')
    try:
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
    except ValueError:
        logger.warning(f"Unable to parse version string: {version_str}")
        return False
    eol = (major < 5) or (major == 5 and minor <= 5)
    logger.info(f"Version EOL status: {eol} (major={major}, minor={minor})")
    return eol

def main():
    if len(sys.argv) < 3:
        logger.error(f"Usage: {sys.argv[0]} <host> <port> [--ssl]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    use_ssl = ('--ssl' in sys.argv)

    logger.info(f"Starting check for {host}:{port}")

    server_header = get_http_server_header(host, port, use_ssl)
    if server_header is None:
        logger.critical("Failed to retrieve Server header; exiting.")
        sys.exit(2)

    version = parse_tomcat_version(server_header)
    if not version:
        logger.critical("Could not determine Tomcat version; exiting.")
        sys.exit(3)

    logger.info(f"Detected Tomcat version: {version}")

if __name__ == "__main__":
    main()
