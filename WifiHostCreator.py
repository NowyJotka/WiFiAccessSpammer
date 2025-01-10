import os
import subprocess

def run_command(command):
    process = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(process.stdout)
    if process.stderr:
        print(process.stderr)

def create_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def main():
    try:
        run_command("tsu")
        run_command("pkg update && pkg upgrade -y")
        run_command("pkg install -y tsu hostapd dnsmasq")

        hostapd_conf_content = """
interface=wlan0
driver=nl80211
ssid=TermuxHotspot
hw_mode=g
channel=6
auth_algs=1
wpa=2
wpa_passphrase=YourSecurePassword
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
"""
        create_file("hostapd.conf", hostapd_conf_content)

        dnsmasq_conf_content = """
interface=wlan0
dhcp-range=192.168.43.2,192.168.43.100,12h
"""
        create_file("dnsmasq.conf", dnsmasq_conf_content)

        run_command("echo 1 > /proc/sys/net/ipv4/ip_forward")
        run_command("iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE")
        run_command("hostapd hostapd.conf &")
        run_command("dnsmasq -C dnsmasq.conf &")

        print("Wi-Fi Hotspot is now running!")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
