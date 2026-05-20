#!/usr/bin/env python3
"""
Security Test Suite — Prototype 2 (WITHOUT Reverse Proxy Web)
Focused on the security problems that reverse-proxy-web solves:
  1. Secure Channel (TLS/HTTPS) — Confidentiality & Integrity
  2. Rate Limiting for web frontend — Availability
  3. Frontend topology hiding — Confidentiality
  4. Security headers — Multiple attributes
Expected: ALL security protections should be MISSING = vulnerabilities.
"""

import subprocess
import sys
import os
import ssl

try:
	import requests
except ImportError:
	print("Installing requests...")
	subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
	import requests

try:
	import urllib3
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
	pass

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"

PASS = 0
FAIL = 0
VULNS_FOUND = 0

WEB_PAGE_URL = "http://localhost:3000"
API_GATEWAY_URL = "http://localhost:8080"


def passed(msg):
	global PASS
	print(f"{GREEN}✓ PASS:{NC} {msg}")
	PASS += 1

def failed(msg):
	global FAIL
	print(f"{RED}✗ FAIL:{NC} {msg}")
	FAIL += 1

def vuln(msg):
	global VULNS_FOUND
	print(f"{RED}⚠ VULN:{NC} {msg}")
	VULNS_FOUND += 1

def info(msg):
	print(f"{YELLOW}ℹ INFO:{NC} {msg}")

def header(msg):
	print(f"\n{CYAN}{'=' * 70}{NC}")
	print(f"{CYAN}  {msg}{NC}")
	print(f"{CYAN}{'=' * 70}{NC}")


def test_https_availability():
	"""Problem #1 from README: Secure Channel — TLS Termination"""
	header("TEST GROUP 1: HTTPS / TLS Secure Channel (Confidentiality)")
	print("\n  Quality Scenario: Confidentiality & Integrity — Secure Channel")
	print("  Expected: HTTPS should be available with valid TLS configuration")
	print("  (In Prototype 2, there is NO HTTPS = vulnerability)\n")

	# Test HTTPS on port 443
	print("  Testing HTTPS on port 443...")
	try:
		r = requests.get("https://localhost:443/", timeout=5, verify=False)
		print(f"  {YELLOW}HTTPS on 443 returned HTTP {r.status_code}{NC}")
		info("HTTPS appears available but may not be properly configured")
	except requests.ConnectionError:
		vuln("HTTPS on port 443 is NOT available — no TLS termination")
		info("Without HTTPS, all traffic between browser and server is in plain text")
		info("An attacker on the same network (WiFi, ISP) can read credentials, tokens, and content")
	except requests.Timeout:
		vuln("HTTPS on port 443 connection timeout — TLS not reachable")
	except requests.RequestException as e:
		vuln(f"HTTPS on port 443 failed: {e}")

	# Test HTTPS on port 8443 (alternative port)
	print("\n  Testing HTTPS on port 8443...")
	try:
		r = requests.get("https://localhost:8443/", timeout=5, verify=False)
		print(f"  {YELLOW}HTTPS on 8443 returned HTTP {r.status_code}{NC}")
	except requests.ConnectionError:
		vuln("HTTPS on port 8443 is NOT available — no TLS termination for web")
	except requests.RequestException:
		vuln("HTTPS on port 8443 is NOT available")

	# Test if frontend is only served over HTTP
	print(f"\n  Testing if frontend is served over plain HTTP ({WEB_PAGE_URL})...")
	try:
		r = requests.get(WEB_PAGE_URL, timeout=5)
		if r.status_code == 200:
			vuln(f"Frontend served over plain HTTP on port 3000 — no encryption in transit")
			info("Credentials, session tokens, and user data travel in plain text")
			info("Susceptible to: packet sniffing, MITM attacks, session hijacking")
	except requests.ConnectionError:
		info("Frontend not reachable on port 3000 (services may not be running)")

	# Check for HTTP → HTTPS redirect
	print("\n  Testing for HTTP → HTTPS redirect...")
	try:
		r = requests.get("http://localhost:80/", timeout=5, allow_redirects=False)
		if r.status_code in [301, 302] and 'https' in r.headers.get('Location', '').lower():
			info("HTTP redirect to HTTPS exists — but no reverse proxy web to enforce it consistently")
		else:
			vuln("No HTTP → HTTPS redirect — plain HTTP traffic is accepted")
			info("Without redirect, users who type http:// are never upgraded to HTTPS")
	except requests.ConnectionError:
		info("No HTTP listener on port 80 (expected without reverse-proxy-web)")

	# Check HSTS header
	print("\n  Checking for Strict-Transport-Security header...")
	hsts_found = False
	for url in [WEB_PAGE_URL, API_GATEWAY_URL]:
		try:
			r = requests.get(url, timeout=5)
			if 'Strict-Transport-Security' in r.headers:
				hsts_found = True
				break
		except requests.RequestException:
			pass
	if not hsts_found:
		vuln("No Strict-Transport-Security (HSTS) header — browsers won't enforce HTTPS")
		info("Without HSTS, browsers accept HTTP connections and are vulnerable to downgrade attacks")


def test_security_headers():
	"""Problem: Missing security headers that reverse-proxy-web adds"""
	header("TEST GROUP 2: Security Headers (Multiple Quality Attributes)")
	print("\n  Expected: Security headers should be present in ALL responses")
	print("  (In Prototype 2, no security headers are added = vulnerability)\n")

	headers_to_check = {
		"Strict-Transport-Security": {
			"desc": "HSTS — Forces HTTPS for future requests (1 year + subdomains)",
			"attack": "Downgrade attack: attacker forces HTTP to intercept traffic",
			"attribute": "Confidentiality"
		},
		"X-Content-Type-Options": {
			"desc": "nosniff — Prevents browser MIME type sniffing",
			"attack": "MIME sniffing: browser interprets response as executable (XSS vector)",
			"attribute": "Integrity"
		},
		"X-Frame-Options": {
			"desc": "DENY — Prevents page from being embedded in iframes",
			"attack": "Clickjacking: attacker overlays invisible iframe to hijack clicks",
			"attribute": "Integrity"
		},
		"Referrer-Policy": {
			"desc": "no-referrer — Prevents leaking URLs via Referer header",
			"attack": "Information leakage: internal URLs exposed to third-party sites",
			"attribute": "Confidentiality"
		},
	}

	# Check on frontend
	print("  Checking headers on frontend (port 3000)...")
	try:
		r = requests.get(WEB_PAGE_URL, timeout=5)
		for headers, details in headers_to_check.items():
			if headers in r.headers:
				info(f"  {headers}: present ({r.headers[headers]})")
			else:
				vuln(f"Missing {headers} — {details['desc']}")
				info(f"  Attack mitigated: {details['attack']}")
				info(f"  Quality attribute: {details['attribute']}")
	except requests.ConnectionError:
		info("Frontend not reachable (services may not be running)")

	# Check on API Gateway
	print(f"\n  Checking headers on API Gateway ({API_GATEWAY_URL})...")
	try:
		r = requests.get(f"{API_GATEWAY_URL}/health", timeout=5)
		for headers, details in headers_to_check.items():
			if headers in r.headers:
				info(f"  {headers}: present ({r.headers[headers]})")
			else:
				vuln(f"Missing {header} — {details['desc']}")
	except requests.ConnectionError:
		info("API Gateway not reachable")


def test_rate_limiting_web():
	"""Problem: Rate limiting for web frontend"""
	header("TEST GROUP 3: Rate Limiting for Web Frontend (Availability)")
	print("\n  Quality Scenario: Availability — Resist Attack")
	print("  Expected: HTTP 429 after burst threshold on web frontend")
	print("  (In Prototype 2, there is NO rate limiting on port 3000 = vulnerability)\n")

	limited = False
	responses = []

	print(f"  Sending 30 rapid requests to frontend ({WEB_PAGE_URL})...")
	for i in range(30):
		try:
			r = requests.get(WEB_PAGE_URL, timeout=3)
			code = r.status_code
			responses.append(code)
			if code == 429:
				limited = True
				break
		except requests.RequestException:
			break

	if limited:
		info(f"Rate limiting triggered on frontend after {len(responses)} requests")
	else:
		vuln(f"No rate limiting on web frontend — all {len(responses)} requests returned HTTP 200")
		info("Without rate limiting on the frontend, an attacker can:")
		info("  - Exhaust Next.js SSR server resources with rapid page requests")
		info("  - Trigger expensive server-side rendering operations repeatedly")
		info("  - Cause denial of service for legitimate web users")

	# Also test rate limiting on API Gateway for completeness
	print(f"\n  Sending 30 rapid requests to API Gateway ({API_GATEWAY_URL}/health)...")
	limited_api = False
	responses_api = []
	for i in range(30):
		try:
			r = requests.get(f"{API_GATEWAY_URL}/health", timeout=3)
			responses_api.append(r.status_code)
			if r.status_code == 429:
				limited_api = True
				break
		except requests.RequestException:
			break

	if not limited_api:
		vuln(f"No rate limiting on API Gateway — all {len(responses_api)} requests returned HTTP 200")


def test_frontend_direct_access():
	"""Problem: Frontend should only be accessible through reverse proxy"""
	header("TEST GROUP 4: Frontend Direct Access (Confidentiality — Limit Access)")
	print("\n  Expected: Frontend NOT accessible directly on port 3000")
	print("  (In Prototype 2, port 3000 IS accessible = vulnerability)\n")

	try:
		r = requests.get(WEB_PAGE_URL, timeout=5)
		vuln(f"Frontend is DIRECTLY accessible on port 3000 (HTTP {r.status_code})")
		info("Without reverse-proxy-web, the Next.js SSR server is exposed directly")
		info("An attacker can:")
		info("  - Probe the SSR server for vulnerabilities directly")
		info("  - Bypass any WAF or rate limiting that a proxy would provide")
		info("  - Discover server internals via error messages or headers")
	except requests.ConnectionError:
		passed("Frontend port 3000 is not directly accessible")
	except requests.RequestException as e:
		vuln(f"Frontend port 3000 reachable but errored: {e}")


def test_server_info_leakage():
	"""Problem: Server information leakage through headers"""
	header("TEST GROUP 5: Server Information Leakage (Confidentiality)")
	print("\n  Expected: No server/technology version headers exposed")
	print("  (In Prototype 2, Next.js and Node.js headers may be exposed)\n")

	leaky_headers = [
		"Server", "X-Powered-By", "X-AspNet-Version",
		"X-Runtime", "X-Version"
	]

	for url, label in [(WEB_PAGE_URL, "Frontend"), (API_GATEWAY_URL, "API Gateway")]:
		print(f"  Checking {label} headers...")
		try:
			r = requests.get(url, timeout=5)
			for headers in leaky_headers:
				if headers in r.headers:
					vuln(f"{label} exposes {headers}: {r.headers[headers]}")
					info(f"  This reveals technology stack information to attackers")
		except requests.ConnectionError:
			info(f"{label} not reachable")


def test_tls_certificate():
	"""Check TLS certificate properties"""
	header("TEST GROUP 6: TLS Certificate Properties (Confidentiality)")
	print("\n  Expected: Valid TLS certificate with proper configuration")
	print("  (In Prototype 2, there is NO TLS certificate = vulnerability)\n")

	try:
		import socket
		context = ssl.create_default_context()
		context.check_hostname = False
		context.verify_mode = ssl.CERT_NONE

		with socket.create_connection(("localhost", 443), timeout=5) as sock:
			try:
				with context.wrap_socket(sock, server_hostname="localhost") as ssock:
					cert = ssock.getpeercert(binary_form=True)
					vuln("TLS certificate exists on port 443 — but no reverse-proxy-web to manage it properly")
			except ssl.SSLError as e:
				vuln(f"TLS not available on port 443: {e}")
	except (ConnectionRefusedError, OSError):
		vuln("No TLS endpoint available — all web traffic is unencrypted")

	# Test TLS version and cipher on 8443
	try:
		import socket
		with socket.create_connection(("localhost", 8443), timeout=5) as sock:
			context = ssl.create_default_context()
			context.check_hostname = False
			context.verify_mode = ssl.CERT_NONE
			with context.wrap_socket(sock, server_hostname="localhost") as ssock:
				vuln(f"TLS available on 8443: version={ssock.version()}, cipher={ssock.cipher()}")
	except (ConnectionRefusedError, OSError):
		vuln("No TLS endpoint on port 8443 — HTTPS not available for web")
	except ssl.SSLError:
		vuln("TLS handshake failed on port 8443")


def test_oauth_redirect_security():
	"""Check OAuth callbacks use HTTPS"""
	header("TEST GROUP 7: OAuth Redirect Security (Confidentiality)")
	print("\n  Expected: OAuth callbacks should use HTTPS URLs")
	print("  (In Prototype 2, OAuth callbacks use HTTP = vulnerability)\n")

	compose_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docker-compose.yml")
	try:
		with open(compose_path, "r") as f:
			content = f.read()

		oauth_patterns = {
			"GOOGLE_CALLBACK_URL": "Google OAuth callback URL",
			"FRONTEND_OAUTH_REDIRECT_URL": "Frontend OAuth redirect URL",
		}

		for pattern, desc in oauth_patterns.items():
			lines = [l for l in content.splitlines() if pattern in l]
			for line in lines:
				if "http://" in line.lower() and "https://" not in line.lower():
					vuln(f"{desc} ({pattern}) uses HTTP instead of HTTPS")
					info(f"  {line.strip()}")
					info("  OAuth tokens transmitted over HTTP can be intercepted")
				elif "https://" in line.lower():
					info(f"{desc} ({pattern}) uses HTTPS — but no TLS termination point exists")
	except FileNotFoundError:
		failed("docker-compose.yml not found")


def main():
	print()
	print("╔" + "═" * 68 + "╗")
	print("║" + " " * 4 + "SECURITY TEST SUITE — PROTOTYPE 2 (NO REVERSE PROXY WEB)" + " " * 8 + "║")
	print("╚" + "═" * 68 + "╝")
	print(f"  Target: Prototype 2 — Direct service access (no web proxy)")
	print(f"  Focus: TLS / HTTPS, Security Headers, Rate Limiting for Web")
	print(f"  Expected result: Multiple security vulnerabilities found")
	print(f"  Reference: Problems described in Prototype 3's reverse-proxy-web/README.md")
	print()

	test_https_availability()
	test_security_headers()
	test_rate_limiting_web()
	test_frontend_direct_access()
	test_server_info_leakage()
	test_tls_certificate()
	test_oauth_redirect_security()

	print()
	print("=" * 70)
	print(f"  SUMMARY: {PASS} passed, {FAIL} failed, {VULNS_FOUND} vulnerabilities found")
	print("=" * 70)

	if VULNS_FOUND > 0:
		print()
		print(f"{RED}  ⚠ {VULNS_FOUND} SECURITY VULNERABILITIES DETECTED{NC}")
		print(f"  These are the problems that reverse-proxy-web in Prototype 3 resolves:")
		print(f"    1. No HTTPS/TLS     → TLS termination + HTTP→HTTPS redirect + HSTS")
		print(f"    2. No security headers → HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy")
		print(f"    3. No rate limiting  → Nginx rate limiting (20r/s + burst 10)")
		print(f"    4. Direct frontend   → Frontend hidden behind proxy, port 3000 internal")
		print(f"    5. Server info leak  → Proxy strips backend headers before sending to client")
		print(f"    6. No TLS cert       → Self-signed dev cert via reverse-proxy-web/certs")
		print(f"    7. HTTP OAuth URLs   → HTTPS callbacks enforced through proxy")
		print()

	return 0 if VULNS_FOUND == 0 else 1


if __name__ == "__main__":
	sys.exit(main())
