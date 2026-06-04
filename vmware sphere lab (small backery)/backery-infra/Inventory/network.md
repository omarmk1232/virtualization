# Network Inventory

**Environment:** MokTech Lab — VMware vSphere

---

## Hosts

| Hostname | IP | Switch | Notes |
|---|---|---|---|
| host1.home.local | 192.168.1.49 | VSS | Runs vCenter — not in cluster |
| host2.home.local | 192.168.1.54 | VDS | Cluster node — workloads |
| host3.home.local | 192.168.1.95 | VDS | Cluster node — workloads |
| host4.home.local | 192.168.1.96 | VDS | Cluster node — workloads |
| main-nfs.home.local | 192.168.1.69 | — | NAS — shared storage, VM datastore + content library |

Each ESXi host has one vmnic only.

---

## Networking

### Host 1 — Standard Switch (VSS)

| Port Group | Purpose |
|---|---|
| Management Network | Host management (vmk0) |
| VM Network | Virtual machine traffic |

### Host 2, 3, 4 — Distributed Switch (VDS)

Two node groups:

| Node Group | Purpose |
|---|---|
| Management | Host management VMkernel (vmk0) |
| Workloads | Virtual machine traffic |

---

## Virtual Machines

| Hostname | IP | Role |
|---|---|---|
| vcenter.home.local | 192.168.1.52 | vCenter Server |
| dns.home.local | 192.168.1.53 | Technitium DNS — home.local zone |
| bakery-app.home.local | 192.168.1.60 | Bakery application server |
| bakery-db.home.local | 192.168.1.61 | PostgreSQL database server |
| monitoring.home.local | 192.168.1.63 | Prometheus + Loki + Grafana |
vCenter and DNS run on Host 1 under the VSS.

---

## Firewall Rules

### bakery-app (192.168.1.60)

| Port | Protocol | Allow From | Purpose |
|---|---|---|---|
| 22 | TCP | Admin only | SSH |
| 80 | TCP | Any | Nginx / bakery web app |

### bakery-db (192.168.1.61)

| Port | Protocol | Allow From | Purpose |
|---|---|---|---|
| 22 | TCP | Admin only | SSH |
| 5432 | TCP | 192.168.1.60 only | PostgreSQL |

### monitoring (192.168.1.63)

| Port | Protocol | Allow From | Purpose |
|---|---|---|---|
| 22 | TCP | Admin only | SSH |
| 3000 | TCP | Any | Grafana |
| 9091 | TCP | 192.168.1.60, 192.168.1.61 | Prometheus remote write |
| 3100 | TCP | 192.168.1.60, 192.168.1.61 | Loki log ingestion |

### dns (192.168.1.53)

| Port | Protocol | Allow From | Purpose |
|---|---|---|---|
| 53 | TCP/UDP | Any | DNS resolution |

### main-nfs.home.local (192.168.1.69)

| Port | Protocol | Allow From | Purpose |
|---|---|---|---|
| 22 | TCP | Admin only | SSH |
| 2049 | TCP/UDP | 192.168.1.54, 192.168.1.95, 192.168.1.96 | NFS |

### ESXi Hosts

| Port | Protocol | Purpose |
|---|---|---|
| 22 | TCP | SSH management |
| 443 | TCP | vSphere Client / vCenter communication |
