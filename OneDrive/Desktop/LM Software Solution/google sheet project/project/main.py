from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import gspread
from google.oauth2.service_account import Credentials
import os
import json
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()

scope = ["https://www.googleapis.com/auth/spreadsheets"]

# Load JSON from ENV (Render-safe)
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
client = gspread.authorize(creds)

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SHEET_NAME = "page1"

workbook = client.open_by_key(SPREADSHEET_ID)
sheet = workbook.worksheet(SHEET_NAME)

HEADERS = ["Name", "Price", "Quantity"]

# ================= FASTAPI =================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo; restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= MODELS =================
class Product(BaseModel):
    name: str
    price: int
    quantity: int

class ExcelData(BaseModel):
    data: list

# ================= FORMATTING =================
def format_header():
    sheet.update("A1:C1", [HEADERS])
    sheet.format(
        "A1:C1",
        {
            "textFormat": {"bold": True, "fontSize": 12},
            "backgroundColor": {"red": 0.1, "green": 0.7, "blue": 1.0},
            "horizontalAlignment": "CENTER"
        }
    )

def apply_row_formatting():
    rows = sheet.get_all_values()
    if len(rows) < 2:
        return
    for i, row in enumerate(rows[1:], start=2):
        # Skip SUM row
        if row[1].startswith("="):
            continue
        try:
            price = int(row[1])
        except:
            continue
        color = (
            {"red": 0.3, "green": 1.0, "blue": 0.3} if price > 1000 else {"red": 1.0, "green": 0.3, "blue": 0.3}
        )
        sheet.format(f"A{i}:C{i}", {"backgroundColor": color, "wrapStrategy": "WRAP"})

# ================= SUM HANDLING =================
def remove_sum_if_exists():
    rows = sheet.get_all_values()
    sheet.delete_rows(len(rows))

def add_sum():
    col_b = sheet.col_values(2)
    if col_b and col_b[0].lower() == "price":
        col_b = col_b[1:]
    last_data_row = len(col_b) + 1
    sheet.update_cell(last_data_row + 1, 2, f"=SUM(B2:B{last_data_row})")

# ================= HELPERS =================
def ensure_header():
    if sheet.row_values(1) != HEADERS:
        format_header()

# ================= APIs =================
@app.post("/add-product")
def add_product(product: Product):
    ensure_header()
    remove_sum_if_exists()
    sheet.append_row([product.name, product.price, product.quantity], value_input_option="USER_ENTERED")
    apply_row_formatting()
    add_sum()
    return {"message": "Product added successfully"}

@app.post("/upload-excel")
def upload_excel(payload: ExcelData):
    ensure_header()
    rows = payload.data
    if rows and rows[0] == HEADERS:
        rows = rows[1:]
    remove_sum_if_exists()
    if rows:
        sheet.append_rows(rows, value_input_option="USER_ENTERED")
    apply_row_formatting()
    add_sum()
    return {"message": "Excel data added successfully"}

@app.get("/fetch")
def fetch_data():
    return sheet.get_all_values()













# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import gspread
# from google.oauth2.service_account import Credentials
# import os

# # ================= AUTH =================
# scope = ["https://www.googleapis.com/auth/spreadsheets"]

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CRED_PATH = os.path.join(BASE_DIR, "Credentials.json")

# creds = Credentials.from_service_account_file(CRED_PATH, scopes=scope)
# client = gspread.authorize(creds)

# # ================= SHEET =================
# SPREADSHEET_ID = "19eR6nnw_YNwqiW3eOzRyD4ot9u1abP28Qut39XAw_5I"
# workbook = client.open_by_key(SPREADSHEET_ID)
# sheet = workbook.worksheet("page1")

# HEADERS = ["Name", "Price", "Quantity"]

# # ================= FASTAPI =================
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ================= MODELS =================
# class Product(BaseModel):
#     name: str
#     price: int
#     quantity: int

# class ExcelData(BaseModel):
#     data: list

# # ================= FORMATTING =================
# def format_header():
#     sheet.format(
#         "A1:C1",
#         {
#             "textFormat": {"bold": True, "fontSize": 12},
#             "backgroundColor": {"red": 0.1, "green": 0.7, "blue": 1.0},
#             "horizontalAlignment": "CENTER"
#         }
#     )
#     sheet.columns_auto_resize(0, 3)


# def apply_row_formatting():
#     rows = sheet.get_all_values()
#     if len(rows) < 2:
#         return

#     last_col = len(rows[0])

#     for i, row in enumerate(rows[1:], start=2):
#         try:
#             price = int(row[1])
#         except:
#             continue

#         color = (
#             {"red": 0.3, "green": 1.0, "blue": 0.3}
#             if price > 1000
#             else {"red": 1.0, "green": 0.3, "blue": 0.3}
#         )

#         sheet.format(
#             f"A{i}:{chr(64 + last_col)}{i}",
#             {
#                 "backgroundColor": color,
#                 "wrapStrategy": "WRAP"
#             }
#         )

# # ================= SUM HANDLING =================
# def remove_sum_if_exists():
#     col_b = sheet.col_values(2)

    
#     sheet.delete_rows(len(col_b))


# def add_sum():
#     col_a = sheet.col_values(1)
#     if col_a and col_a[0].lower() == "name":
#         col_a = col_a[1:]

#     last_data_row = len(col_a) + 1
#     total_row = last_data_row + 1

#     sheet.update_cell(
#         total_row,
#         2,
#         f"=SUM(B2:B{last_data_row})"
#     )

# # ================= HELPERS =================
# def ensure_header():
#     if sheet.row_values(1) != HEADERS:
#         sheet.update("A1:C1", [HEADERS])
#         format_header()

# # ================= APIs =================

# @app.post("/add-product")
# def add_product(product: Product):
#     ensure_header()

#     # 1️⃣ Remove SUM row
#     remove_sum_if_exists()

#     # 2️⃣ Append data
#     sheet.append_row(
#         [product.name, product.price, product.quantity],
#         value_input_option="USER_ENTERED"
#     )

#     # 3️⃣ Re-add SUM + formatting
#     apply_row_formatting()
#     add_sum()

#     return {"message": "Product added successfully"}


# @app.post("/upload-excel")
# def upload_excel(payload: ExcelData):
#     ensure_header()

#     rows = payload.data
#     if rows and rows[0] == HEADERS:
#         rows = rows[1:]

#     # 1️⃣ Remove SUM row
#     remove_sum_if_exists()

#     # 2️⃣ Append Excel data
#     if rows:
#         sheet.append_rows(rows, value_input_option="USER_ENTERED")

#     # 3️⃣ Re-add SUM + formatting
#     apply_row_formatting()
#     add_sum()

#     return {"message": "Excel data added successfully"}


# @app.get("/fetch")
# def fetch_data():
#     return sheet.get_all_values()









