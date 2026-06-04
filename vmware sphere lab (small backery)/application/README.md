# MokTech Bakery — Web Application

A FastAPI + PostgreSQL bakery website with an online ordering system.

## Stack

| Layer    | Technology               |
|----------|--------------------------|
| Backend  | Python 3.11 + FastAPI    |
| Database | PostgreSQL               |
| Frontend | Jinja2 templates + Vanilla JS |
| Server   | Uvicorn (ASGI)           |
| Reverse proxy | Nginx              |
| Process manager | systemd         |

---

## Local Development

### 1. Prerequisites

- Python 3.11+
- PostgreSQL running locally

### 2. Set up the database

```sql
CREATE DATABASE bakery_db;
CREATE USER bakery_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE bakery_db TO bakery_user;
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and set DATABASE_URL
```

### 4. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 5. Run the app

```bash
uvicorn app.main:app --reload
```

Tables are created automatically on first run.

### 6. Seed sample products (optional)

```bash
python seed.py
```

App is now at http://localhost:8000

---

## VM Deployment

### 1. Copy files to the VM

```bash
scp -r application/ user@your-vm:/opt/bakery
```

### 2. Set up on the VM

```bash
cd /opt/bakery
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env   # set DATABASE_URL

python seed.py
```

### 3. Create a system user and fix ownership

```bash
sudo useradd --system --no-create-home bakery
sudo chown -R bakery:bakery /opt/bakery
```

### 4. Install the systemd service

```bash
sudo cp bakery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bakery
sudo systemctl start bakery
```

Check logs:

```bash
sudo journalctl -u bakery -f
```

### 5. Configure Nginx

```bash
sudo cp nginx.conf /etc/nginx/sites-available/bakery
sudo ln -s /etc/nginx/sites-available/bakery /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Edit `/etc/nginx/sites-available/bakery` and replace `your-domain.com` with your VM's IP or domain.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/products/` | List all products |
| POST | `/api/products/` | Create a product |
| PATCH | `/api/products/{id}` | Update a product |
| DELETE | `/api/products/{id}` | Delete a product |
| POST | `/api/orders/` | Place an order |
| GET | `/api/orders/` | List all orders |
| GET | `/api/orders/{id}` | Get single order |
| PATCH | `/api/orders/{id}/status` | Update order status |

Interactive API docs: `http://your-host/api/docs`

## Pages

| URL | Description |
|-----|-------------|
| `/` | Landing page |
| `/menu` | Product catalog with cart |
| `/order` | Cart review + order form |
| `/admin/orders` | Order management dashboard |
