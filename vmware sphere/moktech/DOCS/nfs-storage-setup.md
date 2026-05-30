# Doc: NFS Storage Setup

**Author:** Omar Mokheemer  
**Date:** 2026-05-30  
**Environment:** MokTech Lab — VMware vSphere

---

## Overview

A single NFS server handles both the content library and VM datastore:

| Server | Purpose | Connected To |
|---|---|---|
| NFS Server (main) | Content library + VM datastore | Host 2 + Host 3 |

NFS Server is mounted only on Host 2 and Host 3 since they form the workload cluster. Host 1 runs vCenter and does not need access to the VM datastore.

---

## Steps

1. On the NFS server, create and export the share with appropriate permissions for the ESXi hosts
2. In vCenter go to Host 2 → Storage → New Datastore → NFS → enter server IP and export path
3. Repeat for Host 3
4. Verify the datastore appears on both hosts under Storage

---

## Changes

### Consolidated to Single NFS Server

Initially two NFS servers were used — a small one for the content library and a larger one for VM data. Deploying VMs from the template on NFS Server 1 to the datastore on NFS Server 2 was timing out due to the copy routing through the ESXi host across two separate servers. Both the content library and VM datastore were moved to the main NFS server, eliminating the cross-server copy and resolving the timeout issue.

---

## Issues Faced

### Firewall Blocking NFS Traffic

The NFS server's firewall was blocking traffic from the ESXi hosts. Had to open the relevant NFS ports on the server firewall before the hosts could mount the share.

### NFS Version — Must Use NFSv4 on ESXi 8

ESXi 8 has known issues mounting NFSv3 shares — the datastore would not mount or would drop connectivity. Switching to **NFSv4** resolved the issue. When adding the NFS datastore in vCenter, ensure NFS version is set to **4** not 3.
