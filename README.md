<div align="center">

# ⚡ StreamBill Pro

### Production-Ready Usage-Based Billing Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis_Streams-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Razorpay](https://img.shields.io/badge/Razorpay-02042B?style=for-the-badge&logo=razorpay&logoColor=3395FF)](https://razorpay.com)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Celery](https://img.shields.io/badge/Celery-Planned-37814A?style=for-the-badge&logo=celery&logoColor=white)](#)

<br/>

> **Inspired by Stripe Billing, Lago, and Metronome.**
> Built for SaaS companies that charge based on what their customers actually use.

<br/>

[Overview](#-overview) • [Features](#-current-features) • [Architecture](#-architecture) • [Quick Start](#-installation) • [API Modules](#-api-modules) • [Billing Flow](#-billing-flow)

</div>

---

## 🚀 Overview

**StreamBill Pro** is a modern usage-based billing platform that enables SaaS companies to:

| Capability | Description |
|---|---|
| 🔐 **Authenticate** | Secure organization-level auth with JWT and API keys |
| 👥 **Manage Customers** | Multi-tenant customer and product management |
| 📊 **Track Usage** | Ingest millions of API usage events reliably |
| ⚙️ **Process Async** | Background event processing via Redis Streams |
| 🧾 **Invoice** | Automated graduated pricing and invoice generation |
| 💳 **Collect Payments** | Native Razorpay integration for Indian markets |
| 📈 **Scale** | Architected toward enterprise-grade workloads |

---

## ✨ Current Features

<table>
<tr>
<td width="50%">

### 🔐 Authentication
- JWT Authentication
- Secure password hashing
- Login & Registration

### 🏢 Organizations
- Multi-tenant architecture
- Organization management
- API Key generation

### 👤 Customers
- Customer CRUD
- External customer IDs

### 🛍️ Products
- Product catalog
- Pricing tier management

</td>
<td width="50%">

### 💰 Billing
- Graduated pricing
- Usage aggregation
- Invoice generation

### ⚡ Event Processing
- Redis Streams
- Background worker
- Idempotent event ingestion

### 💳 Payments
- Razorpay order creation
- Payment verification APIs
- Invoice status updates

### 🗄️ Database
- PostgreSQL
- Async SQLAlchemy
- Alembic migrations

</td>
</tr>
</table>

---

## 🏗 Architecture

```
                    ┌─────────────────────┐
                    │   React Dashboard   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
          ┌─────────┴─────────┬───────────┴─────────┐
          │                   │                     │
   ┌──────▼──────┐   ┌────────▼───────┐   ┌────────▼───────┐
   │Authentication│   │    Billing     │   │    Payments    │
   └──────┬───────┘   └────────┬───────┘   └────────┬───────┘
          │                    │                     │
          └──────────┬─────────┘                     │
                     ▼                               ▼
           ┌──────────────────┐           ┌──────────────────┐
           │  Redis Streams   │           │    Razorpay      │
           └────────┬─────────┘           └──────────────────┘
                    │
                    ▼
           ┌──────────────────┐
           │Background Worker │
           └────────┬─────────┘
                    │
                    ▼
           ┌──────────────────┐
           │   PostgreSQL     │
           └──────────────────┘
```

---

## 🗺 Production Architecture *(Roadmap)*

The project is designed to evolve with:

```
Current Stack                    Production Evolution
─────────────────                ──────────────────────────────
FastAPI          →               FastAPI + Celery Workers
Redis Streams    →               Redis Streams + Monitoring
Basic Workers    →               Scheduled Billing + Webhooks
Manual Deploy    →               Docker + Docker Compose + AWS ECS
No Observability →               Prometheus + Grafana
```

Planned production enhancements include:

- ☐ Celery Workers & Scheduled Billing
- ☐ PDF Invoice Generation
- ☐ Email Notifications
- ☐ Docker & Docker Compose
- ☐ AWS Deployment
- ☐ GitHub Actions CI/CD
- ☐ Monitoring (Prometheus + Grafana)
- ☐ Webhooks & Analytics Dashboard

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy Async |
| **Migrations** | Alembic |
| **Queue** | Redis Streams |
| **Payments** | Razorpay |
| **Frontend** | React + Vite *(In Progress)* |
| **Auth** | JWT |
| **Validation** | Pydantic |

---

## 📁 Project Structure

```
StreamBill-Pro/
│
├── backend/
│   ├── app/
│   │   ├── api/             # Route handlers
│   │   ├── core/            # Security, config, Redis client
│   │   ├── db/              # Session factory, engine
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── services/        # Business logic layer
│   │   ├── workers/         # Redis Streams consumer + tasks
│   │   └── main.py          # App entry point
│   ├── alembic/             # Database migrations
│   └── requirements.txt
│
├── frontend/                # React + Vite (In Progress)
└── README.md
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/JayantDethe26/StreamBill-Pro.git
cd StreamBill-Pro
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
# Fill in your values — see Environment Variables below
```

**5. Run database migrations**
```bash
alembic upgrade head
```

**6. Start Redis**
```bash
redis-server
```

**7. Start the backend**
```bash
uvicorn app.main:app --reload
```

**8. Open API docs**
```
http://localhost:8000/docs
```

---

## 🔐 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/streambill
JWT_SECRET_KEY=your_super_secret_key_here
REDIS_URL=redis://localhost:6379/0
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=your_razorpay_secret
ALGORITHM=HS256
```

---

## 📡 API Modules

| Module | Description |
|---|---|
| **Authentication** | Register, login, JWT token management |
| **Organizations** | Multi-tenant org management |
| **API Keys** | Generate and validate API keys per org |
| **Customers** | Customer CRUD with external ID support |
| **Products** | Product catalog management |
| **Pricing Tiers** | Graduated pricing tier configuration |
| **Usage Events** | Idempotent event ingestion via Redis Streams |
| **Invoice Generation** | Automated billing and invoice creation |
| **Payments** | Razorpay order creation and verification |

**Swagger UI available at:**
```
http://localhost:8000/docs
```

---

## 💳 Billing Flow

```
  Customer makes API call
          │
          ▼
  ┌───────────────┐
  │  Usage Event  │  POST /events/ingest
  └───────┬───────┘  (idempotency key required)
          │
          ▼
  ┌───────────────┐
  │ Redis Stream  │  XADD — non-blocking, < 5ms
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │    Worker     │  XREADGROUP consumer group
  └───────┬───────┘
          │
          ▼
  ┌───────────────────┐
  │ Usage Events Table│  Append-only ledger
  └───────┬───────────┘
          │
          ▼
  ┌───────────────────┐
  │Invoice Generation │  Graduated tier calculation
  └───────┬───────────┘
          │
          ▼
  ┌───────────────┐
  │Razorpay Order │  Payment link created
  └───────┬───────┘
          │
          ▼
  ┌──────────────────────┐
  │ Payment Verification │  Webhook / manual verify
  └───────┬──────────────┘
          │
          ▼
  ┌───────────────┐
  │ Invoice: PAID │  ✅ Done
  └───────────────┘
```

---

## 🔮 Future Enhancements

<table>
<tr>
<td width="50%">

**Frontend & UX**
- ☐ React Dashboard
- ☐ Customer Portal
- ☐ PDF Invoice Export

**Backend**
- ☐ Email Service
- ☐ Celery Tasks
- ☐ Scheduled Billing
- ☐ Subscription Billing

</td>
<td width="50%">

**Infrastructure**
- ☐ Docker Deployment
- ☐ AWS ECS
- ☐ CI/CD Pipeline

**Observability**
- ☐ Monitoring
- ☐ Audit Logs
- ☐ Analytics Dashboard
- ☐ Webhooks

</td>
</tr>
</table>

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Commit your changes
git commit -m "feat: add your feature"

# 4. Push to your branch
git push origin feature/your-feature-name

# 5. Open a Pull Request
```

---

## 📜 License

This project is licensed under the **MIT License** — use it, build on it, learn from it.

---

## 👨‍💻 Author

<div align="center">

**Jayant Dethe**
*Final-year IT Engineer · Backend & AI Systems*

[![GitHub](https://img.shields.io/badge/GitHub-JayantDethe26-181717?style=flat-square&logo=github)](https://github.com/JayantDethe26)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/jayant-dethe-728a0726a)

</div>

---

<div align="center">

**If this project helped you understand billing systems, drop a ⭐**

*Built with obsessive attention to backend engineering detail*

</div>
