# Doc: DNS Setup

**Author:** Omar Mokheemer  
**Date:** 2026-05-30  
**Environment:** MokTech Lab — VMware vSphere

---

## Overview

A centralized DNS VM running Technitium DNS Server manages all local name resolution for the lab. All hosts and VMs use this server as their primary DNS.

- **DNS Server:** Technitium DNS
- **Local Zone:** `home.local`

---

## Architecture

```
All VMs + Hosts → Technitium DNS VM → resolves home.local locally
                                    → forwards everything else upstream
```

---

## Local Zone

All internal resources are registered under `home.local`. Examples:

| Hostname | FQDN |
|---|---|
| vCenter | vcenter.home.local |
| Host 1 | host1.home.local |
| Host 2 | host2.home.local |
| Host 3 | host3.home.local |
| App VM | bakery-app.home.local |
| Database VM | bakery-db.home.local |
| Monitoring VM | monitoring.home.local |
| NFS Server 1 | nfs1.home.local |
| NFS Server 2 | main-nfs.home.local |

---

## Configuring DNS on Each VM (Rocky Linux)

Set the Technitium DNS VM as the nameserver:

```bash
nmcli con mod <connection-name> ipv4.dns <technitium-vm-ip>
nmcli con up <connection-name>
```

Verify resolution:

```bash
nslookup vcenter.home.local
```

---

## Configuring DNS on ESXi Hosts

On each host go to **Networking → DNS Configuration** and set the primary DNS to the Technitium VM IP.

---

## Notes

- Technitium forwards unresolved queries upstream — internet resolution still works normally
