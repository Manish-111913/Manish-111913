# Invexis Restaurant Management Platform

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![React](https://img.shields.io/badge/React-18-blue?logo=react&logoColor=white)](https://react.dev/)
[![Node.js](https://img.shields.io/badge/Node.js-20.x-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?logo=amazonwebservices&logoColor=white)](https://aws.amazon.com/)

A production-ready, full-stack restaurant management system and ERP workflow engine. Features dynamic table-side QR ordering, automated kitchen order tickets (KOT), real-time inventory tracking with AI-powered OCR invoice parsing, FIFO stock deduction, and billing automation. Developed and deployed as an enterprise internship project.

---

## 🔗 Architecture & Workflow

```
+------------------+       +------------------+       +-------------------+
|  Table QR Code   | ----> | Customer WebApp  | ----> | Kitchen Dashboard |
|  Scanning        |       | (QR Ordering)    |       | (Live KOT)        |
+------------------+       +------------------+       +---------+---------+
                                                                |
+------------------+       +------------------+                 |
| Supplier Invoice | ----> | OCR Invoice Gen  | <---------------+ (Reduces stock
| (Image / PDF)    |       | (Vision+Gemini)  |                 |  using FIFO)
+------------------+       +---------+--------+                 v
                                     |                +---------+---------+
                                     +--------------> | DB (Mongo + PG)   |
                                                      +-------------------+
```

---

## ⚡ Features

- **Dynamic Table-Side QR Ordering**: Instant ordering without application installation. Seamlessly maps orders to specific table IDs and prints live KOTs to kitchen screens.
- **AI-Powered OCR Inventory & Invoice Parsing**: Upload supplier invoices and purchase receipts; Google Vision API and Gemini AI extract items, quantities, and prices to update inventory records.
- **FIFO (First-In, First-Out) Stock Deduction**: Deducts raw ingredients based on recipe mapping and the batch arrival dates to ensure accurate food cost calculations and reduce wastage.
- **Automated Billing & Digital Receipts**: Generates GST/VAT compliant digital receipts with multiple payment gateway integrations.
- **Real-Time Dashboards & Analytics**: Live monitoring of restaurant sales, peak ordering hours, high-margin menu items, and ingredient depletion warnings.
- **Menu Automation**: Disables menu items in real-time when essential raw ingredients are out of stock.

---

## 💻 Tech Stack

- **Frontend**: React, React Router, Tailwind CSS, Recharts (Admin analytics)
- **Backend API**: Node.js, Express.js
- **Databases**: MongoDB (Operational orders & logs), PostgreSQL (Transactional ledgers & Inventory items)
- **Cloud & Media**: Amazon Web Services (AWS S3 for invoices, EC2 for hosting)
- **AI Services**: Google Cloud Vision API (OCR), Google Gemini API (Structured extraction)

---

## 🛠️ Installation & Setup

> [!NOTE]
> Since this is a production-level ERP platform, it requires access to Google Cloud credentials for Vision OCR and AWS credentials for media storage.

### Step 1: Clone the Repository
```bash
git clone https://github.com/Manish-111913/Invexis-Restaurant.git
cd Invexis-Restaurant
```

### Step 2: Configure Server env
1. Navigate to backend:
   ```bash
   cd backend
   ```
2. Create `.env` file:
   ```env
   PORT=5000
   MONGO_URI=mongodb+srv://your_username:password@cluster.mongodb.net/invexis_restaurant
   POSTGRES_URI=postgresql://postgres_user:password@aws-rds-endpoint:5432/invexis_erp
   GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
   GEMINI_API_KEY=your_gemini_api_key
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   AWS_BUCKET_NAME=invexis-receipts-bucket
   JWT_SECRET=your_jwt_signing_secret
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start development server:
   ```bash
   npm run dev
   ```

### Step 3: Configure Client env
1. Navigate to client:
   ```bash
   cd ../client
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the application:
   ```bash
   npm run dev
   ```

---

## 📂 Folder Structure

```
Invexis-Restaurant/
├── backend/
│   ├── src/
│   │   ├── config/         # MongoDB, PG connection, and AWS SDK setup
│   │   ├── controllers/    # Order routing, OCR processing, FIFO logic
│   │   ├── models/         # Multi-database schemas (Mongoose & PG queries)
│   │   ├── services/       # AI parsing & Google Vision helper classes
│   │   └── routes/         # REST API mounts
│   ├── package.json
│   └── server.js
├── client/
│   ├── public/
│   ├── src/
│   │   ├── components/     # POS interface, Kitchen feed, Receipt visualizer
│   │   ├── pages/          # Customer Menu, Manager ERP Dashboard, Analytics
│   │   └── api/            # API client wrapper
│   └── package.json
├── README.md
└── architecture.png
```

---

## 🚀 Future Improvements

- Add a tabletop tablet application utilizing WebRTC to allow customers to live-chat with waitstaff or query an AI recommendation engine.
- Predictive ingredient ordering: Train localized time-series models (Prophet/LSTM) to predict ingredient requirements based on weekly events and historical patterns.

---

## 📄 License

This repository is private-source for internship records, but the template and core layout are licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
