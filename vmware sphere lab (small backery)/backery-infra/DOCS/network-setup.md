# Doc: Network Setup

**Author:** Omar Mokheemer  
**Date:** 2026-05-29  
**Environment:** MokTech Lab — VMware vSphere

---

## Overview

Host 1 runs a Standard Switch (VSS) to avoid a bootstrap dependency on vCenter. Hosts 2 and 3 run a Distributed Switch (VDS) managed through vCenter.

---

## Host 1 — Standard Switch (VSS)

| Port Group | Purpose |
|---|---|
| Management Network | Host management (vmk0) |
| VM Network | Virtual machine traffic |

---

## Host 2 + 3 — Distributed Switch (VDS)

| Port Group | Purpose |
|---|---|
| Management port group | Host management (vmk0) |
| VM traffic port group | Virtual machine traffic |

---

## Notes

- Host 1 stays on VSS so management access does not depend on vCenter being online
- All 3 hosts have a VMkernel port enabled for vSAN traffic
