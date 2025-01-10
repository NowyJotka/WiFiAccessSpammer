# WiFiAccessSpammer

Easily configure a Wi-Fi hotspot on your rooted Android device using Termux with tools like `hostapd` and `dnsmasq`.

## Prerequisites

- **Root Access:** Your device must be fully rooted.
- **Termux Installed:** [Download Termux](https://f-droid.org/en/packages/com.termux/).
- **Wi-Fi Adapter Support:** Ensure your device supports AP (Access Point) mode. You can check with:
  ```bash
  iw list
  ```
  If your device supports AP mode, you should see "AP" listed under "Supported interface modes".

## Installation

1. **Update and upgrade Termux:**
   ```bash
   pkg update && pkg upgrade
   ```

2. **Install required tools:**
   ```bash
   pkg install tsu hostapd dnsmasq
   ```
   - `tsu`: Provides root access in Termux.
   - `hostapd`: Configures the Wi-Fi hotspot.
   - `dnsmasq`: Manages DHCP and DNS for connected devices.
# Warn

1. You can use the python code to automatize this process, and with another python tool you can repeat the process to do a host spammer
2. **YOU CANT DO THIS WITH TERMUX FROM PlayStore OR WITH A NON-ROOTED PHONE**

# You need to have installed Python and be rooted

## Configuration

### Create the `hostapd.conf` file
Use a text editor like `nano` or `vi`:
```bash
nano hostapd.conf
```
Add the following configuration to `hostapd.conf`:
```bash
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
```

### Create the `dnsmasq.conf` file
```bash
nano dnsmasq.conf
```
Add the following configuration to `dnsmasq.conf`:
```bash
interface=wlan0
dhcp-range=192.168.43.2,192.168.43.100,12h
```

## Enabling IP Forwarding

Allow connected devices to access the internet by enabling IP forwarding and configuring iptables:
```bash
tsu
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
```

## Start the Wi-Fi Hotspot

Run the following commands to start the Wi-Fi hotspot:
```bash
hostapd hostapd.conf &
dnsmasq -C dnsmasq.conf &
```

## Stopping the Wi-Fi Hotspot

To stop the Wi-Fi hotspot, kill the processes:
```bash
pkill hostapd
pkill dnsmasq
```

## Troubleshooting

- **Wi-Fi Adapter Compatibility:** Not all Wi-Fi adapters on Android support AP mode. You can check your device’s Wi-Fi capabilities with:
  ```bash
  iw list
  ```
  Look for "AP" under "Supported interface modes" to verify compatibility.

- **Root Permissions:** Ensure you have proper root permissions. You can check if you have root access with:
  ```bash
  tsu
  ```

- **Android Interference:** Android manages network interfaces and may interfere with `hostapd`. You may need to disable any Wi-Fi management settings within Android for this to work correctly.

