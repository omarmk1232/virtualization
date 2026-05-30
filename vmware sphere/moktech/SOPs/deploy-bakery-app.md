# SOP: Deploy Bakery Application

**Author:** Omar Mokheemer  
**Date:** 2026-05-31  
**Environment:** MokTech Lab — VMware vSphere

---

## Prerequisites

- App VM and Database VM are deployed from the golden image
- DNS records exist for both VMs in Technitium (`home.local`)
- PostgreSQL is running on the database VM with `bakery_db` and `bakery_user` created
- App files are available on the deployment machine

---

## Step 1 — Copy App Files to the VM

```bash
ssh admin@bakery-app.home.local "sudo mkdir -p /opt/bakery && sudo chown admin:admin /opt/bakery"
scp -r application/* admin@bakery-app.home.local:/opt/bakery
```

---

## Step 2 — Install Dependencies

```bash
ssh admin@bakery-app.home.local
sudo dnf install python3.11 python3.11-pip python3.11-venv nginx -y
```

---

## Step 3 — Set Up Python Environment

```bash
cd /opt/bakery
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Step 4 — Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set the database URL pointing to the database VM:

```
DATABASE_URL=postgresql://bakery_user:yourpassword@bakery-db.home.local:5432/bakery_db
```

---

## Step 5 — Create App User and Fix Ownership

```bash
sudo useradd --system --no-create-home bakery
sudo chown -R bakery:bakery /opt/bakery
```

---

## Step 6 — Install and Start the Bakery Service

```bash
sudo cp bakery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now bakery
```

Verify:
```bash
sudo systemctl status bakery
sudo journalctl -u bakery -f
```

---

## Step 7 — Configure Nginx

```bash
sudo cp nginx.conf /etc/nginx/conf.d/bakery.conf
```

Edit `server_name` in `/etc/nginx/conf.d/bakery.conf` to `bakery-app.home.local`, then:

```bash
sudo nginx -t
sudo systemctl enable --now nginx
```

---

## Step 8 — Configure Firewall and SELinux

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
sudo setsebool -P httpd_can_network_connect 1
```

---

## Step 9 — Seed the Database

```bash
cd /opt/bakery
source venv/bin/activate
python seed.py
```

---

## Verify

- App is accessible at `http://bakery-app.home.local`
- Menu loads with products
- An order can be placed successfully

---

## Known Issues

**Permission denied for schema public** — PostgreSQL 15+ restricts public schema access by default. Fix:
```sql
GRANT ALL ON SCHEMA public TO bakery_user;
```

**Nginx connect() permission denied (13)** — SELinux blocks Nginx from proxying to the app. Fix:
```bash
setsebool -P httpd_can_network_connect 1
```
