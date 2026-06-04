# Doc: Monitoring and Logging

**Author:** Omar Mokheemer  
**Date:** 2026-06-04  
**Environment:** MokTech Lab — VMware vSphere

---

## Overview

A dedicated monitoring VM runs the full observability stack. Grafana Alloy runs as an agent on each VM, collecting metrics and logs and forwarding them to the monitoring VM.

```
App VM      → Alloy → Prometheus + Loki (monitoring VM) → Grafana
Database VM → Alloy →
```

---

## Stack

| Component | Role | Port |
|---|---|---|
| Prometheus | Metrics storage | 9091 |
| Loki | Log storage | 3100 |
| Grafana | Dashboards | 3000 |
| Alloy | Agent on each VM — collects metrics and logs | — |

---

## Dashboards

### Node Exporter Full (ID: 1860)
Covers system-level metrics for the app server and database server:
- CPU, RAM, disk, network per VM
- Data source: Prometheus

### Logs / App
Covers all log sources from the app server:
- Nginx access and error logs
- Uvicorn / bakery app logs (via journald)
- System logs
- Data source: Loki

---

## Alloy — App Server Config

Collects:
- System metrics via `prometheus.exporter.unix`
- Nginx metrics via `prometheus.exporter.nginx` (requires nginx stub_status on `127.0.0.1:8080`)
- Nginx logs from `/var/log/nginx/*.log`
- App logs via `loki.source.journal`
- System logs from `/var/log/*.log`

---

## Alloy — Database Server Config

Collects:
- System metrics via `prometheus.exporter.unix`
- PostgreSQL logs from `/var/lib/pgsql/data/log/*.log`
- System logs from `/var/log/*.log`
- Journal logs via `loki.source.journal`

---

## Accessing Grafana

`http://monitoring.home.local:3000`

---

## Notes

- Prometheus has remote write receiver enabled (`--web.enable-remote-write-receiver`) — Alloy pushes metrics directly to it rather than Prometheus scraping the agents
- Alloy is configured to retry — if the monitoring VM is temporarily down, data will resume shipping once it comes back
