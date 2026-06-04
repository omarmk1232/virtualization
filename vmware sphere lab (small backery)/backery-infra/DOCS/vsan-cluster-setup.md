# Doc: vSAN Cluster Setup (3-Node)

**Author:** Omar Mokheemer  
**Date:** 2026-05-29  
**Environment:** MokTech Lab — VMware vSphere

---

## Prerequisites

- ESXi installed on all 3 hosts
- All hosts added to a vCenter Datacenter and Cluster
- Each host has a VMkernel port with vSAN traffic enabled
- Each host has at least one cache disk and one capacity disk

---

## Architecture

All 3 hosts are full data nodes. No witness needed.

```
Host 1 + Host 2 + Host 3 → vSAN Datastore
```

- FTT=1 (one host can fail, cluster keeps running)
- vCenter runs as a VM on the vSAN it manages

---

## Steps

1. **Enable vSAN VMkernel on each host** — on each host go to Networking → VMkernel adapters → enable vSAN traffic on the appropriate vmk.

2. **Create a Cluster in vCenter** — right-click Datacenter → New Cluster → enable vSAN.

3. **Add all 3 hosts to the cluster.**

4. **Claim disks** — vCenter will prompt to claim cache and capacity disks on each host. Assign accordingly.

5. **Verify the datastore** — vSAN datastore should appear under Storage once all disks are claimed.

---

## Post-Setup Checklist

- [ ] vSAN datastore visible in vCenter
- [ ] All 3 hosts show green in vSAN health (Cluster → Monitor → vSAN → Health)
- [ ] No disk claim errors
- [ ] FTT policy set to 1

---

## Notes

- vCenter is deployed onto this vSAN datastore — during cold starts, bring all 3 hosts up before expecting vCenter to come online
- Do not remove a host from the cluster without first migrating its data off

---

## Why vSAN Was Not Used in This Lab

vSAN requires a minimum of 2 disks per host — one cache disk (SSD) and one capacity disk (HDD/SSD) for OSA, or NVMe drives for ESA. Each host in this lab has only a single HDD with no SSD or NVMe. Neither architecture is supported under these conditions. NFS shared storage is used instead as the primary VM datastore.
