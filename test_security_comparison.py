#!/usr/bin/env python3
"""
Security Test Suite — Prototype 2 (WITHOUT Reverse Proxy)
Expected: ALL tests should FAIL since there is no reverse proxy.
This demonstrates the security vulnerabilities that the reverse proxy in Prototype 3 resolves.
"""

import subprocess
import sys
import os

try:
	import requests
except ImportError:
	print("Installing requests...")
	subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
	import requests

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"

PASS = 0
FAIL = 0
VULNS_FOUND = 0

# Prototype 2 exposes services directly — no reverse proxy
API_GATEWAY_URL = "http://localhost:8080"
WEB_PAGE_URL = "http://localhost:3000"

BACKEND_PORTS = [8080, 3001, 8000, 8001, 8193, 5432, 27017, 6379, 5672, 15672]


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


def test_service_exposure():
	"""Problem #1 from README: Unintended access to system resources"""
	header("TEST GROUP 1: Service Exposure (Confidentiality)")
	print("\n  Quality Scenario: Confidentiality — Limit Access")
	print("  Expected: ALL backend ports should be INACCESSIBLE from host")
	print("  (In Prototype 2, they are EXPECTED to be accessible = vulnerability)\n")

	accessible_ports = []
	for port in BACKEND_PORTS:
		print(f"  Testing port {port}...", end=" ")
		try:
			r = requests.get(f"http://localhost:{port}/", timeout=3)
			print(f"{RED}ACCESSIBLE (HTTP {r.status_code}){NC}")
			accessible_ports.append(port)
		except requests.ConnectionError:
			print(f"{GREEN}BLOCKED (connection refused){NC}")
		except requests.Timeout:
			print(f"{YELLOW}TIMEOUT{NC}")
			accessible_ports.append(port)
		except requests.RequestException as e:
			print(f"ERROR: {e}")

	if accessible_ports:
		vuln(f"Ports {accessible_ports} are DIRECTLY accessible from host — no reverse proxy isolation")
		info("This means an attacker can bypass authentication and rate limiting by hitting services directly")
	else:
		passed("No backend ports are directly accessible")

	return accessible_ports


def test_rate_limiting():
	"""Problem #2 from README: DDoS resistance (Availability)"""
	header("TEST GROUP 2: Rate Limiting (Availability)")
	print("\n  Quality Scenario: Availability — Resist Attack")
	print("  Expected: HTTP 429 Too Many Requests after burst threshold")
	print("  (In Prototype 2, there is NO rate limiting = vulnerability)\n")

	limited = False
	responses = []

	print(f"  Sending 30 rapid requests to API Gateway ({API_GATEWAY_URL}/health)...")
	for i in range(30):
		try:
			r = requests.get(f"{API_GATEWAY_URL}/health", timeout=3)
			code = r.status_code
			responses.append(code)
			if code == 429:
				limited = True
				break
		except requests.RequestException:
			pass

	if limited:
		passed(f"Rate limiting triggered HTTP 429 after {len(responses)} requests")
	else:
		vuln(f"No rate limiting — all 30 requests returned HTTP 200 (no 429 received)")
		info("Without rate limiting, the system is vulnerable to DDoS attacks (L7)")
		info("An attacker can exhaust resources by sending thousands of requests per second")

	return limited


def test_topology_leakage():
	"""Problem #2 from README: Internal topology exposure (Confidentiality)"""
	header("TEST GROUP 3: Internal Topology Leakage (Confidentiality)")
	print("\n  Quality Scenario: Confidentiality — Limit Access")
	print("  Expected: NO internal hostnames/ports in responses")
	print("  (In Prototype 2, internal details may leak in error messages)\n")

	infrastructure_patterns = [
		"users-service", "youtube-service", "google-trends-service",
		"nlp-service", "postgres:", "mongo:", "redis:", "rabbitmq:",
		"api-gateway:8080", "localhost:8080", "localhost:3001",
		"localhost:8000", "localhost:8001", "localhost:8193"
	]

	endpoints_to_check = [
		(f"{API_GATEWAY_URL}/health", "API Gateway /health"),
		(f"{API_GATEWAY_URL}/health/dependencies", "API Gateway /health/dependencies"),
	]

	for url, label in endpoints_to_check:
		print(f"  Checking {label}...")
		try:
			r = requests.get(url, timeout=10)
			found = [p for p in infrastructure_patterns if p in r.text]
			if found:
				vuln(f"Internal infrastructure leaked in {label}: {found}")
			else:
				passed(f"No internal routes leaked in {label}")
		except requests.RequestException as e:
			info(f"Could not reach {label}: {e}")


def test_single_entry_point():
	"""Reverse proxy property: single point of entry"""
	header("TEST GROUP 4: Single Entry Point (Confidentiality)")
	print("\n  Expected: Only ONE port should be externally accessible")
	print("  (In Prototype 2, MULTIPLE ports are exposed = vulnerability)\n")

	services_exposed = []
	service_map = {
		3000: "web-page (Frontend)",
		8080: "api-gateway",
		3001: "users-service",
		8000: "youtube-service",
		8001: "google-trends-service",
		8193: "nlp-service",
		5432: "postgres (Database)",
		27017: "mongo (Database)",
		6379: "redis (Cache)",
	}

	for port, name in service_map.items():
		try:
			r = requests.get(f"http://localhost:{port}/", timeout=3)
			services_exposed.append((port, name))
			print(f"  {RED}✗ Port {port} ({name}): ACCESSIBLE — bypasses any gateway{NC}")
		except requests.ConnectionError:
			print(f"  {GREEN}✓ Port {port} ({name}): Not accessible{NC}")
		except requests.Timeout:
			services_exposed.append((port, name))
			print(f"  {YELLOW}⚠ Port {port} ({name}): Timeout (may be accessible){NC}")
		except requests.RequestException:
			print(f"  {GREEN}✓ Port {port} ({name}): Not accessible{NC}")

	if len(services_exposed) > 1:
		vuln(f"{len(services_exposed)} services are directly accessible — no single entry point")
		info(f"Exposed services: {[(p, n) for p, n in services_exposed]}")
		info("Attack surface is expanded: each service is an independent attack vector")
	else:
		passed("Only one entry point exposed")


def test_credential_exposure():
	"""Check if docker-compose.yml exposes credentials in plain text"""
	header("TEST GROUP 5: Credential Exposure in Configuration (Confidentiality)")
	print("\n  Expected: Secrets should be in .env files, not hardcoded")
	print("  (In Prototype 2, secrets are HARDCODED in docker-compose.yml)\n")

	compose_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docker-compose.yml")
	try:
		with open(compose_path, "r") as f:
			content = f.read()

		sensitive_patterns = {
			"JWT_SECRET": "JWT Secret for authentication",
			"POSTGRES_PASSWORD": "Database password",
			"SMTP_PASS": "SMTP credentials",
			"GOOGLE_CLIENT_SECRET": "OAuth client secret",
			"YOUTUBE_API_KEY": "YouTube API key",
			"NVIDIA_NIM_API_KEY": "NVIDIA NIM API key",
			"MONGO_URI": "MongoDB connection string with credentials",
		}

		for pattern, desc in sensitive_patterns.items():
			if pattern in content:
				# Check if it's hardcoded (not using ${} variable)
				lines_with_pattern = [l for l in content.splitlines() if pattern in l and "${" not in l.split(":", 1)[1] if ":" in l]
				if lines_with_pattern:
					vuln(f"{desc} ({pattern}) is HARDCODED in docker-compose.yml")
				else:
					passed(f"{desc} ({pattern}) uses environment variables")
			else:
				info(f"{desc} ({pattern}) not found in docker-compose.yml")
	except FileNotFoundError:
		failed(f"docker-compose.yml not found")


def test_docker_network_isolation():
	"""Check if Docker networks isolate services properly"""
	header("TEST GROUP 6: Docker Network Isolation (Confidentiality)")
	print("\n  Expected: Backend services on internal networks, only proxy on public")
	print("  (In Prototype 2, there are NO network isolation definitions)\n")

	compose_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docker-compose.yml")
	try:
		with open(compose_path, "r") as f:
			content = f.read()

		if "networks:" in content and "internal: true" in content:
			passed("Docker networks are defined with internal isolation")
		elif "networks:" in content:
			info("Docker networks are defined but without internal isolation")
		else:
			vuln("No Docker network isolation defined — all services share the default network")
			info("Without network segmentation, services can reach each other without restrictions")

	except FileNotFoundError:
		failed("docker-compose.yml not found")


def main():
	print()
	print("╔" + "═" * 68 + "╗")
	print("║" + " " * 8 + "SECURITY TEST SUITE — PROTOTYPE 2 (NO REVERSE PROXY)" + " " * 9 + "║")
	print("╚" + "═" * 68 + "╝")
	print(f"  Target: Prototype 2 — Direct service access (no proxy)")
	print(f"  Expected result: Multiple security vulnerabilities found")
	print(f"  Reference: Problems described in Prototype 3's README.md")
	print()

	test_service_exposure()
	test_rate_limiting()
	test_topology_leakage()
	test_single_entry_point()
	test_credential_exposure()
	test_docker_network_isolation()

	print()
	print("=" * 70)
	print(f"  SUMMARY: {PASS} passed, {FAIL} failed, {VULNS_FOUND} vulnerabilities found")
	print("=" * 70)

	if VULNS_FOUND > 0:
		print()
		print(f"{RED}  ⚠ {VULNS_FOUND} SECURITY VULNERABILITIES DETECTED{NC}")
		print(f"  These are the problems that the Reverse Proxy in Prototype 3 resolves:")
		print(f"    1. Service exposure → Reverse proxy hides all backend ports")
		print(f"    2. No rate limiting → Nginx rate limiting with HTTP 429")
		print(f"    3. Topology leakage → proxy_hide_header removes internal headers")
		print(f"    4. Multiple entry points → Single port 8081 for all traffic")
		print(f"    5. Hardcoded credentials → .env files with network isolation")
		print(f"    6. No network isolation → Docker network segmentation")
		print()

	return 0 if VULNS_FOUND == 0 else 1


if __name__ == "__main__":
	sys.exit(main())
