# Doc: Cluster Setup

**Author:** Omar Mokheemer  
**Date:** 2026-05-29  
**Environment:** MokTech Lab — VMware vSphere

---

## Overview

A 2-node workload cluster using Host 2 and Host 3. Host 1 is excluded and runs vCenter only.

---

## Why Host 1 is Not in the Cluster

Host 1 is almost fully utilized running vCenter Server. Adding it to the cluster would make it eligible to receive workload VMs from DRS or HA failover, which would compete with vCenter for resources and risk destabilizing the management layer. Keeping it separate ensures vCenter always has the resources it needs.

---

## Cluster Layout

| Host | Role |
|---|---|
| Host 1 | vCenter only — not in cluster |
| Host 2 | Workload cluster node |
| Host 3 | Workload cluster node |

---

## Enabled Features

| Feature | Status |
|---|---|
| HA | Enabled — if one host fails, VMs restart on the other |
| DRS | Enabled — balances VM load between Host 2 and Host 3 |
| vMotion | Enabled — live migrate VMs between hosts |

---

## Steps

1. In vCenter go to your Datacenter → **New Cluster**
2. Name the cluster and enable **HA** and **DRS**
3. Add **Host 2** and **Host 3** to the cluster
4. Once shared storage is attached, configure the shared datastore for the cluster

---

## Notes

- With 2 nodes, if one host fails HA will restart all its VMs on the remaining host — make sure that host has enough resources to carry the full workload
- DRS requires shared storage to move VMs between hosts (vMotion will not work on local storage)

---

## Known Issues

**Time sync between hosts** — both hosts must be synchronized to the same NTP server, otherwise HA and vMotion will fail or behave unexpectedly. Configure NTP on each host under Host → Configure → Time Configuration and point them to the same NTP source.
