# Complete Guide: Configuring nftables to Allow Only Cloudflare IPs for Web Access

## Introduction
In today's cybersecurity landscape, protecting your VPS server from malicious attacks is crucial. This comprehensive guide demonstrates how to implement nftables firewall rules that only allow web access from Cloudflare's IP addresses, significantly enhancing your server's security posture.

## Prerequisites
- A Linux-based VPS server (Ubuntu, Debian, etc.)
- Root or sudo privileges
- Basic command line knowledge
- Cloudflare configured as your CDN provider

## Quick Deployment

### 1. Install Required Components
First, install curl and nftables:
```bash
apt update && apt install curl nftables -y
```

### 2. Deploy Firewall Rules
Execute the following command to deploy pre-configured nftables rules:
```bash
bash <(curl -s https://raw.githubusercontent.com/azoway/across/main/nftables/nft-cloudflare.sh)
```

## Configuration Details
The default configuration includes the following features:
- ✅ Allows SSH access (port 22) from any IP address
- ✅ Restricts web ports (80 and 443) to Cloudflare IPv4 addresses only
- ✅ Implements ICMP (ping) rate limiting to prevent DoS attacks
- ✅ Automatically fetches and implements the latest Cloudflare IP ranges

## Custom Configuration
To customize the configuration:
1. Visit the [nftables cloudflare script](https://github.com/azoway/across/blob/main/nftables/nft-cloudflare.sh)
2. Modify according to your needs:
   - Whitelist specific IP addresses
   - Customize port rules
   - Adjust access restriction policies

## Important References
- Official Cloudflare IP ranges: https://www.cloudflare.com/ips/
- This configuration includes IPv4 addresses only; modify rules for IPv6 support

## Troubleshooting
If you encounter issues, verify:
1. nftables service status
2. Proper loading of firewall rules
3. Server access to Cloudflare IP lists

## Security Best Practices
- Update firewall rules regularly
- Monitor server access logs
- Keep system and packages updated

## Advanced Tips
- Consider implementing additional security layers
- Regular security audits
- Backup your firewall configurations

## Conclusion
This configuration significantly enhances your server's security by restricting web access to Cloudflare's IP addresses only. Regular maintenance and updates are recommended to ensure continued protection.

## Technical Notes
- Compatible with major Linux distributions
- Minimal performance impact
- Automated rule updates available
- Logging capabilities for security monitoring 