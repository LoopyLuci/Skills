---
name: windows-network-config
description: "Use when configuring Windows network adapters and DNS."
category: software-development
tags: [windows, networking, dns, ip, adapter, configuration]
---
# Windows Network Configuration

Configuring network adapters, IP, DNS, and routing on Windows.

## Adapter Information

```powershell
# List adapters
Get-NetAdapter | Select-Object Name, Status, MacAddress, LinkSpeed

# Detailed adapter info
Get-NetAdapter -Name "Ethernet" | Get-NetAdapterBinding | Where-Object Enabled

# IP configuration
Get-NetIPAddress | Where-Object AddressFamily -eq IPv4 |
    Select-Object InterfaceAlias, IPAddress, PrefixLength

# DNS servers
Get-DnsClientServerAddress | Select-Object InterfaceAlias, ServerAddresses
```

## Configure Static IP

```powershell
# Set static IP
New-NetIPAddress -InterfaceAlias "Ethernet" `
    -IPAddress 192.168.1.100 `
    -PrefixLength 24 `
    -DefaultGateway 192.168.1.1

# Remove existing DHCP config
Remove-NetIPAddress -InterfaceAlias "Ethernet" -Confirm:$false

# Set DNS
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" `
    -ServerAddresses 8.8.8.8, 8.8.4.4
```

## Configure DHCP

```powershell
# Reset to DHCP
Set-NetIPInterface -InterfaceAlias "Ethernet" -Dhcp Enabled
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ResetServerAddresses

# Renew lease
ipconfig /release
ipconfig /renew
```

## Routing

```powershell
# View routing table
Get-NetRoute | Where-Object AddressFamily -eq IPv4 |
    Select-Object DestinationPrefix, NextHop, RouteMetric

# Add route
New-NetRoute -DestinationPrefix "10.0.0.0/8" -NextHop "192.168.1.1" `
    -InterfaceAlias "Ethernet" -RouteMetric 1

# Remove route
Remove-NetRoute -DestinationPrefix "10.0.0.0/8" -Confirm:$false
```

## DNS Troubleshooting

```powershell
# DNS cache
Clear-DnsClientCache
Get-DnsClientCache | Select-Name, Entry, Type

# Resolve hostname
Resolve-DnsName google.com -Type A
Resolve-DnsName google.com -Type MX

# Reverse lookup
Resolve-DnsName 8.8.8.8 -Type PTR
```

## Network Profiles

```powershell
# Set network profile (Public/Private/Domain)
Set-NetConnectionProfile -InterfaceAlias "Ethernet" -NetworkCategory Private

# Windows Firewall profile per network
Get-NetConnectionProfile | Select-Object Name, NetworkCategory
```

## Pitfalls

- Network changes may disconnect remote PowerShell sessions
- Static IP needs admin -- run as Administrator
- Some network adapters don't support all settings (Wi-Fi vs Ethernet)
- DNS cache clearing is immediate but client-side only
- Multiple default gateways can cause routing issues
