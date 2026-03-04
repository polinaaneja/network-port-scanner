import socket
import threading
from datetime import datetime

# Dictionary of common ports and their services
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-ALT"
}

# Ask user for target IP
target = input("Enter target IP address: ")

print("-" * 50)
print("Scanning Target:", target)
print("Time Started:", datetime.now())
print("-" * 50)

# List to store open ports
open_ports = []


# Function to grab banner (server info)
def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None


# Function to scan each port
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((target, port))

        if result == 0:
            service = common_ports.get(port, "Unknown")
            banner = grab_banner(target, port)

            print(f"[OPEN] Port {port} -> {service}")

            if banner:
                print("Banner:", banner)

            open_ports.append((port, service, banner))

        s.close()

    except:
        pass


# Create threads for faster scanning
threads = []

for port in range(1, 1025):
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("\nScan Completed")
print("Open Ports Found:", len(open_ports))


# Save results to a file
with open("scan_report.txt", "w", encoding="utf-8") as file:

    file.write("Scan Report\n")
    file.write(f"Target: {target}\n")
    file.write(f"Time: {datetime.now()}\n\n")

    for port, service, banner in open_ports:
        file.write(f"Port {port} -> {service}\n")

        if banner:
            file.write(f"Banner: {banner}\n")

        file.write("\n")

print("Results saved to scan_report.txt")





















