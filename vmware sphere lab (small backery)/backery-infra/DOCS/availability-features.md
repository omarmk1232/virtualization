# Doc: Availability Features — vMotion, DRS, HA, Fault Tolerance

**Author:** Omar Mokheemer  
**Date:** 2026-06-04  
**Environment:** MokTech Lab — VMware vSphere

---

## Overview

The workload cluster (Host 2 + Host 3) has vMotion, DRS, and HA enabled at the cluster level. Fault Tolerance is enabled individually on the app VM and database VM for continuous availability.

---

## vMotion

Live migrates a running VM between hosts with no downtime. Required for DRS and FT to function. Works because both hosts share the same NFS datastore — VM disks don't need to move, only compute state.

---

## DRS (Distributed Resource Scheduler)

**Mode:** Automatic

Continuously balances VM placement across Host 2 and Host 3 based on resource usage. If one host becomes more loaded, DRS automatically vMotions VMs to the other host — no manual intervention needed.

---

## HA (High Availability)

If a host fails, HA restarts the VMs that were running on it onto the surviving host. There is brief downtime during the restart while the VM boots back up.

---

## Fault Tolerance (FT)

**Enabled on:** App VM, Database VM

FT goes a step further than HA — it keeps a live shadow copy of the VM running on the other host, kept in lockstep with the primary. If the host running the primary fails, the secondary takes over instantly with **zero downtime and no dropped connections**.

FT was enabled on the app and database VMs specifically because they make up the bakery service — losing either one means the site goes down. The monitoring VM does not have FT since a brief interruption to monitoring is acceptable.

---

## Summary

| VM | HA | FT |
|---|---|---|
| App VM | Yes | Yes |
| Database VM | Yes | Yes |
| Monitoring VM | Yes | No |

---

## Notes

- FT requires both hosts to have enough spare capacity to run a full shadow copy of each protected VM at all times
- FT and DRS automatic vMotion both depend on shared NFS storage and host time sync (see [cluster-setup.md](cluster-setup.md) known issues)
