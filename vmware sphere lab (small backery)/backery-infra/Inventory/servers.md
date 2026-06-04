# Servers Inventory

**Environment:** MokTech Lab — VMware vSphere

---

## ESXi Hosts

| Hostname | IP | Purpose |
|---|---|---|
| host1.home.local | 192.168.1.49 | ESXi host — runs vCenter, DNS VM. Not part of the cluster |
| host2.home.local | 192.168.1.54 | ESXi host — workload cluster node |
| host3.home.local | 192.168.1.95 | ESXi host — workload cluster node |
| host4.home.local | 192.168.1.96 | ESXi host — workload cluster node |

---

## Physical Servers

| Hostname | IP | Purpose |
|---|---|---|
| main-nfs.home.local | 192.168.1.69 | NAS — shared VM datastore and content library (ISOs, templates) |
