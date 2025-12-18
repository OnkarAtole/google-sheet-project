

# 📊 Google Sheet Data API (FastAPI + Frontend)

A full-stack project that allows you to **add, upload, fetch, and search data in Google Sheets** using a **FastAPI backend** and a **simple frontend UI**.
Designed to be **Render-friendly** (no credentials file uploaded).

---

## 🚀 Features

### Backend (FastAPI)

* Add single product to Google Sheet
* Upload multiple rows (Excel-like data)
* Automatically:

  * Maintain headers
  * Insert new data **before SUM row**
  * Recalculate SUM
  * Apply row formatting
* Google Service Account credentials via **ENV (secure)**
* CORS enabled for frontend

### Frontend

* Simple HTML + JS UI
* Add product form
* Fetch & display sheet data
* Search/filter table rows
* Connects directly to FastAPI backend

---

## 🧰 Tech Stack

### Backend

* FastAPI
* gspread
* Google Sheets API
* Python 3.10+
* Render (deployment)

### Frontend

* HTML
* CSS
* JavaScript (Fetch API)

---

## 📁 Project Structure

```
google-sheet-project/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── README.md
```

---

## ⚙️ Backend Setup (Developer)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/OnkarAtole/google-sheet-project.git
cd google-sheet-project/backend
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

#### Activate

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

### Create `.env` file

```env
SPREADSHEET_ID=your_google_sheet_id
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

⚠️ **Never upload `Credentials.json` to GitHub**
🔐 Steps to Get Credentials.json

1️⃣ Open Google Cloud Console

👉 https://console.cloud.google.com

2️⃣ Create New Project

Click Select Project → New Project

Project Name: Google-Sheet-API

Click Create

3️⃣ Enable Google Sheets API

Go to APIs & Services → Library

Search Google Sheets API

Click Enable

4️⃣ Create Service Account

Go to APIs & Services → Credentials

Click Create Credentials → Service Account

Fill:

Name: sheet-api-service

Role: Editor

Click Done

5️⃣ Download Credentials.json

Open service account

Go to Keys → Add Key → Create New Key

Select JSON

📥 File downloads automatically

6️⃣ Share Google Sheet

Open your Google Sheet

Click Share

Add service account email

Give Editor access

7️⃣ Convert JSON to ENV (Recommended)

Instead of using file directly, paste entire JSON inside .env:

GOOGLE_SERVICE_ACCOUNT_JSON={...full json...}

Backend code already supports this securely.
---

## ▶️ Run Backend Locally

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger Docs:

```
http://127.0.0.1:8000/docs
```

---

## 🌐 Frontend Setup

### 1️⃣ Open Frontend Folder

```bash
cd ../frontend
```

### 2️⃣ Update API URL in `script.js`

```js
const API_BASE = "http://127.0.0.1:8000";
```

### 3️⃣ Open `index.html`

* Double click
  OR
* Use Live Server (VS Code)

---


---

## ☁️ Deploy Backend on Render

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

### Add Environment Variables on Render

* `SPREADSHEET_ID`
* `GOOGLE_SERVICE_ACCOUNT_JSON`

---

## 🛡️ .gitignore (Important)

```gitignore
venv/
__pycache__/
.env
*.pyc
node_modules/
```
