# Doc: Golden Image

**Author:** Omar Mokheemer  
**Date:** 2026-05-30  
**Environment:** MokTech Lab — VMware vSphere

---

## Overview

A single golden image based on Rocky Linux 10 is used as the base template for all VMs in the environment. It is stored in the content library on NFS Server 1. All VMs are deployed from this template using a **VM Customization Specification** to manually specify the hostname, static IP address, subnet, gateway, and DNS per VM at deploy time.

---

## Base OS

- **OS:** Rocky Linux 10
- **Storage:** Content library (NFS Server 1)
- **Type:** VM Template

---

## Disk Layout

Single disk, partitioned as follows:

| Partition | Mount | Size |
|---|---|---|
| /dev/sda1 | /boot | 1GB |
| /dev/sda2 | swap | 2GB |
| /dev/sda3 | / | 20GB |
| /dev/sda4 | /var | remaining space |

---

## Steps

1. **Create a new VM** — use the Rocky Linux 10 ISO from the content library to install the OS
2. **Install Rocky Linux 10** — minimal install, no unnecessary packages
3. **Post-install configuration:**
   - Update all packages — `dnf update -y`
   - Install VMware Tools — `dnf install open-vm-tools -y`
   - Disable root login — `passwd -l root`
   - Create a named admin user with sudo access
   - Set timezone and NTP
   - Disable unnecessary services
   - Configure SSH access (disable root SSH login in `/etc/ssh/sshd_config`)
4. **Clean up the VM** before converting to template:
   - Clear bash history
   - Remove machine-specific network config
   - Run `dnf clean all`
5. **Convert to template** — in vCenter right-click the VM → Convert to Template
6. **Add to content library** — right-click the template → Clone to Library → select the content library on NFS Server 1

---

## Base Packages

Installed on every VM regardless of role:

| Package | Purpose |
|---|---|
| `open-vm-tools` | VMware guest integration |
| `tailscale` | VPN access |
| `firewalld` | Host-level firewall |
| `chrony` | NTP time sync |
| `dnf-automatic` | Scheduled security updates |
| `curl`, `wget`, `vim`, `tar` | Basic admin tools |
| `alloy` | Ships metrics and logs to Prometheus and Loki on the monitoring VM |

---

## Patching

**Automatic — security updates only (dnf-automatic)**

Install and configure:
```bash
dnf install dnf-automatic -y
```

Edit `/etc/dnf/automatic.conf`:
```ini
upgrade_type = security
apply_updates = yes
```

Override the timer schedule to run every weekend at 12:00:
```bash
systemctl edit dnf-automatic.timer
```

```ini
[Timer]
OnCalendar=
OnCalendar=Sat,Sun 12:00
RandomizedDelaySec=0
```

Enable:
```bash
systemctl daemon-reload
systemctl enable --now dnf-automatic.timer
```

**Manual — full updates via Ansible (planned, not yet configured)**

Ansible patching playbook for full updates is planned for a future setup. For now, run `dnf update -y` manually on each VM. Always take a VM snapshot in vCenter before running updates.

---

## Notes

- Any change to the base config requires cloning the template back to a VM, making the change, then re-converting to template
- All workload VMs are deployed from this template to ensure a consistent base
