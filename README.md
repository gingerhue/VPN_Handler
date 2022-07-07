# VPN_Handler_python

### Simple VPN Auto-connector for Linux

#### Description:

> The script chooses a random server from the list and tries to connect to it. It checks connectivity every 5 seconds. If connection is lost it will reconnect to a random server again.

#### Steps:

1. **Get configuration files**:

- Go to your VPN Provider website.
- Save credentials(_username, password_) for manual setup.
- Download configuration files. In my case these are NordVPN files.

```bash
curl -O https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
```

- Unzip the archive

```bash
unzip ovpn.zip -d path/to/put/extracted_file
```

2. **Clone the repository**:

```bash
git clone https://github.com/gingerhue/VPN_Handler_python.git
```

3. **Run Configuration Handler**:

- Go to the root directory

```bash
cd VPN_Handler_python
```

- Run the script in an interactive way. It will copy needed configuration files and create VPN connections.

```bash
./interactive_setup.py
```

- Alternatively, use configs_handler in the helpers directory to write your own code

4. **Store VPN password credentials**:
``` bash
secret-tool store --label='label' attribute value 
```

3. **Start the handler**:

- Edit vpn_handler.py. Change attribute and value to those you came up with.

- Run the script:

```bash
./vpn_handler.py
```

---
### Symlink:
> Create a symlink to the handler to run it in terminal with your alias.
- Make the script executable:
``` bash
chmod +x vpn_handler.py
```
- Make the bin directory inside your home directory:
``` bash
mkdir $HOME/bin
```
- Create a symlink:
``` bash
ln -s $HOME/path/to/vpn_handler.py $HOME/bin/invoke_name
```

---

### VPN Killswitch Configuration

#### Description:

> Setup for your firewall to prevent data from being exposed to the third party. Data is only transfered between you and VPN server through a secure tunnel. If you lose your VPN Connection killswitch feature blocks all traffic until the connection is restored again. It makes sure your online activity and browsing history, along with your IP address and location, cannot be visible to and tracked by others.

#### Brief Setup:

1. **Disable IPv6**:

```bash
sudo nano /etc/sysctl.conf
```

- Paste the following:

```bash
net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1
net.ipv6.conf.lo.disable_ipv6=1
```

- Reload sysctl config:

```bash
sudo sysctl -p
```

- Check the changes. The output should be **1**:

```bash
cat /proc/sys/net/ipv6/conf/all/disable_ipv6
```

- Disable IPv6 in your firewall settings. You might need to restart firewall:

```bash
sudo nano /etc/default/ufw
IPV6=0
```

2. **Local Traffic**:

- Grab your local IP address along with subnet:

```bash
ip addr | grep inet
```

- Allow traffic go in and out to your local IP:

```bash
sudo ufw allow in to 192.168.0.103/24
sudo ufw allow out to 192.168.0.193/24
```

3. **Main part**:

- Deny all traffic:

```bash
sudo ufw default deny outgoing
sudo ufw default deny incoming
```

- Go to the directory where your configuration files are kept. Open the desired config with your text editor. We need the fourth line with server's IP and port. Copy IP and port.

```bash
remote 212.102.36.150 1194
```

- Configure restrictions that traffic goes to server's IP strictly. Last word is for protocol that you're using. TCP/UDP. Use the _ufw_conf.py_ script in the helpers section to automate the process for all connections.

```bash
sudo ufw allow out to 212.102.36.150 port 1194 proto udp
```

- Configure that traffic goes exclusively through VPN interface:

```bash
sudo ufw allow out tun0 from any to any
sudo ufw allow in on tun0 from any to any
```

4. **Enable/Disable UFW**:

```bash
sudo ufw enable
sudo ufw disable
```
