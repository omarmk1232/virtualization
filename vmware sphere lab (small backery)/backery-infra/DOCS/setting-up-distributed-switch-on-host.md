# SOP: Setting Up a vSphere Distributed Switch and Migrating from Standard Switch

**Author:** Omar Mokheemer  
**Date:** 2026-05-29  
**Environment:** MokTech Lab — VMware vSphere

---

## Prerequisites

- vCenter is deployed and hosts are added to a Datacenter
- Each host has one vmnic (vmnic0) uplinked to a Standard Switch (vSwitch0)
- Management VMkernel (vmk0) is active on vSwitch0

---

## Architecture

**Before:**
```
vmnic0 → vSwitch0 → VM Network + Management (vmk0)
```

**After:**
```
vmnic0 → Distributed Switch → VM port group + Management port group (vmk0)
```

---

## Steps

1. **Create the Distributed Switch** in vCenter under Networking → right-click Datacenter → New Distributed Switch. Set uplink count to `1`.

2. **Create two port groups** on the VDS: one for management, one for VM traffic.

3. **Add host to VDS — uplink only.** Assign vmnic0 as Uplink 1. Do not migrate vmk0 yet.

4. **Migrate vmk0** to the management port group. Verify host connectivity immediately after.

5. **Migrate VMs** to the VM traffic port group.

6. **Remove vmnic0 from vSwitch0** and delete vSwitch0 if empty.

---

## Post-Migration Checklist

- [ ] Host connected in vCenter
- [ ] vmk0 on the management port group
- [ ] VMs reachable on network
- [ ] vSwitch0 removed

---

## Warning

With one vmnic there is no redundancy. If connectivity is lost during Step 4, recover via host console (DCUI) or direct host client at `https://<host-ip>/ui`.
