#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kanawa Soft - Sistema de Gestão Completo
Versão 1.5 - Todos os Módulos Completos
Desenvolvido por Daniel Wasomba - D.Pedro Soluções
"""

import os
import sys
import sqlite3
import datetime
import hashlib
import json
import shutil
import platform
import subprocess
import uuid
import threading
import time
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

# ==================== CONFIGURAÇÕES ====================
APP_NAME = "Kanawa Soft"
VERSION = "2.0"
DEVELOPER = "Daniel Wasomba"
COMPANY_NAME = "D.Pedro Soluções"

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
DB_FILE = os.path.join(BASE_DIR, "kanawa.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
REPORTS_DIR = os.path.join(BASE_DIR, "relatorios")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

for directory in [BACKUP_DIR, REPORTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

DEFAULT_CURRENCY = "AOA"
DEFAULT_TAX_RATE = 0.14

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_invoice_number():
    return f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

def generate_os_number():
    return f"OS-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

def generate_op_number():
    return f"OP-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

def generate_quote_number():
    return f"QOT-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

def generate_purchase_number():
    return f"PUR-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# ==================== MODELOS ====================
@dataclass
class User:
    id: int = 0
    name: str = ""
    email: str = ""
    password: str = ""
    phone: str = ""
    role: str = "seller"
    avatar: str = ""
    first_login: bool = True
    created_at: str = ""

@dataclass
class Company:
    id: int = 0
    name: str = ""
    nif: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    description: str = ""
    logo_path: str = ""
    currency: str = DEFAULT_CURRENCY
    tax_rate: float = DEFAULT_TAX_RATE
    taxpayer_type: str = "normal"
    level: str = "micro"

@dataclass
class Category:
    id: int = 0
    name: str = ""
    description: str = ""

@dataclass
class Product:
    id: int = 0
    name: str = ""
    code: str = ""
    category_id: int = 0
    price: float = 0.0
    cost: float = 0.0
    stock: float = 0.0
    min_stock: float = 0.0
    unit: str = "UN"
    brand: str = ""
    ncm: str = ""
    tax_exempt: bool = False
    created_at: str = ""

@dataclass
class Client:
    id: int = 0
    name: str = ""
    nif: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    total_purchases: float = 0.0
    purchase_count: int = 0
    last_purchase: str = ""
    type: str = "normal"
    credit_limit: float = 0.0
    created_at: str = ""

@dataclass
class Supplier:
    id: int = 0
    name: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    tax_id: str = ""
    contact_person: str = ""
    created_at: str = ""

@dataclass
class Quote:
    id: int = 0
    number: str = ""
    client_id: int = 0
    client_name: str = ""
    total_amount: float = 0.0
    status: str = "Pendente"
    valid_until: str = ""
    user_id: int = 0
    user_name: str = ""
    created_at: str = ""

@dataclass
class QuoteItem:
    id: int = 0
    quote_id: int = 0
    product_id: int = 0
    product_name: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    total_price: float = 0.0

@dataclass
class Purchase:
    id: int = 0
    number: str = ""
    supplier_id: int = 0
    supplier_name: str = ""
    total_amount: float = 0.0
    payment_method: str = "À vista"
    status: str = "Pendente"
    user_id: int = 0
    user_name: str = ""
    created_at: str = ""

@dataclass
class PurchaseItem:
    id: int = 0
    purchase_id: int = 0
    product_id: int = 0
    product_name: str = ""
    quantity: float = 0.0
    unit_cost: float = 0.0
    total_cost: float = 0.0

@dataclass
class Sale:
    id: int = 0
    invoice_number: str = ""
    client_id: int = 0
    subtotal: float = 0.0
    discount: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    payment_method: str = "Dinheiro"
    status: str = "completed"
    user_id: int = 0
    user_name: str = ""
    created_at: str = ""
    profit: float = 0.0

@dataclass
class SaleItem:
    id: int = 0
    sale_id: int = 0
    product_id: int = 0
    product_name: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    total_price: float = 0.0

@dataclass
class StockMovement:
    id: int = 0
    product_id: int = 0
    product_name: str = ""
    type: str = ""
    quantity: float = 0.0
    old_stock: float = 0.0
    new_stock: float = 0.0
    reason: str = ""
    user_id: int = 0
    user_name: str = ""
    created_at: str = ""

@dataclass
class ProductionOrder:
    id: int = 0
    number: str = ""
    product_id: int = 0
    product_name: str = ""
    quantity: float = 0.0
    status: str = "Planejada"
    start_date: str = ""
    end_date: str = ""
    user_id: int = 0
    user_name: str = ""
    created_at: str = ""

@dataclass
class BillOfMaterial:
    id: int = 0
    product_id: int = 0
    component_id: int = 0
    component_name: str = ""
    quantity: float = 0.0

@dataclass
class Transaction:
    id: int = 0
    type: str = ""
    category: str = ""
    description: str = ""
    amount: float = 0.0
    payment_method: str = ""
    status: str = "Pendente"
    due_date: str = ""
    paid_date: str = ""
    user_id: int = 0
    user_name: str = ""
    created_at: str = ""

@dataclass
class Expense:
    id: int = 0
    category: str = ""
    description: str = ""
    amount: float = 0.0
    due_date: str = ""
    paid: bool = False
    paid_date: str = ""
    user_id: int = 0
    user_name: str = ""
    created_at: str = ""

@dataclass
class Return:
    id: int = 0
    sale_id: int = 0
    invoice_number: str = ""
    client_id: int = 0
    client_name: str = ""
    total_amount: float = 0.0
    reason: str = ""
    status: str = "Pendente"
    user_id: int = 0
    user_name: str = ""
    created_at: str = ""

@dataclass
class ReturnItem:
    id: int = 0
    return_id: int = 0
    product_id: int = 0
    product_name: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    total_price: float = 0.0

@dataclass
class SellerLimit:
    id: int = 0
    seller_id: int = 0
    seller_name: str = ""
    daily_limit: float = 50000.0
    monthly_limit: float = 200000.0
    current_daily_sales: float = 0.0
    current_monthly_sales: float = 0.0
    last_reset_date: str = ""

@dataclass
class PDVSession:
    id: int = 0
    user_id: int = 0
    user_name: str = ""
    opening_date: str = ""
    opening_balance: float = 0.0
    status: str = "Aberto"
    closing_date: str = ""
    closing_balance: float = 0.0
    total_sales: float = 0.0
    notes: str = ""



# ==================== BANCO DE DADOS ====================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.current_user = None
        self.create_tables()

    def create_tables(self):
        # Empresas
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY, name TEXT, nif TEXT, phone TEXT, email TEXT,
            address TEXT, description TEXT, logo_path TEXT, currency TEXT DEFAULT 'AOA',
            tax_rate REAL DEFAULT 0.14, taxpayer_type TEXT DEFAULT 'normal',
            level TEXT DEFAULT 'micro'
        )''')

        # Usuários
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT,
            phone TEXT, role TEXT, avatar TEXT, first_login INTEGER, created_at TIMESTAMP
        )''')

        # Permissões
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY, role TEXT, module TEXT,
            can_view INTEGER DEFAULT 0, can_create INTEGER DEFAULT 0,
            can_edit INTEGER DEFAULT 0, can_delete INTEGER DEFAULT 0
        )''')

        # Categorias
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY, name TEXT UNIQUE, description TEXT
        )''')

        # Produtos
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY, name TEXT, code TEXT UNIQUE, category_id INTEGER,
            price REAL, cost REAL, stock REAL, min_stock REAL, unit TEXT,
            brand TEXT, ncm TEXT, tax_exempt INTEGER, created_at TIMESTAMP
        )''')

        # Clientes
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY, name TEXT, nif TEXT, phone TEXT, email TEXT,
            address TEXT, total_purchases REAL, purchase_count INTEGER,
            last_purchase TIMESTAMP, type TEXT, credit_limit REAL, created_at TIMESTAMP
        )''')

        # Fornecedores
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT,
            address TEXT, tax_id TEXT, contact_person TEXT, created_at TIMESTAMP
        )''')

        # Vendas
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY, invoice_number TEXT UNIQUE, client_id INTEGER,
            subtotal REAL, discount REAL, tax REAL, total REAL,
            payment_method TEXT, status TEXT, user_id INTEGER, user_name TEXT,
            profit REAL, created_at TIMESTAMP
        )''')

        # Itens de venda
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY, sale_id INTEGER, product_id INTEGER,
            product_name TEXT, quantity REAL, unit_price REAL, total_price REAL
        )''')

        # Orçamentos
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY, number TEXT UNIQUE, client_id INTEGER,
            client_name TEXT, total_amount REAL, status TEXT,
            valid_until TEXT, user_id INTEGER, user_name TEXT, created_at TIMESTAMP
        )''')

        # Itens de orçamento
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS quote_items (
            id INTEGER PRIMARY KEY, quote_id INTEGER, product_id INTEGER,
            product_name TEXT, quantity REAL, unit_price REAL, total_price REAL
        )''')

        # Compras
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY, number TEXT UNIQUE, supplier_id INTEGER,
            supplier_name TEXT, total_amount REAL, payment_method TEXT,
            status TEXT, user_id INTEGER, user_name TEXT, created_at TIMESTAMP
        )''')

        # Itens de compra
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY, purchase_id INTEGER, product_id INTEGER,
            product_name TEXT, quantity REAL, unit_cost REAL, total_cost REAL
        )''')

        # Devoluções
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS returns (
            id INTEGER PRIMARY KEY, sale_id INTEGER, invoice_number TEXT,
            client_id INTEGER, client_name TEXT, total_amount REAL,
            reason TEXT, status TEXT, user_id INTEGER, user_name TEXT,
            created_at TIMESTAMP
        )''')

        # Itens de devolução
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS return_items (
            id INTEGER PRIMARY KEY, return_id INTEGER, product_id INTEGER,
            product_name TEXT, quantity REAL, unit_price REAL, total_price REAL
        )''')

        # Movimentações de estoque
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY, product_id INTEGER, product_name TEXT,
            type TEXT, quantity REAL, old_stock REAL, new_stock REAL,
            reason TEXT, user_id INTEGER, user_name TEXT, created_at TIMESTAMP
        )''')

        # Ordens de produção
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS production_orders (
            id INTEGER PRIMARY KEY, number TEXT UNIQUE, product_id INTEGER,
            product_name TEXT, quantity REAL, status TEXT,
            start_date TEXT, end_date TEXT, user_id INTEGER, user_name TEXT,
            created_at TIMESTAMP
        )''')

        # Lista de materiais
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bill_of_materials (
            id INTEGER PRIMARY KEY, product_id INTEGER, component_id INTEGER, quantity REAL
        )''')

        # Transações financeiras
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY, type TEXT, category TEXT, description TEXT,
            amount REAL, payment_method TEXT, status TEXT, due_date TEXT,
            paid_date TEXT, user_id INTEGER, user_name TEXT, created_at TIMESTAMP
        )''')

        # Despesas
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY, category TEXT, description TEXT, amount REAL,
            due_date TEXT, paid INTEGER, paid_date TEXT,
            user_id INTEGER, user_name TEXT, created_at TIMESTAMP
        )''')

        # Atividades
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY, type TEXT, description TEXT, details TEXT,
            user_id INTEGER, user_name TEXT, created_at TIMESTAMP
        )''')

        # Limites de vendedores
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS seller_limits (
            id INTEGER PRIMARY KEY, seller_id INTEGER, seller_name TEXT,
            daily_limit REAL, monthly_limit REAL,
            current_daily_sales REAL, current_monthly_sales REAL,
            last_reset_date TEXT
        )''')

        # Sessões PDV
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pdv_sessions (
            id INTEGER PRIMARY KEY, user_id INTEGER, user_name TEXT,
            opening_date TIMESTAMP, opening_balance REAL, status TEXT,
            closing_date TIMESTAMP, closing_balance REAL,
            total_sales REAL, notes TEXT
        )''')

        self.conn.commit()

        # Criar admin padrão
        self.cursor.execute("SELECT * FROM users WHERE email='admin@kanawa.com'")
        if not self.cursor.fetchone():
            now = datetime.datetime.now().isoformat()
            self.cursor.execute('''INSERT INTO users (name, email, password, phone,
                role, first_login, created_at) VALUES (?,?,?,?,?,?,?)''',
                ('Administrador', 'admin@kanawa.com', hash_password('admin123'),
                 '900000000', 'admin', 0, now))
            self.conn.commit()

        # Criar categorias padrão
        for cat in ['Geral', 'Alimentos', 'Bebidas', 'Limpeza', 'Eletrônicos',
                    'Roupas', 'Calçados', 'Papelaria', 'Móveis', 'Cosméticos']:
            self.cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))
        self.conn.commit()

        # Criar permissões padrão
        self.create_default_permissions()

    def create_default_permissions(self):
        permissions = [
            ('admin', 'all', 1, 1, 1, 1),
            ('manager', 'products', 1, 1, 1, 0),
            ('manager', 'clients', 1, 1, 1, 0),
            ('manager', 'sales', 1, 1, 1, 0),
            ('seller', 'sales', 1, 1, 0, 0),
            ('seller', 'clients', 1, 1, 0, 0),
            ('stock', 'products', 1, 1, 1, 0),
            ('stock', 'stock', 1, 1, 1, 0),
        ]
        for role, module, view, create, edit, delete in permissions:
            self.cursor.execute('''INSERT OR IGNORE INTO permissions
                (role, module, can_view, can_create, can_edit, can_delete)
                VALUES (?,?,?,?,?,?)''', (role, module, view, create, edit, delete))
        self.conn.commit()

    # ========== MÉTODOS AUXILIARES ==========
    def get_categories(self):
        rows = self.cursor.execute("SELECT * FROM categories ORDER BY name").fetchall()
        return [Category(**{k: row[k] for k in row.keys()}) for row in rows]

    def update_category(self, category):
        self.cursor.execute("UPDATE categories SET name=?, description=? WHERE id=?",
                           (category.name, category.description, category.id))
        self.conn.commit()

    def delete_category(self, category_id):
        self.cursor.execute("DELETE FROM categories WHERE id=?", (category_id,))
        self.conn.commit()

    def get_sales_by_client(self, client_id):
        rows = self.cursor.execute(
            "SELECT * FROM sales WHERE client_id=? ORDER BY created_at DESC",
            (client_id,)).fetchall()
        return [Sale(**{k: row[k] for k in row.keys()}) for row in rows]

    # ========== MÉTODOS PRINCIPAIS ==========
    def get_company(self):
        row = self.cursor.execute("SELECT * FROM companies LIMIT 1").fetchone()
        return Company(**{k: row[k] for k in row.keys()}) if row else None

    def update_company(self, company):
        self.cursor.execute('''UPDATE companies SET name=?, nif=?, phone=?, email=?,
            address=?, description=?, currency=?, tax_rate=?, level=? WHERE id=?''',
            (company.name, company.nif, company.phone, company.email, company.address,
             company.description, company.currency, company.tax_rate, company.level, company.id))
        self.conn.commit()

    def create_company(self, company):
        cur = self.cursor.execute('''INSERT INTO companies (name, nif, phone, email,
            address, description, currency, tax_rate, level) VALUES (?,?,?,?,?,?,?,?,?)''',
            (company.name, company.nif, company.phone, company.email, company.address,
             company.description, company.currency, company.tax_rate, company.level))
        self.conn.commit()
        company.id = cur.lastrowid
        return company

    def authenticate_user(self, email, password):
        row = self.cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, hash_password(password))
        ).fetchone()
        if row:
            user = User(**{k: row[k] for k in row.keys()})
            user.password = password
            return user
        return None

    def get_user_by_id(self, uid):
        row = self.cursor.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
        return User(**{k: row[k] for k in row.keys()}) if row else None

    def get_users(self):
        rows = self.cursor.execute("SELECT * FROM users ORDER BY name").fetchall()
        return [User(**{k: row[k] for k in row.keys()}) for row in rows]

    def create_user(self, user):
        hashed = hash_password(user.password)
        cur = self.cursor.execute('''INSERT INTO users (name, email, password, phone,
            role, first_login, created_at) VALUES (?,?,?,?,?,?,?)''',
            (user.name, user.email, hashed, user.phone, user.role,
             1 if user.first_login else 0, datetime.datetime.now().isoformat()))
        self.conn.commit()
        user.id = cur.lastrowid
        return user

    def update_user(self, user):
        if user.password and not user.password.startswith('sha256'):
            user.password = hash_password(user.password)
        self.cursor.execute('''UPDATE users SET name=?, email=?, password=?, phone=?,
            role=?, first_login=? WHERE id=?''',
            (user.name, user.email, user.password, user.phone, user.role,
             1 if user.first_login else 0, user.id))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    # ========== PRODUTOS ==========
    def get_products(self):
        rows = self.cursor.execute("SELECT * FROM products ORDER BY name").fetchall()
        return [Product(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_product_by_id(self, pid):
        row = self.cursor.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        return Product(**{k: row[k] for k in row.keys()}) if row else None

    def get_product_by_code(self, code):
        row = self.cursor.execute("SELECT * FROM products WHERE code=?", (code,)).fetchone()
        return Product(**{k: row[k] for k in row.keys()}) if row else None

    def get_category_by_id(self, cat_id):
        row = self.cursor.execute("SELECT * FROM categories WHERE id=?", (cat_id,)).fetchone()
        return Category(**{k: row[k] for k in row.keys()}) if row else None

    def get_category_by_name(self, name):
        row = self.cursor.execute("SELECT * FROM categories WHERE name=?", (name,)).fetchone()
        return Category(**{k: row[k] for k in row.keys()}) if row else None

    def create_category(self, name, description=""):
        cur = self.cursor.execute(
            "INSERT INTO categories (name, description) VALUES (?,?)",
            (name, description))
        self.conn.commit()
        return Category(id=cur.lastrowid, name=name, description=description)

    def create_product(self, product):
        cur = self.cursor.execute('''INSERT INTO products (name, code, category_id,
            price, cost, stock, min_stock, unit, brand, ncm, tax_exempt, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (product.name, product.code, product.category_id, product.price,
             product.cost, product.stock, product.min_stock, product.unit,
             product.brand, product.ncm, int(product.tax_exempt),
             datetime.datetime.now().isoformat()))
        self.conn.commit()
        product.id = cur.lastrowid
        return product

    def update_product(self, product):
        self.cursor.execute('''UPDATE products SET name=?, code=?, category_id=?,
            price=?, cost=?, stock=?, min_stock=?, unit=?, brand=?, ncm=?,
            tax_exempt=? WHERE id=?''',
            (product.name, product.code, product.category_id, product.price,
             product.cost, product.stock, product.min_stock, product.unit,
             product.brand, product.ncm, int(product.tax_exempt), product.id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()

    def update_product_stock(self, product_id, delta, reason=None):
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        old_stock = product.stock
        new_stock = old_stock + delta
        if new_stock < 0:
            return False
        product.stock = new_stock
        self.update_product(product)
        self.cursor.execute('''INSERT INTO stock_movements (product_id, product_name,
            type, quantity, old_stock, new_stock, reason, user_id, user_name, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (product_id, product.name, 'entrada' if delta > 0 else 'saida',
             abs(delta), old_stock, new_stock, reason,
             self.current_user.id if self.current_user else 0,
             self.current_user.name if self.current_user else 'system',
             datetime.datetime.now().isoformat()))
        self.conn.commit()
        return True

    def get_products_low_stock(self):
        rows = self.cursor.execute(
            "SELECT * FROM products WHERE stock <= min_stock ORDER BY name"
        ).fetchall()
        return [Product(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_stock_movements(self, product_id=None, limit=100):
        if product_id:
            rows = self.cursor.execute(
                "SELECT * FROM stock_movements WHERE product_id=? ORDER BY created_at DESC LIMIT ?",
                (product_id, limit)).fetchall()
        else:
            rows = self.cursor.execute(
                "SELECT * FROM stock_movements ORDER BY created_at DESC LIMIT ?",
                (limit,)).fetchall()
        return [StockMovement(**{k: row[k] for k in row.keys()}) for row in rows]

    # ========== CLIENTES ==========
    def get_clients(self):
        rows = self.cursor.execute("SELECT * FROM clients ORDER BY name").fetchall()
        return [Client(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_client_by_id(self, cid):
        row = self.cursor.execute("SELECT * FROM clients WHERE id=?", (cid,)).fetchone()
        return Client(**{k: row[k] for k in row.keys()}) if row else None

    def get_vip_clients(self):
        rows = self.cursor.execute(
            "SELECT * FROM clients WHERE type='vip' ORDER BY total_purchases DESC"
        ).fetchall()
        return [Client(**{k: row[k] for k in row.keys()}) for row in rows]

    def create_client(self, client):
        cur = self.cursor.execute('''INSERT INTO clients (name, nif, phone, email,
            address, total_purchases, purchase_count, last_purchase, type,
            credit_limit, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            (client.name, client.nif, client.phone, client.email, client.address,
             client.total_purchases, client.purchase_count, client.last_purchase,
             client.type, client.credit_limit, datetime.datetime.now().isoformat()))
        self.conn.commit()
        client.id = cur.lastrowid
        return client

    def update_client(self, client):
        self.cursor.execute('''UPDATE clients SET name=?, nif=?, phone=?, email=?,
            address=?, total_purchases=?, purchase_count=?, last_purchase=?,
            type=?, credit_limit=? WHERE id=?''',
            (client.name, client.nif, client.phone, client.email, client.address,
             client.total_purchases, client.purchase_count, client.last_purchase,
             client.type, client.credit_limit, client.id))
        self.conn.commit()

    def delete_client(self, client_id):
        self.cursor.execute("DELETE FROM clients WHERE id=?", (client_id,))
        self.conn.commit()

    # ========== FORNECEDORES ==========
    def get_suppliers(self):
        rows = self.cursor.execute("SELECT * FROM suppliers ORDER BY name").fetchall()
        return [Supplier(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_supplier_by_id(self, sid):
        row = self.cursor.execute("SELECT * FROM suppliers WHERE id=?", (sid,)).fetchone()
        return Supplier(**{k: row[k] for k in row.keys()}) if row else None

    def create_supplier(self, supplier):
        cur = self.cursor.execute('''INSERT INTO suppliers (name, phone, email,
            address, tax_id, contact_person, created_at) VALUES (?,?,?,?,?,?,?)''',
            (supplier.name, supplier.phone, supplier.email, supplier.address,
             supplier.tax_id, supplier.contact_person, datetime.datetime.now().isoformat()))
        self.conn.commit()
        supplier.id = cur.lastrowid
        return supplier

    def update_supplier(self, supplier):
        self.cursor.execute('''UPDATE suppliers SET name=?, phone=?, email=?,
            address=?, tax_id=?, contact_person=? WHERE id=?''',
            (supplier.name, supplier.phone, supplier.email, supplier.address,
             supplier.tax_id, supplier.contact_person, supplier.id))
        self.conn.commit()

    def delete_supplier(self, supplier_id):
        self.cursor.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
        self.conn.commit()

    # ========== VENDAS ==========
    def get_sales(self):
        rows = self.cursor.execute("SELECT * FROM sales ORDER BY created_at DESC").fetchall()
        return [Sale(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_sale_by_id(self, sale_id):
        row = self.cursor.execute("SELECT * FROM sales WHERE id=?", (sale_id,)).fetchone()
        return Sale(**{k: row[k] for k in row.keys()}) if row else None

    def get_sales_by_period(self, start_date, end_date):
        rows = self.cursor.execute(
            "SELECT * FROM sales WHERE date(created_at) BETWEEN ? AND ? ORDER BY created_at",
            (start_date, end_date)).fetchall()
        return [Sale(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_sales_today(self):
        today = datetime.date.today().isoformat()
        rows = self.cursor.execute(
            "SELECT * FROM sales WHERE date(created_at)=?", (today,)).fetchall()
        return [Sale(**{k: row[k] for k in row.keys()}) for row in rows]

    def create_sale(self, sale):
        cur = self.cursor.execute('''INSERT INTO sales (invoice_number, client_id,
            subtotal, discount, tax, total, payment_method, status,
            user_id, user_name, profit, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (sale.invoice_number, sale.client_id, sale.subtotal, sale.discount,
             sale.tax, sale.total, sale.payment_method, sale.status,
             sale.user_id, sale.user_name, sale.profit,
             datetime.datetime.now().isoformat()))
        self.conn.commit()
        sale.id = cur.lastrowid
        return sale

    def create_sale_item(self, item):
        self.cursor.execute('''INSERT INTO sale_items (sale_id, product_id,
            product_name, quantity, unit_price, total_price) VALUES (?,?,?,?,?,?)''',
            (item.sale_id, item.product_id, item.product_name,
             item.quantity, item.unit_price, item.total_price))
        self.conn.commit()

    def get_sale_items(self, sale_id):
        rows = self.cursor.execute(
            "SELECT * FROM sale_items WHERE sale_id=?", (sale_id,)).fetchall()
        return [SaleItem(**{k: row[k] for k in row.keys()}) for row in rows]

    def process_sale(self, sale, items_list):
        subtotal = sum(item.total_price for item in items_list)
        discount = sale.discount
        company = self.get_company()
        tax_rate = company.tax_rate if company else 0
        tax = (subtotal - discount) * tax_rate
        total = (subtotal - discount) + tax

        sale.subtotal = subtotal
        sale.tax = tax
        sale.total = total
        sale = self.create_sale(sale)

        profit = 0
        for item in items_list:
            item.sale_id = sale.id
            self.create_sale_item(item)
            product = self.get_product_by_id(item.product_id)
            if product:
                profit += (item.unit_price - product.cost) * item.quantity
                self.update_product_stock(item.product_id, -item.quantity,
                                         reason=f"Venda #{sale.invoice_number}")

        self.cursor.execute("UPDATE sales SET profit=? WHERE id=?", (profit, sale.id))
        self.conn.commit()
        self.create_activity("sale", f"Venda #{sale.invoice_number} realizada",
                            f"Valor: {sale.total:.2f}")
        return sale

    # ========== COMPRAS ==========
    def get_purchases(self):
        rows = self.cursor.execute("SELECT * FROM purchases ORDER BY created_at DESC").fetchall()
        return [Purchase(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_purchase_by_id(self, purchase_id):
        row = self.cursor.execute("SELECT * FROM purchases WHERE id=?", (purchase_id,)).fetchone()
        return Purchase(**{k: row[k] for k in row.keys()}) if row else None

    def create_purchase(self, purchase):
        cur = self.cursor.execute('''INSERT INTO purchases (number, supplier_id,
            supplier_name, total_amount, payment_method, status, user_id, user_name, created_at)
            VALUES (?,?,?,?,?,?,?,?,?)''',
            (purchase.number, purchase.supplier_id, purchase.supplier_name,
             purchase.total_amount, purchase.payment_method, purchase.status,
             purchase.user_id, purchase.user_name, datetime.datetime.now().isoformat()))
        self.conn.commit()
        purchase.id = cur.lastrowid
        return purchase

    def create_purchase_item(self, item):
        self.cursor.execute('''INSERT INTO purchase_items (purchase_id, product_id,
            product_name, quantity, unit_cost, total_cost) VALUES (?,?,?,?,?,?)''',
            (item.purchase_id, item.product_id, item.product_name,
             item.quantity, item.unit_cost, item.total_cost))
        self.conn.commit()

    def get_purchase_items(self, purchase_id):
        rows = self.cursor.execute(
            "SELECT * FROM purchase_items WHERE purchase_id=?", (purchase_id,)).fetchall()
        return [PurchaseItem(**{k: row[k] for k in row.keys()}) for row in rows]

    def process_purchase(self, purchase, items_list):
        purchase = self.create_purchase(purchase)
        for item in items_list:
            item.purchase_id = purchase.id
            self.create_purchase_item(item)
            self.update_product_stock(item.product_id, item.quantity,
                                     reason=f"Compra #{purchase.number}")
        self.create_activity("purchase", f"Compra #{purchase.number} realizada",
                            f"Valor: {purchase.total_amount:.2f}")
        return purchase

    # ========== ORÇAMENTOS ==========
    def get_quotes(self, status=None):
        if status:
            rows = self.cursor.execute(
                "SELECT * FROM quotes WHERE status=? ORDER BY created_at DESC",
                (status,)).fetchall()
        else:
            rows = self.cursor.execute("SELECT * FROM quotes ORDER BY created_at DESC").fetchall()
        return [Quote(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_quote_by_id(self, quote_id):
        row = self.cursor.execute("SELECT * FROM quotes WHERE id=?", (quote_id,)).fetchone()
        return Quote(**{k: row[k] for k in row.keys()}) if row else None

    def get_quote_items(self, quote_id):
        rows = self.cursor.execute(
            "SELECT * FROM quote_items WHERE quote_id=?", (quote_id,)).fetchall()
        return [QuoteItem(**{k: row[k] for k in row.keys()}) for row in rows]

    def create_quote(self, quote):
        cur = self.cursor.execute('''INSERT INTO quotes (number, client_id, client_name,
            total_amount, status, valid_until, user_id, user_name, created_at)
            VALUES (?,?,?,?,?,?,?,?,?)''',
            (quote.number, quote.client_id, quote.client_name, quote.total_amount,
             quote.status, quote.valid_until, quote.user_id, quote.user_name,
             datetime.datetime.now().isoformat()))
        self.conn.commit()
        quote.id = cur.lastrowid
        return quote

    def create_quote_item(self, item):
        self.cursor.execute('''INSERT INTO quote_items (quote_id, product_id,
            product_name, quantity, unit_price, total_price) VALUES (?,?,?,?,?,?)''',
            (item.quote_id, item.product_id, item.product_name,
             item.quantity, item.unit_price, item.total_price))
        self.conn.commit()

    def update_quote_status(self, quote_id, status):
        self.cursor.execute("UPDATE quotes SET status=? WHERE id=?", (status, quote_id))
        self.conn.commit()

    def convert_quote_to_sale(self, quote_id):
        quote = self.get_quote_by_id(quote_id)
        if not quote or quote.status != "Aprovado":
            return None

        sale = Sale(
            invoice_number=generate_invoice_number(),
            client_id=quote.client_id,
            payment_method="Dinheiro",
            status="completed",
            user_id=self.current_user.id if self.current_user else 0,
            user_name=self.current_user.name if self.current_user else "system"
        )

        items = self.get_quote_items(quote_id)
        sale_items = []
        for item in items:
            sale_items.append(SaleItem(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            ))

        return self.process_sale(sale, sale_items)

    # ========== DEVOLUÇÕES ==========
    def get_returns(self):
        rows = self.cursor.execute("SELECT * FROM returns ORDER BY created_at DESC").fetchall()
        return [Return(**{k: row[k] for k in row.keys()}) for row in rows]

    def create_return(self, return_obj):
        cur = self.cursor.execute('''INSERT INTO returns (sale_id, invoice_number,
            client_id, client_name, total_amount, reason, status, user_id, user_name, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (return_obj.sale_id, return_obj.invoice_number, return_obj.client_id,
             return_obj.client_name, return_obj.total_amount, return_obj.reason,
             return_obj.status, return_obj.user_id, return_obj.user_name,
             datetime.datetime.now().isoformat()))
        self.conn.commit()
        return_obj.id = cur.lastrowid
        return return_obj

    def create_return_item(self, item):
        self.cursor.execute('''INSERT INTO return_items (return_id, product_id,
            product_name, quantity, unit_price, total_price) VALUES (?,?,?,?,?,?)''',
            (item.return_id, item.product_id, item.product_name,
             item.quantity, item.unit_price, item.total_price))
        self.conn.commit()

    def process_return(self, return_obj, items_list):
        return_obj = self.create_return(return_obj)
        for item in items_list:
            item.return_id = return_obj.id
            self.create_return_item(item)
            self.update_product_stock(item.product_id, item.quantity,
                                     reason=f"Devolução da venda #{return_obj.invoice_number}")
        self.create_activity("return", f"Devolução da venda #{return_obj.invoice_number}",
                            f"Valor: {return_obj.total_amount:.2f}")
        return return_obj

    # ========== PRODUÇÃO E MRP ==========
    def get_production_orders(self):
        rows = self.cursor.execute("SELECT * FROM production_orders ORDER BY created_at DESC").fetchall()
        return [ProductionOrder(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_production_order_by_id(self, po_id):
        row = self.cursor.execute("SELECT * FROM production_orders WHERE id=?", (po_id,)).fetchone()
        return ProductionOrder(**{k: row[k] for k in row.keys()}) if row else None

    def create_production_order(self, po):
        cur = self.cursor.execute('''INSERT INTO production_orders (number, product_id,
            product_name, quantity, status, start_date, end_date, user_id, user_name, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (po.number, po.product_id, po.product_name, po.quantity, po.status,
             po.start_date, po.end_date, po.user_id, po.user_name,
             datetime.datetime.now().isoformat()))
        self.conn.commit()
        po.id = cur.lastrowid
        self.create_activity("production", f"Ordem de Produção #{po.number} criada",
                            f"Produto: {po.product_name} | Quantidade: {po.quantity}")
        return po

    def update_production_order_status(self, po_id, status, end_date=None):
        if status == "Concluída" and not end_date:
            end_date = datetime.date.today().isoformat()
        self.cursor.execute(
            "UPDATE production_orders SET status=?, end_date=? WHERE id=?",
            (status, end_date, po_id))
        self.conn.commit()

        po = self.get_production_order_by_id(po_id)
        if po and status == "Concluída":
            self.update_product_stock(po.product_id, po.quantity,
                                     reason=f"Produção concluída - OP #{po.number}")

    # ========== BOM ==========
    def get_bom_by_product_id(self, product_id):
        rows = self.cursor.execute(
            """SELECT b.*, p.name as component_name
               FROM bill_of_materials b
               JOIN products p ON b.component_id = p.id
               WHERE b.product_id=?""",
            (product_id,)).fetchall()
        return [BillOfMaterial(
            id=row['id'], product_id=row['product_id'],
            component_id=row['component_id'], component_name=row['component_name'],
            quantity=row['quantity']
        ) for row in rows]

    def add_bom_item(self, bom):
        cur = self.cursor.execute(
            "INSERT INTO bill_of_materials (product_id, component_id, quantity) VALUES (?,?,?)",
            (bom.product_id, bom.component_id, bom.quantity))
        self.conn.commit()
        bom.id = cur.lastrowid
        return bom

    def delete_bom_item(self, bom_id):
        self.cursor.execute("DELETE FROM bill_of_materials WHERE id=?", (bom_id,))
        self.conn.commit()

    def calculate_mrp(self, product_id, required_quantity):
        product = self.get_product_by_id(product_id)
        if not product:
            return None

        result = {
            'product': product,
            'required': required_quantity,
            'stock': product.stock,
            'to_produce': max(0, required_quantity - product.stock),
            'components': []
        }

        bom = self.get_bom_by_product_id(product_id)
        for bom_item in bom:
            component = self.get_product_by_id(bom_item.component_id)
            if component:
                needed = bom_item.quantity * required_quantity
                result['components'].append({
                    'product': component,
                    'quantity_per_unit': bom_item.quantity,
                    'total_needed': needed,
                    'stock': component.stock,
                    'to_produce': max(0, needed - component.stock)
                })
        return result

    # ========== FINANCEIRO ==========
    def get_transactions(self, trans_type=None, status=None):
        query = "SELECT * FROM transactions"
        params = []
        conditions = []
        if trans_type:
            conditions.append("type=?")
            params.append(trans_type)
        if status:
            conditions.append("status=?")
            params.append(status)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY created_at DESC"
        rows = self.cursor.execute(query, params).fetchall()
        return [Transaction(**{k: row[k] for k in row.keys()}) for row in rows]

    def create_transaction(self, transaction):
        cur = self.cursor.execute('''INSERT INTO transactions (type, category,
            description, amount, payment_method, status, due_date,
            paid_date, user_id, user_name, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            (transaction.type, transaction.category, transaction.description,
             transaction.amount, transaction.payment_method, transaction.status,
             transaction.due_date, transaction.paid_date, transaction.user_id,
             transaction.user_name, datetime.datetime.now().isoformat()))
        self.conn.commit()
        transaction.id = cur.lastrowid
        return transaction

    def get_expenses(self, paid_only=None):
        if paid_only is not None:
            rows = self.cursor.execute(
                "SELECT * FROM expenses WHERE paid=? ORDER BY due_date DESC",
                (1 if paid_only else 0,)).fetchall()
        else:
            rows = self.cursor.execute("SELECT * FROM expenses ORDER BY due_date DESC").fetchall()
        return [Expense(**{k: row[k] for k in row.keys()}) for row in rows]

    def create_expense(self, expense):
        cur = self.cursor.execute('''INSERT INTO expenses (category, description,
            amount, due_date, paid, paid_date, user_id, user_name, created_at)
            VALUES (?,?,?,?,?,?,?,?,?)''',
            (expense.category, expense.description, expense.amount,
             expense.due_date, 1 if expense.paid else 0, expense.paid_date,
             expense.user_id, expense.user_name, datetime.datetime.now().isoformat()))
        self.conn.commit()
        expense.id = cur.lastrowid
        return expense

    def get_financial_summary(self):
        receitas = self.cursor.execute(
            "SELECT COALESCE(SUM(total),0) FROM sales WHERE status='completed'"
        ).fetchone()[0]
        despesas = self.cursor.execute(
            "SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='Saída' AND status='Pago'"
        ).fetchone()[0] if self.table_exists('transactions') else 0
        expenses_paid = self.cursor.execute(
            "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE paid=1"
        ).fetchone()[0] if self.table_exists('expenses') else 0
        total_despesas = despesas + expenses_paid
        return {"receita_total": receitas, "despesa_total": total_despesas,
                "lucro_real": receitas - total_despesas, "saldo_caixa": receitas - total_despesas}

    def table_exists(self, table_name):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return self.cursor.fetchone() is not None

    # ========== VENDEDORES ==========
    def get_sellers(self):
        rows = self.cursor.execute(
            "SELECT * FROM users WHERE role='seller' ORDER BY name"
        ).fetchall()
        return [User(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_seller_limit(self, seller_id):
        row = self.cursor.execute(
            "SELECT * FROM seller_limits WHERE seller_id=?", (seller_id,)).fetchone()
        return SellerLimit(**{k: row[k] for k in row.keys()}) if row else None

    def create_seller_limit(self, seller_id, seller_name, daily_limit=50000, monthly_limit=200000):
        cur = self.cursor.execute('''INSERT INTO seller_limits
            (seller_id, seller_name, daily_limit, monthly_limit,
             current_daily_sales, current_monthly_sales, last_reset_date)
            VALUES (?,?,?,?,?,?,?)''',
            (seller_id, seller_name, daily_limit, monthly_limit,
             0, 0, datetime.date.today().isoformat()))
        self.conn.commit()
        return cur.lastrowid

    def update_seller_limit(self, seller_id, daily_limit, monthly_limit):
        self.cursor.execute(
            "UPDATE seller_limits SET daily_limit=?, monthly_limit=? WHERE seller_id=?",
            (daily_limit, monthly_limit, seller_id))
        self.conn.commit()

    def check_seller_limit(self, seller_id, amount):
        limit = self.get_seller_limit(seller_id)
        if not limit:
            return True, "Sem limite definido"
        today = datetime.date.today().isoformat()
        if limit.last_reset_date != today:
            self.cursor.execute(
                "UPDATE seller_limits SET current_daily_sales=0, last_reset_date=? WHERE seller_id=?",
                (today, seller_id))
            self.conn.commit()
            limit.current_daily_sales = 0
        if limit.current_daily_sales + amount > limit.daily_limit:
            return False, f"Limite diário excedido! Disponível: {limit.daily_limit - limit.current_daily_sales:.2f}"
        if limit.current_monthly_sales + amount > limit.monthly_limit:
            return False, f"Limite mensal excedido! Disponível: {limit.monthly_limit - limit.current_monthly_sales:.2f}"
        return True, "OK"

    def add_seller_sales(self, seller_id, amount):
        self.cursor.execute('''UPDATE seller_limits SET
            current_daily_sales = current_daily_sales + ?,
            current_monthly_sales = current_monthly_sales + ?
            WHERE seller_id = ?''', (amount, amount, seller_id))
        self.conn.commit()

    # ========== SESSÕES PDV ==========
    def get_pdv_sessions(self, user_id=None):
        if user_id:
            rows = self.cursor.execute(
                "SELECT * FROM pdv_sessions WHERE user_id=? ORDER BY opening_date DESC",
                (user_id,)).fetchall()
        else:
            rows = self.cursor.execute("SELECT * FROM pdv_sessions ORDER BY opening_date DESC").fetchall()
        return [PDVSession(**{k: row[k] for k in row.keys()}) for row in rows]

    def get_active_pdv_session(self, user_id):
        row = self.cursor.execute(
            "SELECT * FROM pdv_sessions WHERE user_id=? AND status='Aberto'",
            (user_id,)).fetchone()
        return PDVSession(**{k: row[k] for k in row.keys()}) if row else None

    def open_pdv_session(self, user_id, user_name, opening_balance, notes=""):
        existing = self.get_active_pdv_session(user_id)
        if existing:
            return None
        cur = self.cursor.execute('''INSERT INTO pdv_sessions
            (user_id, user_name, opening_date, opening_balance, status, notes)
            VALUES (?,?,?,?,?,?)''',
            (user_id, user_name, datetime.datetime.now().isoformat(),
             opening_balance, "Aberto", notes))
        self.conn.commit()
        return cur.lastrowid

    def close_pdv_session(self, session_id, closing_balance, total_sales, notes=""):
        self.cursor.execute('''UPDATE pdv_sessions SET
            closing_date=?, closing_balance=?, total_sales=?, status=?, notes=?
            WHERE id=?''',
            (datetime.datetime.now().isoformat(), closing_balance,
             total_sales, "Fechado", notes, session_id))
        self.conn.commit()

    # ========== ATIVIDADES ==========
    def get_activities(self, limit=50):
        rows = self.cursor.execute(
            "SELECT * FROM activities ORDER BY created_at DESC LIMIT ?",
            (limit,)).fetchall()
        return rows

    def create_activity(self, act_type, description, details=""):
        self.cursor.execute('''INSERT INTO activities (type, description,
            details, user_id, user_name, created_at) VALUES (?,?,?,?,?,?)''',
            (act_type, description, details,
             self.current_user.id if self.current_user else 0,
             self.current_user.name if self.current_user else 'system',
             datetime.datetime.now().isoformat()))
        self.conn.commit()

    # ========== BACKUP ==========
    def backup_database(self):
        backup_name = f"kanawa_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        shutil.copy2(DB_FILE, backup_path)
        self.clean_old_backups()
        self.create_activity("backup", f"Backup criado: {backup_name}", "")
        return backup_path

    def clean_old_backups(self, keep=10):
        if not os.path.exists(BACKUP_DIR):
            return
        backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith('kanawa_backup_')])
        for old in backups[:-keep]:
            os.remove(os.path.join(BACKUP_DIR, old))

    def restore_backup(self, backup_path):
        shutil.copy2(backup_path, DB_FILE)
        self.conn.close()
        self.__init__()
        self.create_activity("restore", f"Backup restaurado: {backup_path}", "")
        return True


# ==================== INTERFACE PRINCIPAL ====================

# ==================== CLASSE DE GRÁFICOS ====================
class NativeCharts:
    """Classe para criar gráficos nativos sem bibliotecas externas"""
    
    @staticmethod
    def create_bar_chart(parent, data, title="", x_label="", y_label="", 
                         width=500, height=250, colors=None):
        """
        Cria um gráfico de barras nativo
        
        Args:
            parent: widget pai (Frame, Canvas, etc)
            data: lista de tuplas (label, valor)
            title: título do gráfico
            x_label: rótulo do eixo X
            y_label: rótulo do eixo Y
            width: largura do canvas
            height: altura do canvas
            colors: lista de cores (opcional)
        """
        canvas = tk.Canvas(parent, width=width, height=height, bg='white', 
                          highlightthickness=1, highlightbackground='#e2e8f0')
        canvas.pack(fill='both', expand=True, pady=10)
        
        if not data:
            canvas.create_text(width//2, height//2, text="Sem dados para exibir",
                              font=('Segoe UI', 12), fill='#64748b')
            return canvas
        
        # Configurações do gráfico
        margin_left = 60
        margin_right = 30
        margin_top = 50
        margin_bottom = 50
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom
        
        # Calcular valores máximos
        max_value = max([v for _, v in data]) if data else 1
        if max_value == 0:
            max_value = 1
        
        # Cores padrão
        if colors is None:
            colors = ['#00adb5', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', 
                     '#8b5cf6', '#ec489a', '#06b6d4', '#84cc16', '#f97316']
        
        # Barra de largura
        bar_width = (chart_width / len(data)) * 0.5
        bar_spacing = (chart_width / len(data)) * 0.2
        
        # Desenhar eixos
        canvas.create_line(margin_left, margin_top, margin_left, height - margin_bottom,
                          fill='#334155', width=2)
        canvas.create_line(margin_left, height - margin_bottom, width - margin_right, 
                          height - margin_bottom, fill='#334155', width=2)
        
        # Título
        if title:
            canvas.create_text(width//2, 20, text=title, font=('Segoe UI', 14, 'bold'),
                              fill='#1e293b')
        
        # Rótulo Y
        if y_label:
            canvas.create_text(20, height//2, text=y_label, angle=60,
                              font=('Segoe UI', 12), fill='#64748b')
        
        # Rótulo X
        if x_label:
            canvas.create_text(width//2, height - 10, text=x_label,
                              font=('Segoe UI', 10), fill='#64748b')
        
        # Grid e eixo Y
        num_ticks = 5
        for i in range(num_ticks + 1):
            y = margin_top + (chart_height / num_ticks) * i
            value = max_value * (1 - i / num_ticks)
            canvas.create_line(margin_left - 5, y, width - margin_right, y,
                              fill='#e2e8f0', dash=(4, 4))
            canvas.create_text(margin_left - 10, y, text=f"{value:,.0f}",
                              anchor='e', font=('Segoe UI', 10), fill='#64748b')
        
        # Desenhar barras
        for idx, (label, value) in enumerate(data):
            x = margin_left + idx * (bar_width + bar_spacing) + bar_spacing/2
            bar_height = (value / max_value) * chart_height
            y = height - margin_bottom - bar_height
            
            color = colors[idx % len(colors)]
            
            # Barra com gradiente simulado
            canvas.create_rectangle(x, y, x + bar_width, height - margin_bottom,
                                   fill=color, outline='', width=0)
            
            # Efeito de brilho
            canvas.create_rectangle(x, y, x + bar_width, y + 3,
                                   fill='white', stipple='gray50', outline='')
            
            # Valor no topo da barra
            if value > 0:
                canvas.create_text(x + bar_width/2, y - 5, text=f"{value:,.0f}",
                                  anchor='s', font=('Segoe UI', 20, 'bold'), fill=color)
            
            # Label
            label_text = label[:15] + "..." if len(label) > 15 else label
            canvas.create_text(x + bar_width/2, height - margin_bottom + 15,
                              text=label_text, angle=95, anchor='nw',
                              font=('Segoe UI', 8), fill='#475569')
        
        return canvas
    
    @staticmethod
    def create_horizontal_bar_chart(parent, data, title="", width=250, height=250):
        """
        Cria um gráfico de barras horizontais
        
        Args:
            parent: widget pai
            data: lista de tuplas (label, valor)
            title: título do gráfico
            width: largura
            height: altura
        """
        canvas = tk.Canvas(parent, width=width, height=height, bg='white',
                          highlightthickness=1, highlightbackground='#e2e8f0')
        canvas.pack(fill='both', expand=True, pady=10)
        
        if not data:
            canvas.create_text(width//2, height//2, text="Sem dados para exibir",
                              font=('Segoe UI', 12), fill='#64748b')
            return canvas
        
        # Configurações
        margin_left = 120
        margin_right = 50
        margin_top = 40
        margin_bottom = 30
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom
        
        # Calcular máximo
        max_value = max([v for _, v in data]) if data else 1
        
        # Título
        if title:
            canvas.create_text(width//2, 20, text=title, font=('Segoe UI', 12, 'bold'),
                              fill='#1e293b')
        
        # Altura de cada barra
        bar_height = chart_height / len(data) * 0.7
        bar_spacing = chart_height / len(data) * 0.3
        
        # Desenhar barras
        colors = ['#ef4444', '#f59e0b', '#eab308', '#84cc16', '#10b981', '#06b6d4', '#3b82f6']
        
        for idx, (label, value) in enumerate(data):
            y = margin_top + idx * (bar_height + bar_spacing) + bar_spacing/2
            bar_width = (value / max_value) * chart_width
            
            color = colors[idx % len(colors)]
            
            # Barra
            canvas.create_rectangle(margin_left, y, margin_left + bar_width, y + bar_height,
                                   fill=color, outline='')
            
            # Label
            label_text = label[:20] + "..." if len(label) > 20 else label
            canvas.create_text(margin_left - 5, y + bar_height/2, text=label_text,
                              anchor='e', font=('Segoe UI', 9), fill='#1e293b')
            
            # Valor
            canvas.create_text(margin_left + bar_width + 5, y + bar_height/2,
                              text=f"{value:.0f}", anchor='w',
                              font=('Segoe UI', 9, 'bold'), fill=color)
        
        return canvas
    
    @staticmethod
    def create_trend_line(canvas, points, x_offset, y_offset, color='#00adb5'):
        """Cria uma linha de tendência (média móvel)"""
        if len(points) < 2:
            return
        
        # Calcular média móvel
        window = min(3, len(points))
        smoothed = []
        for i in range(len(points)):
            start = max(0, i - window//2)
            end = min(len(points), i + window//2 + 1)
            avg = sum(points[start:end]) / (end - start)
            smoothed.append(avg)
        
        # Desenhar linha
        for i in range(len(smoothed) - 1):
            canvas.create_line(x_offset[i], y_offset[i],
                              x_offset[i+1], y_offset[i+1],
                              fill=color, width=2, dash=(4, 2))


# ==================== CLASSE DE BARRA DE PROGRESSO ====================
class ProgressOverlay:
    """Overlay de progresso para operações longas"""
    
    def __init__(self, parent, message="Processando..."):
        self.parent = parent
        self.message = message
        self.overlay = None
        self.progress_bar = None
        
    def show(self):
        """Exibe o overlay com barra de progresso"""
        # Criar overlay
        self.overlay = tk.Toplevel(self.parent)
        self.overlay.transient(self.parent)
        self.overlay.grab_set()
        self.overlay.overrideredirect(True)
        
        # Centralizar
        self.parent.update_idletasks()
        x = self.parent.winfo_rootx() + self.parent.winfo_width()//2 - 150
        y = self.parent.winfo_rooty() + self.parent.winfo_height()//2 - 60
        self.overlay.geometry(f"250x150+{x}+{y}")
        
        # Frame com estilo
        frame = tk.Frame(self.overlay, bg='white', relief='solid', bd=1)
        frame.pack(fill='both', expand=True)
        
        # Mensagem
        tk.Label(frame, text=self.message, font=('Segoe UI', 12),
                bg='white', fg='#1e293b').pack(pady=(20, 10))
        
        # Barra de progresso customizada
        style = ttk.Style()
        style.configure("Cyan.Horizontal.TProgressbar",
                       troughcolor='#e2e8f0',
                       background='#00adb5',
                       lightcolor='#00adb5',
                       darkcolor='#00adb5',
                       bordercolor='#00adb5',
                       thickness=12)
        
        self.progress_bar = ttk.Progressbar(frame, style="Cyan.Horizontal.TProgressbar",
                                            mode='indeterminate', length=250)
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)
        
        self.overlay.lift()
        self.overlay.focus_force()
        self.parent.update()
        
    def hide(self):
        """Remove o overlay"""
        if self.progress_bar:
            self.progress_bar.stop()
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None


# ==================== CLASSE DE LOGOTIPO MELHORADO ====================
class LogoDisplay:
    """Exibição melhorada de logo e cabeçalho"""
    
    @staticmethod
    def create_logo(parent, size="large"):
        """Cria um display de logo estilizado"""
        colors = {
            'primary': '#00adb5',
            'secondary': '#1e293b',
            'accent': '#f59e0b'
        }
        
        if size == "large":
            logo_text = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     ██╗  ██╗ █████╗ ███╗   ██╗ █████╗ ██╗    ██╗ █████╗     ║
    ║     ██║ ██╔╝██╔══██╗████╗  ██║██╔══██╗██║    ██║██╔══██╗    ║
    ║     █████╔╝ ███████║██╔██╗ ██║███████║██║ █╗ ██║███████║    ║
    ║     ██╔═██╗ ██╔══██║██║╚██╗██║██╔══██║██║███╗██║██╔══██║    ║
    ║     ██║  ██╗██║  ██║██║ ╚████║██║  ██║╚███╔███╔╝██║  ██║    ║
    ║     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ║
    ║                                                              ║
    ║                     S O F T W A R E                          ║
    ║                   Sistema de Gestão Completo                 ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
            """
            frame = tk.Frame(parent, bg=colors['primary'], padx=20, pady=15)
            frame.pack(fill='x')
            
            logo_label = tk.Label(frame, text=logo_text, font=('Courier', 8),
                                 bg=colors['primary'], fg='white', justify='center')
            logo_label.pack()
            
            return frame
        
        else:
            # Logo pequeno para toolbar
            frame = tk.Frame(parent, bg=colors['primary'])
            tk.Label(frame, text="🔷 KS", font=('Segoe UI', 12, 'bold'),
                    bg=colors['primary'], fg='white').pack(side='left', padx=10)
            return frame
    
    @staticmethod
    def create_card(parent, title, description, icon="🏪", color="black"):
        """Cria um card estilizado para a tela inicial"""
        card = tk.Frame(parent, bg='white', relief='flat', bd=0)
        
        # Sombra simulada
        shadow = tk.Frame(card, bg='#cbd5e1', height=2)
        shadow.pack(fill='x', side='bottom')
        
        # Conteúdo
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=15)
        
        tk.Label(content, text=icon, font=('Segoe UI', 32),
                bg='white', fg=color).pack()
        tk.Label(content, text=title, font=('Segoe UI', 14, 'bold'),
                bg='white', fg='#1e293b').pack(pady=(10, 5))
        tk.Label(content, text=description, font=('Segoe UI', 9),
                bg='white', fg='#64748b', wraplength=200).pack()
        
        return card


# ==================== CLASSE DE MELHORIAS DO PDV ====================
class PDVEnhancements:
    """Melhorias específicas para o módulo PDV"""
    
    @staticmethod
    def setup_focus_and_shortcuts(pdv_tab, app_instance):
        """
        Configura foco automático e atalhos de teclado no PDV
        
        Args:
            pdv_tab: frame da aba PDV
            app_instance: instância da classe KanawaApp
        """
        # Garantir que o campo de busca existe
        if hasattr(app_instance, 'pdv_search'):
            # Definir foco automático ao entrar na aba
            def on_tab_selected(event=None):
                if app_instance.notebook and app_instance.notebook.index('current') == 1:
                    app_instance.pdv_search.focus_set()
                    app_instance.update_status("PDV ativo - Digite para buscar ou use código de barras")
            
            # Bind para quando a aba é selecionada
            if hasattr(app_instance, 'notebook'):
                app_instance.notebook.bind('<<NotebookTabChanged>>', on_tab_selected)
            
            # Enter no campo de busca filtra produtos
            def on_search_enter(event):
                app_instance.filter_pdv_products()
                # Opcional: focar na lista de produtos
                if hasattr(app_instance, 'products_tree') and app_instance.products_tree:
                    app_instance.products_tree.focus_set()
            
            app_instance.pdv_search.bind('<Return>', on_search_enter)
        
        # Enter na lista de produtos adiciona ao carrinho
        if hasattr(app_instance, 'products_tree') and app_instance.products_tree:
            def on_product_enter(event):
                app_instance.add_to_cart()
                # Voltar foco para busca
                if hasattr(app_instance, 'pdv_search'):
                    app_instance.pdv_search.focus_set()
                    app_instance.pdv_search.select_range(0, tk.END)
            
            app_instance.products_tree.bind('<Return>', on_product_enter)
            app_instance.products_tree.bind('<Double-1>', lambda e: app_instance.add_to_cart())
        
        # Atalho numérico para quantidade (tecla 'Q')
        def on_q_pressed(event):
            if hasattr(app_instance, 'cart_listbox') and app_instance.cart_listbox.curselection():
                app_instance.remove_from_cart()
        
        app_instance.root.bind('<Key-q>', on_q_pressed)
        app_instance.root.bind('<Key-Q>', on_q_pressed)
        
        # Atalho 'C' para limpar carrinho
        def on_c_pressed(event):
            if hasattr(app_instance, 'cart') and app_instance.cart:
                app_instance.clear_cart()
        
        app_instance.root.bind('<Key-c>', on_c_pressed)
        app_instance.root.bind('<Key-C>', on_c_pressed)
        
        # Atalho 'F' para finalizar venda
        def on_f_pressed(event):
            if hasattr(app_instance, 'cart') and app_instance.cart:
                if hasattr(app_instance, 'pdv_finalize_with_dialog'):
                    app_instance.pdv_finalize_with_dialog()
                else:
                    app_instance.finalize_sale()
        
        app_instance.root.bind('<Key-f>', on_f_pressed)
        app_instance.root.bind('<Key-F>', on_f_pressed)


# ==================== MELHORIAS DA TELA INICIAL ====================
class InitialScreenEnhancements:
    """Melhorias para a tela inicial do sistema"""
    
    @staticmethod
    def create_enhanced_initial_screen(parent, app_instance):
        """
        Cria uma tela inicial aprimorada com cards maiores e mais informativos
        """
        for widget in parent.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(parent, bg='white')
        main_frame.pack(fill='both', expand=True)
        
        # Container central responsivo
        container = tk.Frame(main_frame, bg='white', relief='flat')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)
        
        # Cabeçalho com logo
        header = tk.Frame(container, bg='white', height=150)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="🏪", font=('Segoe UI', 25),
                bg='white', fg='black').pack(pady=10)
        tk.Label(header, text="KANAWA SOFT", font=('Segoe UI', 24, 'bold'),
                bg='white', fg='black').pack()
        tk.Label(header, text="Sistema de Gestão Completo", font=('Segoe UI', 11),
                bg='white', fg='black').pack()
        
        # Corpo com cards
        body = tk.Frame(container, bg='white')
        body.pack(fill='both', expand=True, padx=10, pady=20)
        
        # Cards de nível de empresa
        levels = [
            ("🏪 MICRO EMPRESA", "micro", "#10b981",
             "✓ Controle Financeiro\n✓ Notas Fiscais\n✓ Gestão de Estoque\n✓ PDV Completo"),
            ("🏬 SUPERMERCADO", "macro", "#3b82f6",
             "✓ Gestão de Múltiplas Categorias\n✓ Controle de Fornecedores\n✓ Promoções e Ofertas\n✓ Relatórios Avançados"),
            ("🏭 HIPERMERCADO", "industry", "#8b5cf6",
             "✓ Múltiplos PDVs\n✓ MRP e Produção\n✓ Controle de Filiais\n✓ Business Intelligence")
        ]
        
        # Frame para os cards
        cards_frame = tk.Frame(body, bg='white')
        cards_frame.pack(expand=True, fill='both')
        
        for i, (title, level, color, description) in enumerate(levels):
            # Card
            card = tk.Frame(cards_frame, bg='white', relief='solid', bd=1,
                          highlightbackground='#e2e8f0', highlightthickness=1)
            card.grid(row=0, column=i, padx=15, pady=10, sticky='nsew')
            cards_frame.grid_columnconfigure(i, weight=1)
            
            # Ícone
            icon_label = tk.Label(card, text=title.split()[0], font=('Segoe UI', 10),
                                 bg='white', fg=color)
            icon_label.pack(pady=(20, 10))
            
            # Título
            tk.Label(card, text=title, font=('Segoe UI', 10, 'bold'),
                    bg='white', fg='#1e293b').pack()
            
            # Separador
            tk.Frame(card, bg=color, height=2, width=30).pack(pady=10)
            
            # Descrição
            tk.Label(card, text=description, font=('Segoe UI', 8),
                    bg='white', fg='#475569', justify='center').pack(pady=10)
            
            # Botão
            btn = tk.Button(card, text=f"▶️ {title.split()[1]} {title.split()[2] if len(title.split())>2 else ''}",
                           command=lambda l=level: app_instance.set_company_level(l),
                           bg=color, fg='white', font=('Segoe UI', 8, 'bold'),
                           padx=20, pady=8, bd=0, cursor='hand2')
            btn.pack(pady=(10, 20))
            
            # Efeito hover
            def on_enter(e, btn=btn, bg=color):
                btn.config(bg='#1e293b')
            def on_leave(e, btn=btn, bg=color):
                btn.config(bg=bg)
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        # Footer
        footer = tk.Frame(container, bg='#f1f5f9', height=40)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        tk.Label(footer, text=f"© Daniel Wasomba | D.Pedro Soluções |suporte tecnica:+244946299834 v1",
                font=('Segoe UI', 10), bg='#f1f5f9', fg='#64748b').pack(pady=10)
        
        # Botão continuar
        continue_btn = tk.Button(container, text="▶️ CONTINUAR", command=app_instance.show_login,
                                bg='#00adb5', fg='white', font=('Segoe UI', 12, 'bold'),
                                padx=40, pady=10, bd=0, cursor='hand2')
        continue_btn.pack(side='bottom', pady=15)
        
        def on_enter_cont(e):
            continue_btn.config(bg='#0891b2')
        def on_leave_cont(e):
            continue_btn.config(bg='#00adb5')
        continue_btn.bind('<Enter>', on_enter_cont)
        continue_btn.bind('<Leave>', on_leave_cont)


# ==================== GRÁFICOS NO DASHBOARD ====================
class DashboardCharts:
    """Adiciona gráficos nativos ao dashboard"""
    
    @staticmethod
    def add_charts_to_dashboard(dashboard_tab, app_instance, low_stock_container=None):
        """
        Adiciona gráficos de vendas e estoque baixo ao dashboard
        """
        db = app_instance.db
        colors = {
            'primary': '#00adb5',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444'
        }
        
        # Buscar dados de vendas dos últimos 7 dias
        daily_sales = {}
        today = datetime.date.today()
        
        for i in range(7):
            date = today - datetime.timedelta(days=6-i)
            daily_sales[date] = 0
        
        for sale in db.get_sales():
            if sale.created_at:
                try:
                    sale_date = datetime.datetime.fromisoformat(sale.created_at).date()
                    if sale_date in daily_sales:
                        daily_sales[sale_date] += sale.total
                except:
                    pass
        
        # Preparar dados para o gráfico
        sales_data = [(date.strftime('%d/%m'), amount) for date, amount in daily_sales.items()]
        
        # Frame para o gráfico de vendas
        sales_chart_frame = tk.Frame(dashboard_tab, bg='white', relief='flat', bd=0,
                                    highlightbackground='#e2e8f0', highlightthickness=1)
        sales_chart_frame.pack(fill='both', expand=True, pady=10)
        tk.Label(sales_chart_frame, text="📊 Vendas dos Últimos 7 Dias", font=('Segoe UI', 12, 'bold'), bg='white', fg=app_instance.colors['dark']).pack(anchor='w', padx=15, pady=(15, 0))
        tk.Frame(sales_chart_frame, bg='#e2e8f0', height=1).pack(fill='x', padx=15, pady=(10, 0))
        
        # Criar gráfico de barras
        if any(amount > 0 for _, amount in sales_data):
            chart_canvas = NativeCharts.create_bar_chart(
                sales_chart_frame, sales_data,
                title="", x_label="Data", y_label="Valor (AOA)",
                width=500, height=180
            )
            
            # Adicionar linha de tendência
            if hasattr(chart_canvas, 'find_all'):
                values = [amount for _, amount in sales_data]
                if len(values) > 1:
                    # Calcular posições da linha de tendência
                    margin_left = 60
                    margin_right = 30
                    margin_top = 50
                    margin_bottom = 50
                    chart_width = 450 - margin_left - margin_right
                    chart_height = 250 - margin_top - margin_bottom
                    
                    max_value = max(values) if values else 1
                    if max_value == 0:
                        max_value = 1
                    
                    bar_width = (chart_width / len(sales_data)) * 0.7
                    bar_spacing = (chart_width / len(sales_data)) * 0.3
                    
                    x_points = []
                    y_points = []
                    
                    for idx, value in enumerate(values):
                        x = margin_left + idx * (bar_width + bar_spacing) + bar_width/2 + bar_spacing/2
                        bar_height = (value / max_value) * chart_height
                        y = 250 - margin_bottom - bar_height + bar_height/2
                        x_points.append(x)
                        y_points.append(y)
                    
                    # Desenhar linha de tendência
                    NativeCharts.create_trend_line(chart_canvas, values, x_points, y_points,
                                                  color=colors['primary'])
        else:
            tk.Label(sales_chart_frame, text="Nenhuma venda registrada nos últimos 7 dias",
                    font=('Segoe UI', 12), bg='white', fg='#64748b').pack(pady=40)
        
        # Gráfico de produtos com estoque baixo
        low_stock = db.get_products_low_stock()
        low_stock_data = [(p.name[:20], p.stock) for p in low_stock[:8]]  # Top 8 produtos
        parent = low_stock_container if low_stock_container is not None else dashboard_tab
        
        if low_stock_data:
            low_stock_frame = tk.Frame(parent, bg='white', relief='flat', bd=0,
                                       highlightbackground='#e2e8f0', highlightthickness=1)
            low_stock_frame.pack(fill='both', expand=True, pady=10)
            tk.Label(low_stock_frame, text="⚠️ Produtos com Estoque Baixo", font=('Segoe UI', 12, 'bold'), bg='white', fg=app_instance.colors['dark']).pack(anchor='w', padx=15, pady=(15, 0))
            tk.Frame(low_stock_frame, bg='black', height=1).pack(fill='x', padx=15, pady=(10, 0))
            NativeCharts.create_horizontal_bar_chart(
                low_stock_frame, low_stock_data,
                title="", width=950, height=min(300, len(low_stock_data) * 35)
            )


# ==================== FUNÇÃO DE PATCH PRINCIPAL ====================
def apply_patches(app_instance):
    """
    Aplica todos os patches no sistema existente
    
    Args:
        app_instance: instância da classe KanawaApp
    """
    
    # 1. Melhorar a tela inicial
    original_show_initial = app_instance.show_initial_screen
    
    def patched_show_initial():
        InitialScreenEnhancements.create_enhanced_initial_screen(app_instance.root, app_instance)
    
    app_instance.show_initial_screen = patched_show_initial
    
    
    # 3. Melhorar o PDV com foco automático
    original_create_pdv = app_instance.create_pdv_tab
    
    def patched_create_pdv():
        original_create_pdv()
        # Encontrar a aba PDV e aplicar melhorias
        for child in app_instance.root.winfo_children():
            if isinstance(child, ttk.Notebook):
                for tab_id in range(child.index('end')):
                    if child.tab(tab_id, 'text') == "🛒 PDV":
                        pdv_frame = child.nametowidget(child.tabs()[tab_id])
                        PDVEnhancements.setup_focus_and_shortcuts(pdv_frame, app_instance)
                        break
                break
    
    app_instance.create_pdv_tab = patched_create_pdv
    
    # 4. Melhorar o login com Enter
    original_show_login = app_instance.show_login
    
    def patched_show_login():
        original_show_login()
        # Adicionar bind de Enter nos campos de login
        if hasattr(app_instance, 'login_email') and hasattr(app_instance, 'login_password'):
            def on_enter(event):
                app_instance.do_login()
            app_instance.login_email.bind('<Return>', on_enter)
            app_instance.login_password.bind('<Return>', on_enter)
            # Focar no campo de email
            app_instance.login_email.focus_set()
            app_instance.login_email.select_range(0, tk.END)
    
    app_instance.show_login = patched_show_login
    
    # 5. Adicionar cursor hand2 em todos os botões existentes
    def add_cursors_to_buttons(widget):
        """Recursivamente adiciona cursor hand2 a todos os botões"""
        try:
            if isinstance(widget, tk.Button) or isinstance(widget, ttk.Button):
                widget.config(cursor='hand2')
            for child in widget.winfo_children():
                add_cursors_to_buttons(child)
        except:
            pass
    
    # Aplicar após cada criação de tela
    original_show_main = app_instance.show_main_screen
    
    def patched_show_main():
        original_show_main()
        app_instance.root.after(100, lambda: add_cursors_to_buttons(app_instance.root))
    
    app_instance.show_main_screen = patched_show_main
    
    print("✅ Patches aplicados com sucesso!")
    print("   - Tela inicial aprimorada")
    print("   - Gráficos nativos no dashboard")
    print("   - PDV com foco automático e atalhos")
    print("   - Login com tecla Enter")
    print("   - Cursor hand2 em todos os botões")


class KanawaApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.current_user = None
        self.cart = []
        self.user_role = None
        self.notebook = None
        self.barcode_entry = None
        self.status_label = None
        self.products_tree = None
        self.cart_listbox = None
        self.cart_total_label = None

        self.root.title(f"{APP_NAME} - {VERSION}")
        self.root.configure(bg='#f0f2f5')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # ── Detecção automática do monitor ──────────────────────────────
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        # Escolhe dimensão de acordo com o tamanho do ecrã
        if sw >= 1920:
            win_w, win_h = 1610, 920
        elif sw >= 1440:
            win_w, win_h = 1326, 800
        elif sw >= 1280:
            win_w, win_h = 1250, 720
        else:
            win_w, win_h = min(sw, 104), min(sh, 640)

        # Centrar na janela
        x = max(0, (sw - win_w) // 2)
        y = max(0, (sh - win_h) // 2)
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.root.minsize(1024, 600)

        # Guarda largura do ecrã para dimensionamento proporcional do PDV
        self._screen_w = sw
        self._screen_h = sh
        self._win_w    = win_w
        self._win_h    = win_h

        # Largura dinâmica do painel direito do PDV (≈35 % da janela, mín 250 px)
        self._pdv_right_w = max(250, int(win_w * 0.35))
        # ────────────────────────────────────────────────────────────────

        self.root.bind('<Configure>', self.on_window_resize)

        self.colors = {
            'primary': '#1e293b', 'secondary': '#334155', 'success': '#10b981',
            'warning': '#f59e0b', 'danger': '#ef4444', 'info': '#3b82f6',
            'dark': '#0f172a', 'light': '#f1f5f9', 'white': '#ffffff'
        }

        # Fontes adaptadas ao tamanho do monitor
        base = 10 if sw < 1440 else 11
        self.fonts = {
            'title':   ('Segoe UI', base + 14, 'bold'),
            'heading': ('Segoe UI', base + 4,  'bold'),
            'normal':  ('Segoe UI', base),
            'small':   ('Segoe UI', base - 1),
            'pdv_key': ('Segoe UI', base + 6,  'bold'),
        }

        self.show_initial_screen()

    def on_window_resize(self, event):
        """Atualiza dimensões dinâmicas quando a janela é redimensionada."""
        try:
            if event.widget is self.root:
                w = self.root.winfo_width()
                if w > 200:
                    self._win_w = w
                    self._pdv_right_w = max(400, int(w * 0.35))
            self.root.update_idletasks()
        except Exception:
            pass

    def show_initial_screen(self):
        InitialScreenEnhancements.create_enhanced_initial_screen(self.root, self)

    def set_company_level(self, level):
        company = self.db.get_company()
        if company:
            company.level = level
            self.db.update_company(company)
        else:
            company = Company(level=level)
            self.db.create_company(company)
        level_names = {'micro': 'EMPRESA MICRO', 'macro': 'SUPERMERCADO', 'industry': 'HIPERMERCADO'}
        messagebox.showinfo("Nível Definido", f"Nível da empresa definido para: {level_names.get(level, level)}")

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg=self.colors['primary'])
        main_frame.pack(fill='both', expand=True)

        card = tk.Frame(main_frame, bg=self.colors['white'], relief='flat', bd=0)
        card.pack(fill='both', expand=True, padx=20, pady=20)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=0)

        tk.Label(card, text="🔐", font=('Hobo Std', 25),
                bg=self.colors['white'], fg=self.colors['primary']).pack(pady=20)
        tk.Label(card, text="Acesso ao Sistema", font=self.fonts['title'],
                bg=self.colors['white'], fg=self.colors['dark']).pack()

        tk.Label(card, text="Email", anchor='w', bg=self.colors['white']).pack(fill='x', padx=30, pady=(20, 5))
        self.login_email = tk.Entry(card, font=self.fonts['normal'], bd=1, relief='solid')
        self.login_email.pack(fill='x', padx=30, pady=(0, 15))
        self.login_email.insert(0, "")

        tk.Label(card, text="Senha", anchor='w', bg=self.colors['white']).pack(fill='x', padx=30, pady=(0, 5))
        self.login_password = tk.Entry(card, font=self.fonts['normal'], show="*", bd=1, relief='solid')
        self.login_password.pack(fill='x', padx=30, pady=(0, 15))
        self.login_password.insert(0, "")

        tk.Button(card, text="Entrar", command=self.do_login,
                 bg=self.colors['success'], fg='white', font=self.fonts['heading'], bd=0).pack(pady=10, padx=30, fill='x')
        card.pack_propagate(False)

        tk.Label(card, text="ENTRA EM CONTACTO PARA TE FORNECER CHAVE DE ACESSO: +244 94699834/+244 959777301",
                font=self.fonts['small'], bg=self.colors['white'], fg='gray').pack(pady=10)

        # Adicionar bind de Enter nos campos de login
        def on_enter(event):
            self.do_login()
        self.login_email.bind('<Return>', on_enter)
        self.login_password.bind('<Return>', on_enter)
        # Focar no campo de email
        self.login_email.focus_set()
        self.login_email.select_range(0, tk.END)

    def do_login(self):
        user = self.db.authenticate_user(self.login_email.get(), self.login_password.get())
        if user:
            self.current_user = user
            self.user_role = user.role
            self.db.current_user = user

            # Verificar se é vendedor e tem limite configurado
            if user.role == 'seller':
                limit = self.db.get_seller_limit(user.id)
                if not limit:
                    self.db.create_seller_limit(user.id, user.name)
                    messagebox.showinfo("Limite Definido", f"Limite diário: 50.000 AOA\nLimite mensal: 200.000 AOA")

            self.show_main_screen()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos!")

    def show_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_menu_bar()
        self.create_toolbar()
        self.create_status_bar()

        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Criar todas as abas
        self.create_dashboard_tab()
        self.create_pdv_tab()
        self.create_products_tab()
        self.create_clients_tab()
        self.create_suppliers_tab()
        self.create_quotes_tab()
        self.create_purchases_tab()
        self.create_returns_tab()
        self.create_finance_tab()
        self.create_reports_tab()
        self.create_production_tab()
        self.create_bom_tab()
        self.create_stock_movements_tab()
        self.create_sellers_tab()
        self.create_pdv_sessions_tab()
        self.create_cash_register_tab()       # ← NOVO: Caixa diário
        self.create_promotions_tab()          # ← NOVO: Promoções
        self.create_service_orders_tab()      # ← NOVO: Ordens de serviço
        self.create_backup_tab()
        self.create_settings_tab()

        if self.user_role == 'admin':
            self.create_users_tab()
            self.create_permissions_tab()

        self.notebook.select(0)
        self.update_status("Sistema pronto. Use o menu para navegar.")

        # Adicionar cursor hand2 em todos os botões
        self.root.after(100, lambda: self.add_cursors_to_buttons(self.root))

    def add_cursors_to_buttons(self, widget):
        """Recursivamente adiciona cursor hand2 a todos os botões"""
        try:
            if isinstance(widget, tk.Button) or isinstance(widget, ttk.Button):
                widget.config(cursor='hand2')
            for child in widget.winfo_children():
                self.add_cursors_to_buttons(child)
        except:
            pass

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # ===== MENU VENDAS =====
        menu_vendas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🛒 VENDAS", menu=menu_vendas)
        menu_vendas.add_command(label="🛍️ PDV", command=lambda: self.select_tab(1), accelerator="F2")
        menu_vendas.add_separator()
        menu_vendas.add_command(label="📋 Orçamentos", command=lambda: self.select_tab(4))
        menu_vendas.add_command(label="📄 Notas Fiscais", command=lambda: self.select_tab(8))
        menu_vendas.add_command(label="🔄 Devoluções", command=lambda: self.select_tab(7))
        menu_vendas.add_separator()
        menu_vendas.add_command(label="👥 Clientes", command=lambda: self.select_tab(3))
        menu_vendas.add_command(label="📦 Produtos", command=lambda: self.select_tab(2))
        menu_vendas.add_separator()
        menu_vendas.add_command(label="💰 Todas as Vendas", command=self.show_sales_history)

        # ===== MENU ESTOQUE =====
        menu_estoque = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📦 ESTOQUE", menu=menu_estoque)
        menu_estoque.add_command(label="📦 Produtos", command=lambda: self.select_tab(2))
        menu_estoque.add_command(label="🏷️ Categorias", command=self.manage_categories)
        menu_estoque.add_command(label="📏 Unidades", command=self.manage_units)
        menu_estoque.add_separator()
        menu_estoque.add_command(label="📊 Movimentações", command=lambda: self.select_tab(12))
        menu_estoque.add_command(label="🔄 Transferências", command=self.open_stock_transfer)
        menu_estoque.add_command(label="📋 Inventário", command=self.open_inventory)
        menu_estoque.add_separator()
        menu_estoque.add_command(label="📥 Entrada de Estoque", command=self.open_stock_entry)
        menu_estoque.add_command(label="📤 Saída de Estoque", command=self.open_stock_exit)

        # ===== MENU MRP =====
        menu_mrp = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🏭 MRP", menu=menu_mrp)
        menu_mrp.add_command(label="🧠 Planejamento MRP", command=self.open_mrp_planning)
        menu_mrp.add_command(label="📋 Necessidades de Materiais", command=self.show_mrp_requirements)
        menu_mrp.add_command(label="✅ Ordens Sugeridas", command=self.show_suggested_orders)
        menu_mrp.add_separator()
        menu_mrp.add_command(label="📋 Lista de Materiais (BOM)", command=lambda: self.select_tab(11))
        menu_mrp.add_command(label="⏱️ Lead Times", command=self.manage_lead_times)

        # ===== MENU PRODUÇÃO =====
        menu_producao = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 PRODUÇÃO", menu=menu_producao)
        menu_producao.add_command(label="📋 Ordens de Produção", command=lambda: self.select_tab(10))
        menu_producao.add_command(label="📊 Acompanhamento", command=self.view_production_tracking)
        menu_producao.add_command(label="📝 Apontamentos", command=self.add_production_note)
        menu_producao.add_separator()
        menu_producao.add_command(label="📋 Roteiros", command=self.manage_routings)
        menu_producao.add_command(label="🏭 Centros de Trabalho", command=self.manage_workcenters)

        # ===== MENU COMPRAS =====
        menu_compras = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🛒 COMPRAS", menu=menu_compras)
        menu_compras.add_command(label="📦 Pedidos de Compra", command=lambda: self.select_tab(5))
        menu_compras.add_command(label="📄 Cotações", command=self.open_quotations)
        menu_compras.add_separator()
        menu_compras.add_command(label="🏢 Fornecedores", command=lambda: self.select_tab(3))
        menu_compras.add_command(label="📋 Recebimentos", command=self.open_receipts)

        # ===== MENU FINANCEIRO =====
        menu_financeiro = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="💰 FINANCEIRO", menu=menu_financeiro)

        submenu_contas = tk.Menu(menu_financeiro, tearoff=0)
        submenu_contas.add_command(label="💸 Contas a Pagar", command=self.open_payables)
        submenu_contas.add_command(label="📈 Contas a Receber", command=self.open_receivables)
        menu_financeiro.add_cascade(label="📋 Contas", menu=submenu_contas)

        submenu_caixa = tk.Menu(menu_financeiro, tearoff=0)
        submenu_caixa.add_command(label="🏦 Caixa", command=self.open_cash_management)
        submenu_caixa.add_command(label="📊 Fluxo de Caixa", command=self.open_cashflow)
        menu_financeiro.add_cascade(label="💵 Caixa", menu=submenu_caixa)

        menu_financeiro.add_separator()
        menu_financeiro.add_command(label="💸 Despesas", command=self.open_expenses_dialog)
        # CORREÇÃO: Usar cashflow_report que já existe
        menu_financeiro.add_command(label="📊 Relatório Financeiro", command=self.cashflow_report)

        # ===== MENU CLIENTES =====
        menu_clientes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👥 CLIENTES", menu=menu_clientes)
        menu_clientes.add_command(label="📝 Cadastro", command=lambda: self.select_tab(3))
        menu_clientes.add_command(label="📊 Histórico", command=self.view_client_history)
        menu_clientes.add_separator()
        menu_clientes.add_command(label="⭐ Clientes VIP", command=self.vip_clients_report)
        menu_clientes.add_command(label="📧 Comunicação", command=self.client_communication)

        # ===== MENU RELATÓRIOS =====
        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📈 RELATÓRIOS", menu=menu_relatorios)

        submenu_vendas = tk.Menu(menu_relatorios, tearoff=0)
        submenu_vendas.add_command(label="📊 Vendas por Período", command=self.sales_period_report)
        submenu_vendas.add_command(label="👥 Vendas por Vendedor", command=self.sales_by_seller_report)
        submenu_vendas.add_command(label="📦 Produtos Mais Vendidos", command=self.top_products_report)
        menu_relatorios.add_cascade(label="📊 Vendas", menu=submenu_vendas)

        submenu_estoque = tk.Menu(menu_relatorios, tearoff=0)
        submenu_estoque.add_command(label="📦 Estoque Atual", command=self.stock_report)
        submenu_estoque.add_command(label="⚠️ Produtos com Baixo Estoque", command=self.low_stock_report)
        menu_relatorios.add_cascade(label="📦 Estoque", menu=submenu_estoque)

        menu_relatorios.add_separator()
        menu_relatorios.add_command(label="📤 Exportar Vendas", command=self.export_sales_excel)
        menu_relatorios.add_command(label="📄 Relatório Geral", command=self.general_report)

        # ===== MENU ADMIN =====
        if self.user_role == 'admin':
            menu_admin = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="⚙️ ADMIN", menu=menu_admin)
            menu_admin.add_command(label="👥 Usuários", command=lambda: self.select_tab(16))
            menu_admin.add_command(label="🔐 Permissões", command=lambda: self.select_tab(17))
            menu_admin.add_command(label="📜 Logs do Sistema", command=self.view_logs)
            menu_admin.add_separator()
            menu_admin.add_command(label="💾 Backup", command=lambda: self.select_tab(15))
            menu_admin.add_command(label="🖨️ Impressoras", command=self.printer_settings)

        # ===== MENU AJUDA =====
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ AJUDA", menu=menu_ajuda)
        menu_ajuda.add_command(label="📖 Documentação", command=self.show_documentation)
        menu_ajuda.add_command(label="📞 Suporte", command=self.show_support)
        menu_ajuda.add_command(label="ℹ️ Sobre", command=self.show_about)
        menu_ajuda.add_separator()
        menu_ajuda.add_command(label="🚪 Sair", command=self.logout, accelerator="Ctrl+Q")

        # Atalhos de teclado
        self.root.bind('<F2>', lambda e: self.select_tab(1))
        self.root.bind('<Control-q>', lambda e: self.logout())
        self.root.bind('<F5>', lambda e: self.refresh_current_tab())
        self.root.bind('<F1>', lambda e: self.show_documentation())

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg=self.colors['primary'], height=45)
        toolbar.pack(side='top', fill='x')
        toolbar.pack_propagate(False)

        buttons = [
            ("🏠 Início", 0), ("🛒 PDV", 1), ("📦 Produtos", 2),
            ("👥 Clientes", 3), ("💰 Financeiro", 8), ("📈 Relatórios", 9),
            ("💾 Backup", 15), ("⚙️ Config", 14)
        ]
        for text, tab in buttons:
            tk.Button(toolbar, text=text, command=lambda t=tab: self.select_tab(t),
                     bg=self.colors['secondary'], fg='white', font=self.fonts['small'],
                     padx=12, pady=5).pack(side='left', padx=2, pady=2)

        # Separador
        tk.Frame(toolbar, width=20, bg=self.colors['primary']).pack(side='left')

        # Campo de código de barras
        tk.Label(toolbar, text="📱 Código de Barras:", font=self.fonts['small'],
                bg=self.colors['primary'], fg='white').pack(side='left', padx=(10, 5))
        self.barcode_entry = tk.Entry(toolbar, font=self.fonts['normal'], width=30)
        self.barcode_entry.pack(side='left', padx=5)
        self.barcode_entry.bind('<Return>', self.on_barcode_scan)
        self.barcode_entry.bind('<FocusIn>', lambda e: self.update_status("Aguardando código de barras..."))

        # Relógio
        self.clock_label = tk.Label(toolbar, font=self.fonts['small'],
                                    bg=self.colors['primary'], fg='white')
        self.clock_label.pack(side='right', padx=20)
        self.update_clock()

        # Usuário logado
        role_icons = {'admin': '👑', 'manager': '📋', 'seller': '🛒', 'stock': '📦'}
        icon = role_icons.get(self.user_role, '👤')
        tk.Label(toolbar, text=f"{icon} {self.current_user.name} ({self.user_role})",
                font=self.fonts['small'], bg=self.colors['primary'], fg='#a5f3fc').pack(side='right', padx=10)

    def create_status_bar(self):
        status_bar = tk.Frame(self.root, bg=self.colors['secondary'], height=25)
        status_bar.pack(side='bottom', fill='x')
        status_bar.pack_propagate(False)

        self.status_label = tk.Label(status_bar, text="Pronto", font=self.fonts['small'],
                                     bg=self.colors['secondary'], fg='white')
        self.status_label.pack(side='left', padx=10)

        company = self.db.get_company()
        if company:
            level_names = {'micro': '🏪 Micro', 'macro': '🏬 Macro', 'industry': '🏭 Indústria'}
            level_text = level_names.get(company.level, company.level)
            tk.Label(status_bar, text=f"{level_text} | Moeda: {company.currency}",
                    font=self.fonts['small'], bg=self.colors['secondary'], fg='#cbd5e1').pack(side='right', padx=10)

    def update_clock(self):
        try:
            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if hasattr(self, 'clock_label') and self.clock_label and self.clock_label.winfo_exists():
                self.clock_label.config(text=now)
        except:
            pass
        self.root.after(1000, self.update_clock)

    def update_status(self, message):
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.config(text=message)

    def select_tab(self, index):
        if self.notebook:
            try:
                self.notebook.select(index)
                tab_text = self.notebook.tab(index, 'text')
                self.update_status(f"Aba selecionada: {tab_text}")
            except:
                pass

    def refresh_current_tab(self):
        self.update_status("Atualizado")

    # ========== DASHBOARD ==========
    def create_dashboard_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Dashboard")

        # Frame rolável
        canvas = tk.Canvas(tab, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.colors['light'])

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Título
        tk.Label(scrollable, text="Dashboard - Visão Geral", font=self.fonts['title'],
                bg=self.colors['light'], fg=self.colors['dark']).pack(pady=20)

        # KPIs
        kpis = self.db.get_financial_summary()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        metrics_frame = tk.Frame(scrollable, bg=self.colors['light'])
        metrics_frame.pack(fill='x', padx=20, pady=10)

        metrics = [
            ("💰 Vendas Totais", f"{currency} {kpis['receita_total']:,.2f}", self.colors['success']),
            ("📦 Produtos", str(len(self.db.get_products())), self.colors['info']),
            ("👥 Clientes", str(len(self.db.get_clients())), self.colors['primary']),
            ("📈 Lucro", f"{currency} {kpis['lucro_real']:,.2f}", self.colors['warning'])
        ]

        for i, (title, value, color) in enumerate(metrics):
            card = tk.Frame(metrics_frame, bg='white', relief='flat', bd=0,
                          highlightbackground='#e2e8f0', highlightthickness=1)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            metrics_frame.grid_columnconfigure(i, weight=1)
            tk.Label(card, text=title, font=self.fonts['small'], bg='white', fg='#64748b').pack(pady=(12, 0))
            tk.Label(card, text=value, font=('Segoe UI', 18, 'bold'), bg='white', fg=color).pack(pady=(5, 12))

        # Gráficos e alertas principais
        charts_container = tk.Frame(scrollable, bg=self.colors['light'])
        charts_container.pack(fill='both', expand=True, padx=20, pady=10)
        charts_container.columnconfigure(0, weight=2)
        charts_container.columnconfigure(1, weight=1)

        left_chart = tk.Frame(charts_container, bg=self.colors['light'])
        right_chart = tk.Frame(charts_container, bg=self.colors['light'])
        left_chart.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        right_chart.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        summary_card = tk.Frame(right_chart, bg='white', relief='flat', bd=0,
                                highlightbackground='#e2e8f0', highlightthickness=1)
        summary_card.pack(fill='x', pady=(0, 10))
        tk.Label(summary_card, text="Resumo Rápido", font=self.fonts['heading'], bg='white', fg=self.colors['dark']).pack(anchor='w', padx=15, pady=(15, 5))

        low_stock_count = len(self.db.get_products_low_stock())
        tk.Label(summary_card, text=f"Produtos com estoque baixo: {low_stock_count}",
                 font=self.fonts['normal'], bg='white', fg='#475569').pack(anchor='w', padx=15, pady=(0, 10))

        tk.Label(summary_card, text="Use a visão lateral para acompanhar o estoque crítico.",
                 font=('Segoe UI', 9), bg='white', fg='#94a3b8').pack(anchor='w', padx=15, pady=(0, 15))

        DashboardCharts.add_charts_to_dashboard(left_chart, self, low_stock_container=right_chart)

        # Atividades Recentes
        acts_frame = tk.Frame(scrollable, bg='white', relief='flat', bd=0,
                              highlightbackground='#e2e8f0', highlightthickness=1)
        acts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        tk.Label(acts_frame, text="📝 Atividades Recentes", font=self.fonts['heading'], bg='white', fg=self.colors['dark']).pack(anchor='w', padx=15, pady=(15, 5))

        acts_list = tk.Listbox(acts_frame, font=self.fonts['normal'], height=10, bd=0, highlightthickness=0)
        acts_list.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        for act in self.db.get_activities(15):
            icon = "💰" if act['type'] == "sale" else "📦" if act['type'] == "stock" else "🔧" if act['type'] == "production" else "📝"
            acts_list.insert(tk.END, f"{icon} {act['description'][:80]}")

    # ========== PDV ==========
    def create_pdv_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛒 PDV")

        # ── Barra superior: código de barras ────────────────────────────
        top_bar = tk.Frame(tab, bg='#1e293b', height=32)
        top_bar.pack(fill='x', side='top')
        top_bar.pack_propagate(False)

        tk.Label(top_bar, text="📷 Código de Barras:", font=self.fonts['heading'],
                 bg='#1e293b', fg='white').pack(side='left', padx=(15, 5), pady=10)
        self.barcode_entry = tk.Entry(top_bar, font=('Segoe UI', 10, 'bold'),
                                      width=18, bd=0, relief='flat',
                                      bg='#f8fafc', fg='#0f172a')
        self.barcode_entry.pack(side='left', padx=5, ipady=6)
        self.barcode_entry.bind('<Return>', self.on_barcode_scan)

        tk.Button(top_bar, text="⚡ Scan", command=lambda: self.on_barcode_scan(None),
                  bg='#00adb5', fg='white', font=self.fonts['normal'],
                  bd=0, padx=10, pady=2, cursor='hand2').pack(side='left', padx=3)

        # Relógio PDV
        self._pdv_clock_var = tk.StringVar()
        tk.Label(top_bar, textvariable=self._pdv_clock_var, font=self.fonts['normal'],
                 bg='#1e293b', fg='#94a3b8').pack(side='right', padx=20)
        self._update_pdv_clock()

        # ── Corpo principal: esquerda (produtos) + direita (carrinho) ───
        body = tk.Frame(tab, bg=self.colors['light'])
        body.pack(fill='both', expand=True)

        # Painel esquerdo – produtos
        left = tk.Frame(body, bg=self.colors['light'])
        left.pack(side='left', fill='both', expand=True, padx=(10, 4), pady=10)

        # Painel direito – carrinho (largura dinâmica calculada no __init__)
        pdv_right_w = getattr(self, '_pdv_right_w', 40)
        right_outer = tk.Frame(body, bg=self.colors['light'])
        right_outer.pack(side='right', fill='y', padx=(4, 10), pady=10)

        right = tk.Frame(right_outer, bg=self.colors['light'], width=pdv_right_w)
        right.pack(fill='both', expand=True)
        right.pack_propagate(False)

        # ── ESQUERDA: Busca ─────────────────────────────────────────────
        srch_hdr = tk.Frame(left, bg=self.colors['light'])
        srch_hdr.pack(fill='x')
        tk.Label(srch_hdr, text="🔍 Buscar Produto", font=self.fonts['heading'],
                 bg=self.colors['light'], fg=self.colors['dark']).pack(side='left', pady=(0, 4))

        search_frame = tk.Frame(left, bg=self.colors['light'])
        search_frame.pack(fill='x', pady=(0, 6))

        self.pdv_search = tk.Entry(search_frame, font=self.fonts['normal'],
                                   bd=1, relief='solid')
        self.pdv_search.pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=4)
        self.pdv_search.bind('<KeyRelease>', self.filter_pdv_products)

        tk.Button(search_frame, text="🔍", command=self.filter_pdv_products,
                  bg=self.colors['info'], fg='white', bd=0, padx=10,
                  cursor='hand2').pack(side='left')

        # Filtro de categoria
        cat_frame = tk.Frame(left, bg=self.colors['light'])
        cat_frame.pack(fill='x', pady=(0, 6))
        tk.Label(cat_frame, text="Categoria:", font=self.fonts['small'],
                 bg=self.colors['light']).pack(side='left')
        self._pdv_cat_var = tk.StringVar(value="Todas")
        cats = ["Todas"] + [c.name for c in self.db.get_categories()]
        self._pdv_cat_combo = ttk.Combobox(cat_frame, textvariable=self._pdv_cat_var,
                                           values=cats, state='readonly', width=15)
        self._pdv_cat_combo.pack(side='left', padx=5)
        self._pdv_cat_combo.bind('<<ComboboxSelected>>', self.filter_pdv_products)

        # ── ESQUERDA: Tabela de produtos ────────────────────────────────
        tk.Label(left, text="📦 Produtos Disponíveis", font=self.fonts['heading'],
                 bg=self.colors['light'], fg=self.colors['dark']).pack(anchor='w', pady=(4, 4))

        tree_frame = tk.Frame(left, bg=self.colors['light'])
        tree_frame.pack(fill='both', expand=True)

        columns = ('ID', 'Código', 'Nome', 'Preço', 'Estoque', 'Categoria')
        self.products_tree = ttk.Treeview(tree_frame, columns=columns,
                                          show='headings', selectmode='browse')

        col_widths = {'ID': 45, 'Código': 90, 'Nome': 0, 'Preço': 110,
                      'Estoque': 80, 'Categoria': 110}
        for col in columns:
            self.products_tree.heading(col, text=col,
                command=lambda c=col: self._pdv_sort_tree(c))
            w = col_widths.get(col, 80)
            if w == 0:
                self.products_tree.column(col, stretch=True, minwidth=180)
            else:
                self.products_tree.column(col, width=w, stretch=False)

        vsb = ttk.Scrollbar(tree_frame, orient='vertical',
                            command=self.products_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal',
                            command=self.products_tree.xview)
        self.products_tree.configure(yscrollcommand=vsb.set,
                                     xscrollcommand=hsb.set)

        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.products_tree.pack(fill='both', expand=True)

        self.products_tree.bind('<Double-1>', lambda e: self.add_to_cart())
        self.products_tree.bind('<Return>', lambda e: self.add_to_cart())
        self.products_tree.bind('<<TreeviewSelect>>', lambda e: self.on_pdv_product_select())

        # Estilo zebra na tabela
        self.products_tree.tag_configure('odd',  background='#f8fafc')
        self.products_tree.tag_configure('even', background='#ffffff')
        self.products_tree.tag_configure('low',  background='#fef3c7', foreground='#92400e')

        # ── DIREITA: Cabeçalho do carrinho ──────────────────────────────
        cart_hdr = tk.Frame(right, bg='#1e293b', height=25)
        cart_hdr.pack(fill='x')
        cart_hdr.pack_propagate(False)
        tk.Label(cart_hdr, text="🛒 CARRINHO DE COMPRAS", font=self.fonts['heading'],
                 bg='#1e293b', fg='white').pack(pady=8)

        # ── DIREITA: Cliente ─────────────────────────────────────────────
        client_frame = tk.Frame(right, bg='white', relief='flat', bd=0,
                                highlightbackground='#e2e8f0', highlightthickness=1)
        client_frame.pack(fill='x', pady=(4, 0))
        cf_row = tk.Frame(client_frame, bg='white')
        cf_row.pack(fill='x', padx=10, pady=6)
        tk.Label(cf_row, text="👤", font=('Segoe UI', 10), bg='white').pack(side='left')
        self.pdv_client_var = tk.StringVar(value="Consumidor Final")
        tk.Label(cf_row, textvariable=self.pdv_client_var, font=self.fonts['normal'],
                 bg='white', fg=self.colors['dark']).pack(side='left', padx=5)
        tk.Button(cf_row, text="Mudar", command=self.pdv_select_client,
                  bg=self.colors['info'], fg='white', font=self.fonts['small'],
                  bd=0, padx=8, cursor='hand2').pack(side='right')
        self.pdv_current_client = None
        self.pdv_last_receipt = None

        # ── DIREITA: Lista do carrinho com scroll ────────────────────────
        cart_list_frame = tk.Frame(right, bg='white', relief='flat', bd=0,
                                   highlightbackground='#e2e8f0', highlightthickness=1)
        cart_list_frame.pack(fill='both', expand=True, pady=(4, 0))

        cart_cols = ('Produto', 'Qtd', 'Preço', 'Total')
        self.cart_listbox = ttk.Treeview(cart_list_frame, columns=cart_cols,
                                         show='headings', height=8,
                                         selectmode='browse')
        for col, w in zip(cart_cols, [0, 50, 80, 90]):
            self.cart_listbox.heading(col, text=col)
            if w == 0:
                self.cart_listbox.column(col, stretch=True, minwidth=100)
            else:
                self.cart_listbox.column(col, width=w, stretch=False)

        cart_vsb = ttk.Scrollbar(cart_list_frame, orient='vertical',
                                  command=self.cart_listbox.yview)
        self.cart_listbox.configure(yscrollcommand=cart_vsb.set)
        cart_vsb.pack(side='right', fill='y')
        self.cart_listbox.pack(fill='both', expand=True, padx=4, pady=4)

        # Produto selecionado
        self.pdv_selected_product_label = tk.Label(
            right, text="Produto selecionado: nenhum",
            font=self.fonts['small'], bg=self.colors['light'],
            fg='#475569', wraplength=pdv_right_w - 20, justify='left')
        self.pdv_selected_product_label.pack(fill='x', pady=(2, 0), padx=6)

        # ── DIREITA: Quantidade + teclado numérico ───────────────────────
        qty_frame = tk.Frame(right, bg='white', relief='flat', bd=0,
                             highlightbackground='#e2e8f0', highlightthickness=1)
        qty_frame.pack(fill='x', pady=(4, 0))

        qty_hdr = tk.Frame(qty_frame, bg='white')
        qty_hdr.pack(fill='x', padx=10, pady=(6, 2))
        tk.Label(qty_hdr, text="Quantidade:", font=self.fonts['small'],
                 bg='white').pack(side='left')

        self.pdv_qty_var = tk.IntVar(value=1)
        self.pdv_qty_entry = tk.Entry(qty_hdr, textvariable=self.pdv_qty_var,
                                      font=self.fonts['pdv_key'],
                                      justify='center', width=5)
        self.pdv_qty_entry.pack(side='left', padx=5, ipady=2)
        self.pdv_qty_entry.bind('<Return>', lambda e: self.add_to_cart())

        tk.Button(qty_hdr, text="▲", command=lambda: self.change_pdv_qty(1),
                  bg=self.colors['info'], fg='white', font=self.fonts['normal'],
                  bd=0, padx=6, cursor='hand2').pack(side='left', padx=1)
        tk.Button(qty_hdr, text="▼", command=lambda: self.change_pdv_qty(-1),
                  bg=self.colors['warning'], fg='white', font=self.fonts['normal'],
                  bd=0, padx=6, cursor='hand2').pack(side='left', padx=1)

        # Teclado numérico compacto
        keypad_frame = tk.Frame(qty_frame, bg='white')
        keypad_frame.pack(fill='x', padx=6, pady=(2, 6))
        keypad = [['7','8','9'], ['4','5','6'], ['1','2','3'], ['C','0','✔']]
        key_colors = {'C': self.colors['danger'], '✔': self.colors['success']}
        for row in keypad:
            rf = tk.Frame(keypad_frame, bg='white')
            rf.pack(fill='x')
            for k in row:
                bg = key_colors.get(k, '#f1f5f9')
                fg = 'white' if k in key_colors else self.colors['dark']
                tk.Button(rf, text=k, command=lambda x=k: self.on_pdv_keypad(x),
                          bg=bg, fg=fg, font=self.fonts['heading'],
                          width=4, height=1, bd=0, relief='flat', cursor='hand2',
                          highlightbackground='#e2e8f0',
                          highlightthickness=1).pack(side='left', expand=True,
                                                     fill='x', padx=2, pady=2)

        # ── DIREITA: Botões Adicionar / Remover ──────────────────────────
        btn_add_rm = tk.Frame(right, bg=self.colors['light'])
        btn_add_rm.pack(fill='x', pady=(4, 0))
        tk.Button(btn_add_rm, text="➕ Adicionar (Enter)", command=self.add_to_cart,
                  bg=self.colors['primary'], fg='white', font=self.fonts['normal'],
                  bd=0, height=2, cursor='hand2').pack(side='left', fill='x',
                                                       expand=True, padx=(0, 2))
        tk.Button(btn_add_rm, text="🗑️ Remover", command=self.remove_from_cart,
                  bg=self.colors['danger'], fg='white', font=self.fonts['normal'],
                  bd=0, height=2, cursor='hand2').pack(side='left', fill='x',
                                                       expand=True, padx=(2, 0))

        # ── DIREITA: Desconto + IVA ──────────────────────────────────────
        tax_frame = tk.Frame(right, bg='white', relief='flat', bd=0,
                             highlightbackground='#e2e8f0', highlightthickness=1)
        tax_frame.pack(fill='x', pady=(4, 0))

        tax_row1 = tk.Frame(tax_frame, bg='white')
        tax_row1.pack(fill='x', padx=10, pady=5)
        tk.Label(tax_row1, text="Desconto (%):", font=self.fonts['small'],
                 bg='white').pack(side='left')
        self.pdv_discount_var = tk.DoubleVar(value=0)
        tk.Spinbox(tax_row1, from_=0, to=100, textvariable=self.pdv_discount_var,
                   width=6, font=self.fonts['small']).pack(side='left', padx=5)
        self.pdv_discount_var.trace_add('write', lambda *a: self.update_cart_display())

        tax_row2 = tk.Frame(tax_frame, bg='white')
        tax_row2.pack(fill='x', padx=10, pady=(0, 5))
        self.pdv_apply_iva = tk.BooleanVar(value=True)
        tk.Checkbutton(tax_row2, text="Aplicar IVA (14%)", variable=self.pdv_apply_iva,
                       bg='white', font=self.fonts['small'],
                       command=self.update_cart_display).pack(side='left')
        self.pdv_add_tax = tk.BooleanVar(value=False)
        tk.Checkbutton(tax_row2, text="Taxa/Serviço", variable=self.pdv_add_tax,
                       bg='white', font=self.fonts['small'],
                       command=self.update_cart_display).pack(side='left', padx=10)

        # ── DIREITA: Pagamento ───────────────────────────────────────────
        pay_frame = tk.Frame(right, bg='white', relief='flat', bd=0,
                             highlightbackground='#e2e8f0', highlightthickness=1)
        pay_frame.pack(fill='x', pady=(4, 0))

        pay_r1 = tk.Frame(pay_frame, bg='white')
        pay_r1.pack(fill='x', padx=10, pady=5)
        tk.Label(pay_r1, text="💳 Pagamento:", font=self.fonts['small'],
                 bg='white').pack(side='left')
        self.pdv_payment_var = tk.StringVar(value="Dinheiro")
        pay_opts = ["Dinheiro", "Cartão Débito", "Cartão Crédito", "Cheque",
                    "Transferência", "Multicaixa", "Misto"]
        pay_menu = tk.OptionMenu(pay_r1, self.pdv_payment_var, *pay_opts)
        pay_menu.config(bg='white', fg=self.colors['dark'],
                        font=self.fonts['small'], highlightthickness=0, bd=0)
        pay_menu.pack(side='left', padx=5, fill='x', expand=True)

        pay_r2 = tk.Frame(pay_frame, bg='white')
        pay_r2.pack(fill='x', padx=10, pady=(0, 6))
        tk.Label(pay_r2, text="Valor Recebido:", font=self.fonts['small'],
                 bg='white').pack(side='left')
        self.pdv_received_var = tk.DoubleVar(value=0)
        self.pdv_received_entry = tk.Entry(pay_r2, textvariable=self.pdv_received_var,
                                           width=10, font=self.fonts['normal'])
        self.pdv_received_entry.pack(side='left', padx=5)
        self.pdv_received_var.trace_add('write', lambda *a: self.update_pdv_change())
        tk.Label(pay_r2, text="Troco:", font=self.fonts['small'],
                 bg='white').pack(side='left', padx=(8, 0))
        self.pdv_change_label = tk.Label(pay_r2, text="0.00",
                                          font=('Segoe UI', 12, 'bold'),
                                          bg='white', fg=self.colors['success'])
        self.pdv_change_label.pack(side='left', padx=5)

        # ── DIREITA: Totais ──────────────────────────────────────────────
        tot_frame = tk.Frame(right, bg='white', relief='flat', bd=0,
                             highlightbackground='#e2e8f0', highlightthickness=1)
        tot_frame.pack(fill='x', pady=(4, 0))

        for label_text, var_name in [("Subtotal:", "pdv_subtotal_label"),
                                      ("Desconto:", "pdv_discount_label"),
                                      ("IVA:", "pdv_iva_label"),
                                      ("Taxa:", "pdv_tax_label")]:
            row = tk.Frame(tot_frame, bg='white')
            row.pack(fill='x', padx=10, pady=2)
            tk.Label(row, text=label_text, font=self.fonts['small'],
                     bg='white', fg='#64748b').pack(side='left')
            lbl = tk.Label(row, text="0.00", font=self.fonts['small'],
                           bg='white', fg=self.colors['dark'])
            lbl.pack(side='right')
            setattr(self, var_name, lbl)

        total_bar = tk.Frame(tot_frame, bg=self.colors['primary'])
        total_bar.pack(fill='x', padx=0, pady=(4, 0))
        tk.Label(total_bar, text="TOTAL FINAL:", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['primary'], fg='white').pack(side='left', padx=12, pady=6)
        self.pdv_final_total_label = tk.Label(total_bar, text="AOA 0.00",
                                               font=('Segoe UI', 10, 'bold'),
                                               bg=self.colors['primary'],
                                               fg='#4ade80')
        self.pdv_final_total_label.pack(side='right', padx=12, pady=6)

        # Alias compatível com código legado
        self.cart_total_label = self.pdv_final_total_label

        # ── DIREITA: Botões de Ação finais ───────────────────────────────
        action_grid = tk.Frame(right, bg=self.colors['light'])
        action_grid.pack(fill='x', pady=5)
        action_grid.columnconfigure(0, weight=1)
        action_grid.columnconfigure(1, weight=1)

        btns_top = [
            ("✅ FINALIZAR (F)", self.pdv_finalize_with_dialog, self.colors['success']),
            ("❌ CANCELAR",      self.pdv_cancel_sale,          self.colors['danger']),
        ]
        btns_bot = [
            ("🧹 LIMPAR",       self.clear_cart,                self.colors['warning']),
            ("🖨️ IMPRIMIR",     self.pdv_print_receipt_shortcut,self.colors['info']),
        ]
        for col, (text, cmd, bg) in enumerate(btns_top):
            tk.Button(action_grid, text=text, command=cmd, bg=bg,
                      fg='white', font=self.fonts['heading'], height=2, bd=0,
                      cursor='hand2').grid(row=0, column=col, sticky='ew',
                                           padx=2, pady=2)
        for col, (text, cmd, bg) in enumerate(btns_bot):
            tk.Button(action_grid, text=text, command=cmd, bg=bg,
                      fg='white', font=self.fonts['heading'], height=2, bd=0,
                      cursor='hand2').grid(row=1, column=col, sticky='ew',
                                           padx=2, pady=2)

        self.load_pdv_products()
        PDVEnhancements.setup_focus_and_shortcuts(tab, self)

    def _update_pdv_clock(self):
        """Actualiza o relógio na barra do PDV a cada segundo."""
        try:
            now = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
            self._pdv_clock_var.set(now)
            self.root.after(1000, self._update_pdv_clock)
        except Exception:
            pass

    def _pdv_sort_tree(self, col):
        """Ordena a tabela de produtos pelo cabeçalho clicado."""
        try:
            items = [(self.products_tree.set(i, col), i)
                     for i in self.products_tree.get_children('')]
            items.sort()
            for idx, (_, item) in enumerate(items):
                self.products_tree.move(item, '', idx)
        except Exception:
            pass

    def load_pdv_products(self):
        if not hasattr(self, 'products_tree') or not self.products_tree:
            return
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        products = self.db.get_products()
        for idx, p in enumerate(products):
            if p.stock > 0:
                cat = self.db.get_category_by_id(p.category_id)
                cat_name = cat.name if cat else ""
                tag = ('odd' if idx % 2 == 0 else 'even')
                if p.stock <= p.min_stock:
                    tag = 'low'
                self.products_tree.insert('', 'end', tags=(tag,), values=(
                    p.id, p.code, p.name,
                    f"{currency} {p.price:.2f}", f"{p.stock:.0f}", cat_name
                ))

    def filter_pdv_products(self, event=None):
        if not hasattr(self, 'products_tree') or not self.products_tree:
            return
        search = self.pdv_search.get().lower() if hasattr(self, 'pdv_search') else ''
        sel_cat = self._pdv_cat_var.get() if hasattr(self, '_pdv_cat_var') else 'Todas'

        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        idx = 0
        for p in self.db.get_products():
            if p.stock <= 0:
                continue
            cat = self.db.get_category_by_id(p.category_id)
            cat_name = cat.name if cat else ""
            if sel_cat != "Todas" and cat_name != sel_cat:
                continue
            if search and search not in p.name.lower() and search not in p.code.lower():
                continue
            tag = ('odd' if idx % 2 == 0 else 'even')
            if p.stock <= p.min_stock:
                tag = 'low'
            self.products_tree.insert('', 'end', tags=(tag,), values=(
                p.id, p.code, p.name,
                f"{currency} {p.price:.2f}", f"{p.stock:.0f}", cat_name
            ))
            idx += 1

    def add_to_cart(self):
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return

        item = self.products_tree.item(selection[0])
        pid = item['values'][0]
        product = self.db.get_product_by_id(pid)

        try:
            qty = int(self.pdv_qty_var.get())
        except (ValueError, TypeError):
            qty = 1

        if qty <= 0:
            messagebox.showwarning("Quantidade inválida", "Informe uma quantidade válida.")
            return

        if qty > product.stock:
            messagebox.showwarning("Sem estoque", f"Estoque insuficiente. Disponível: {product.stock}")
            return

        if self.user_role == 'seller':
            total_temp = sum(i['total'] for i in self.cart) + (qty * product.price)
            allowed, msg = self.db.check_seller_limit(self.current_user.id, total_temp)
            if not allowed:
                messagebox.showerror("Limite Excedido", msg)
                return

        for cart_item in self.cart:
            if cart_item['id'] == pid:
                cart_item['quantity'] += qty
                cart_item['total'] = cart_item['quantity'] * cart_item['price']
                break
        else:
            self.cart.append({
                'id': pid, 'name': product.name, 'price': product.price,
                'quantity': qty, 'total': qty * product.price
            })

        self.pdv_qty_var.set(1)
        self.update_cart_display()
        self.update_status(f"Adicionado: {qty}x {product.name}")

    def on_pdv_product_select(self):
        selection = self.products_tree.selection()
        if not selection:
            self.pdv_selected_product_label.config(text="Produto selecionado: nenhum")
            return

        item = self.products_tree.item(selection[0])
        pid = item['values'][0]
        product = self.db.get_product_by_id(pid)
        if not product:
            self.pdv_selected_product_label.config(text="Produto selecionado: nenhum")
            return

        self.pdv_selected_product_label.config(
            text=f"Produto selecionado: {product.name} | Código: {product.code} | Preço: {product.price:.2f} | Estoque: {product.stock:.0f}"
        )

    def change_pdv_qty(self, delta):
        try:
            current = int(self.pdv_qty_var.get())
        except (ValueError, TypeError):
            current = 1
        next_qty = max(1, current + delta)
        self.pdv_qty_var.set(next_qty)

    def on_pdv_keypad(self, key):
        if key == 'C':
            self.pdv_qty_var.set(1)
            return
        if key == '✔':
            self.add_to_cart()
            return

        try:
            current = str(self.pdv_qty_var.get())
        except Exception:
            current = '0'

        if current == '0':
            new_value = key
        else:
            new_value = current + key

        try:
            self.pdv_qty_var.set(int(new_value))
        except ValueError:
            self.pdv_qty_var.set(1)

    def update_cart_display(self):
        # Limpar a Treeview do carrinho
        for item in self.cart_listbox.get_children():
            self.cart_listbox.delete(item)

        subtotal = 0
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for item in self.cart:
            self.cart_listbox.insert('', 'end', values=(
                item['name'][:28],
                f"{item['quantity']:.0f}",
                f"{item['price']:.2f}",
                f"{item['total']:.2f}"
            ))
            subtotal += item['total']

        # Calcular descontos e impostos
        discount_pct = self.pdv_discount_var.get()
        discount_amount = subtotal * (discount_pct / 100)
        subtotal_after_discount = subtotal - discount_amount

        iva_rate = (company.tax_rate if company else 0.0) if self.pdv_apply_iva.get() else 0
        iva_amount = subtotal_after_discount * iva_rate

        tax_amount = 0
        if self.pdv_add_tax.get():
            tax_amount = subtotal_after_discount * 0.05

        total = subtotal_after_discount + iva_amount + tax_amount

        # Atualizar labels
        self.pdv_subtotal_label.config(text=f"{currency} {subtotal:.2f}")
        self.pdv_discount_label.config(text=f"-{currency} {discount_amount:.2f}")
        self.pdv_iva_label.config(text=f"{currency} {iva_amount:.2f}")
        self.pdv_tax_label.config(text=f"{currency} {tax_amount:.2f}")
        self.pdv_final_total_label.config(text=f"{currency} {total:.2f}")
        self.cart_total_label.config(text=f"{currency} {total:.2f}")

        # Calcular troco
        try:
            received = self.pdv_received_var.get()
            change = received - total
            self.pdv_change_label.config(text=f"{currency} {max(0, change):.2f}")
        except (ValueError, TypeError):
            self.pdv_change_label.config(text="0.00")

    def pdv_select_client(self):
        client = self.select_client_dialog()
        if client:
            self.pdv_client_var.set(f"{client.name} ({client.nif})")
            self.pdv_current_client = client
        else:
            self.pdv_client_var.set("Consumidor Final")
            self.pdv_current_client = None

    def pdv_cancel_sale(self):
        if not self.cart:
            messagebox.showinfo("Aviso", "Carrinho já está vazio")
            return
        if messagebox.askyesno("Cancelar Venda", "Tem certeza que deseja cancelar esta venda?"):
            self.cart = []
            self.pdv_current_client = None
            self.pdv_last_receipt = None
            self.pdv_client_var.set("Consumidor Final")
            self.pdv_received_var.set(0)
            self.pdv_discount_var.set(0)
            self.pdv_apply_iva.set(True)
            self.pdv_add_tax.set(False)
            self.pdv_payment_var.set("Dinheiro")
            self.update_cart_display()
            self.update_status("Venda cancelada")

    def pdv_finalize_with_dialog(self):
        if not self.cart:
            messagebox.showwarning("Aviso", "Carrinho vazio!")
            return

        company = self.db.get_company()
        if not company:
            messagebox.showerror("Erro", "Configure a empresa primeiro!")
            return

        # Calcular totais
        self.update_cart_display()
        subtotal = sum(item['total'] for item in self.cart)
        discount_pct = self.pdv_discount_var.get()
        discount_amount = subtotal * (discount_pct / 100)
        subtotal_after_discount = subtotal - discount_amount

        iva_rate = (company.tax_rate if company else 0.0) if self.pdv_apply_iva.get() else 0
        iva_amount = subtotal_after_discount * iva_rate

        tax_amount = 0
        if self.pdv_add_tax.get():
            tax_amount = subtotal_after_discount * 0.05

        total = subtotal_after_discount + iva_amount + tax_amount

        # Obter cliente
        client = self.pdv_current_client if hasattr(self, 'pdv_current_client') and self.pdv_current_client else None
        if not client:
            client = Client(name="Consumidor Final", nif="999999999")
            client = self.db.create_client(client)

        # Criar venda
        sale = Sale(
            invoice_number=generate_invoice_number(),
            client_id=client.id,
            subtotal=subtotal,
            discount=discount_amount,
            tax=iva_amount + tax_amount,
            total=total,
            payment_method=self.pdv_payment_var.get(),
            status="completed",
            user_id=self.current_user.id,
            user_name=self.current_user.name
        )

        items = []
        for item in self.cart:
            items.append(SaleItem(
                product_id=item['id'],
                product_name=item['name'],
                quantity=item['quantity'],
                unit_price=item['price'],
                total_price=item['total']
            ))

        self.db.process_sale(sale, items)

        # Atualizar cliente
        if client.nif != "999999999":
            client.total_purchases += total
            client.purchase_count += 1
            client.last_purchase = datetime.datetime.now().isoformat()
            if client.purchase_count >= 100 and client.type != 'vip':
                client.type = 'vip'
            self.db.update_client(client)

        # Atualizar limite do vendedor
        if self.user_role == 'seller':
            self.db.add_seller_sales(self.current_user.id, total)

        # Guardar último comprovante para impressão rápida
        try:
            received = self.pdv_received_var.get()
        except (ValueError, TypeError):
            received = 0
        change = max(0, received - total)
        self.pdv_last_receipt = (sale, client, items, company, total, change)

        # Limpar carrinho
        self.cart = []
        self.pdv_client_var.set("Consumidor Final")
        self.pdv_received_var.set(0)
        self.pdv_discount_var.set(0)
        self.pdv_apply_iva.set(True)
        self.pdv_add_tax.set(False)
        self.pdv_payment_var.set("Dinheiro")
        self.update_cart_display()
        self.load_pdv_products()

        self.update_status(f"Venda #{sale.invoice_number} finalizada! Total: {company.currency} {total:.2f}")
        messagebox.showinfo("Sucesso", f"✅ Venda realizada!\n\nNF: {sale.invoice_number}\nTotal: {company.currency} {total:.2f}\nCliente: {client.name}\n\nPressione ENTER ou use o botão Imprimir para ver a fatura.")

    def pdv_print_receipt_shortcut(self):
        if hasattr(self, 'pdv_last_receipt') and self.pdv_last_receipt:
            sale, client, items, company, total, change = self.pdv_last_receipt
            self.print_receipt(sale, client, items, company, total, change)
        else:
            messagebox.showinfo("Imprimir", "Nenhuma venda recente para imprimir. Finalize uma venda primeiro.")

    def update_pdv_change(self):
        try:
            subtotal = sum(item['total'] for item in self.cart)
            discount_pct = self.pdv_discount_var.get()
            discount_amount = subtotal * (discount_pct / 100)
            subtotal_after_discount = subtotal - discount_amount

            company = self.db.get_company()
            iva_rate = (company.tax_rate if company else 0.0) if self.pdv_apply_iva.get() else 0
            iva_amount = subtotal_after_discount * iva_rate

            total = subtotal_after_discount + iva_amount + tax_amount
            received = self.pdv_received_var.get()
            change = received - total

            currency = company.currency if company else DEFAULT_CURRENCY
            self.pdv_change_label.config(text=f"{currency} {max(0, change):.2f}")
        except (ValueError, TypeError):
            self.pdv_change_label.config(text="0.00")



    def remove_from_cart(self):
        selection = self.cart_listbox.selection()
        if selection:
            idx = self.cart_listbox.index(selection[0])
            if 0 <= idx < len(self.cart):
                removed = self.cart.pop(idx)
                self.update_cart_display()
                self.update_status(f"Removido: {removed['name']}")

    def clear_cart(self):
        if messagebox.askyesno("Confirmar", "Limpar todo o carrinho?"):
            self.cart = []
            self.update_cart_display()
            self.update_status("Carrinho limpo")


    def print_receipt(self, sale, client, items, company, total, change):
        receipt = f"""
{'='*40}
{company.name.center(40)}
NIF: {company.nif}
Tel: {company.phone}
{'='*40}
NF: {sale.invoice_number}
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
Cliente: {client.name}
{'='*40}
Item                 Qtd   Preço
{'-'*40}"""
        for item in items:
            name = item.product_name[:20]
            receipt += f"\n{name:<20} {item.quantity:>4.0f} {item.unit_price:>8.2f}"

        receipt += f"""
{'-'*40}
Subtotal: {company.currency} {sale.subtotal:.2f}
IVA: {company.currency} {sale.tax:.2f}
TOTAL: {company.currency} {total:.2f}
Pagamento: {sale.payment_method}
{'-'*40}
Obrigado pela preferência!
{company.name.center(40)}
{'='*40}
        """
        # Mostrar comprovante
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Comprovante")
        receipt_window.geometry("450x550")
        text_widget = tk.Text(receipt_window, font=('Courier', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', receipt)
        text_widget.config(state='disabled')

    def select_client_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Selecionar Cliente")
        dialog.geometry("450x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Selecionar Cliente", font=self.fonts['heading']).pack(pady=10)

        # Busca
        search_frame = tk.Frame(dialog)
        search_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(search_frame, text="Buscar:").pack(side='left')
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)

        client_list = tk.Listbox(dialog, font=self.fonts['normal'], height=15)
        client_list.pack(fill='both', expand=True, padx=10, pady=5)

        def load_clients(search=""):
            client_list.delete(0, tk.END)
            for c in self.db.get_clients():
                if search.lower() in c.name.lower() or search in c.nif:
                    tipo = "⭐ VIP" if c.type == 'vip' else ""
                    client_list.insert(tk.END, f"{c.id} - {c.name} ({c.nif}) {tipo}")

        def on_search(event):
            load_clients(search_entry.get())

        search_entry.bind('<KeyRelease>', on_search)
        load_clients()

        result = None

        def new_client():
            nonlocal result
            new_dialog = tk.Toplevel(dialog)
            new_dialog.title("Novo Cliente")
            new_dialog.geometry("350x400")
            new_dialog.transient(dialog)
            new_dialog.grab_set()

            tk.Label(new_dialog, text="Novo Cliente", font=self.fonts['heading']).pack(pady=10)

            frame = tk.Frame(new_dialog)
            frame.pack(fill='both', expand=True, padx=20, pady=10)

            fields = [("Nome:", "name"), ("NIF:", "nif"), ("Telefone:", "phone"),
                      ("Email:", "email"), ("Endereço:", "address")]

            entries = {}
            for i, (label, key) in enumerate(fields):
                tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
                entry = tk.Entry(frame, width=35)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries[key] = entry

            def save():
                client = Client(
                    name=entries['name'].get(),
                    nif=entries['nif'].get(),
                    phone=entries['phone'].get(),
                    email=entries['email'].get(),
                    address=entries['address'].get()
                )
                result = self.db.create_client(client)
                load_clients()
                new_dialog.destroy()
                dialog.destroy()
                messagebox.showinfo("Sucesso", "Cliente cadastrado!")

            tk.Button(new_dialog, text="Salvar", command=save, bg=self.colors['success'], fg='white').pack(pady=20)

        def select():
            nonlocal result
            sel = client_list.curselection()
            if sel:
                text = client_list.get(sel[0])
                cid = int(text.split(' - ')[0])
                result = self.db.get_client_by_id(cid)
                dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(btn_frame, text="➕ Novo Cliente", command=new_client, bg=self.colors['info'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="✅ Selecionar", command=select, bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=dialog.destroy, bg=self.colors['danger'], fg='white').pack(side='right', padx=5)

        dialog.wait_window()
        return result

    def select_payment_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Forma de Pagamento")
        dialog.geometry("150x300")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Forma de Pagamento", font=self.fonts['heading']).pack(pady=20)

        result = tk.StringVar()
        payments = ["💰 Dinheiro", "💳 Cartão Débito", "💳 Cartão Crédito", "📱 PIX", "📋 Crediário", "📝 Cheque"]

        for p in payments:
            tk.Radiobutton(dialog, text=p, variable=result, value=p.split()[1],
                          font=self.fonts['normal']).pack(anchor='w', padx=40, pady=5)

        def confirm():
            if not result.get():
                messagebox.showwarning("Aviso", "Selecione uma forma de pagamento!")
                return
            dialog.destroy()

        tk.Button(dialog, text="Confirmar", command=confirm, bg=self.colors['success'], fg='white').pack(pady=20)
        dialog.wait_window()
        return result.get()

    # ========== PRODUTOS ==========
    def create_products_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Produtos")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Novo Produto", command=self.open_product_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="✏️ Editar", command=self.edit_product,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="🗑️ Excluir", command=self.delete_product,
                 bg=self.colors['danger'], fg='white').pack(side='left', padx=5)

        tk.Label(toolbar, text="Buscar:", bg=self.colors['light']).pack(side='left', padx=(20, 5))
        self.product_search = tk.Entry(toolbar, width=25)
        self.product_search.pack(side='left', padx=5)
        self.product_search.bind('<KeyRelease>', self.filter_products)

        columns = ('ID', 'Código', 'Nome', 'Categoria', 'Preço', 'Estoque', 'Mínimo')
        self.products_table = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.products_table.heading(col, text=col)
            if col == 'Nome':
                self.products_table.column(col, width=200)
            else:
                self.products_table.column(col, width=100)
        self.products_table.pack(fill='both', expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=self.products_table.yview)
        self.products_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)

        self.load_products()

    def load_products(self):
        if not hasattr(self, 'products_table') or not self.products_table:
            return
        for item in self.products_table.get_children():
            self.products_table.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for p in self.db.get_products():
            cat = self.db.get_category_by_id(p.category_id)
            cat_name = cat.name if cat else "Geral"
            self.products_table.insert('', 'end', values=(
                p.id, p.code, p.name, cat_name,
                f"{currency} {p.price:.2f}", f"{p.stock:.0f}", f"{p.min_stock:.0f}"
            ))

    def filter_products(self, event=None):
        if not hasattr(self, 'products_table') or not self.products_table:
            return
        search = self.product_search.get().lower()
        for item in self.products_table.get_children():
            self.products_table.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for p in self.db.get_products():
            if search in p.name.lower() or search in p.code.lower():
                cat = self.db.get_category_by_id(p.category_id)
                cat_name = cat.name if cat else "Geral"
                self.products_table.insert('', 'end', values=(
                    p.id, p.code, p.name, cat_name,
                    f"{currency} {p.price:.2f}", f"{p.stock:.0f}", f"{p.min_stock:.0f}"
                ))

    def open_product_dialog(self):
        # ... (código completo do método permanece igual)
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Produto")
        dialog.geometry("450x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Cadastro de Produto", font=self.fonts['heading']).pack(pady=10)

        nb = ttk.Notebook(dialog)
        nb.pack(fill='both', expand=True, padx=20, pady=10)

        basic_frame = ttk.Frame(nb)
        nb.add(basic_frame, text="📋 Básico")

        fields = [
            ("Nome:", "name"), ("Código:", "code"), ("Categoria:", "category"),
            ("Unidade:", "unit"), ("Preço de Venda:", "price"), ("Preço de Custo:", "cost"),
            ("Estoque Inicial:", "stock"), ("Estoque Mínimo:", "min_stock")
        ]

        entries = {}
        categories = self.db.get_categories()

        for i, (label, key) in enumerate(fields):
            tk.Label(basic_frame, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=5)

            if key == "category":
                entry = ttk.Combobox(basic_frame, values=[c.name for c in categories], state='readonly', width=35)
                if categories:
                    entry.set(categories[0].name)
            elif key == "unit":
                entry = ttk.Combobox(basic_frame, values=['UN', 'KG', 'G', 'L', 'ML', 'CX', 'PCT', 'PC'], state='readonly', width=35)
                entry.set('UN')
            else:
                entry = tk.Entry(basic_frame, width=37)
                if key == "code" and hasattr(self, 'barcode_entry') and self.barcode_entry:
                    entry.insert(0, self.barcode_entry.get())
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry

        extra_frame = ttk.Frame(nb)
        nb.add(extra_frame, text="🔧 Complementos")

        extra_fields = [("Marca:", "brand"), ("NCM:", "ncm")]
        for i, (label, key) in enumerate(extra_fields):
            tk.Label(extra_frame, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            entry = tk.Entry(extra_frame, width=37)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry

        tax_exempt_var = tk.BooleanVar()
        tk.Checkbutton(extra_frame, text="Isento de IVA", variable=tax_exempt_var).grid(row=len(extra_fields), column=0, columnspan=2, pady=10)

        def save():
            try:
                if not entries['name'].get().strip():
                    raise ValueError("Nome é obrigatório!")

                cat_name = entries['category'].get()
                category = self.db.get_category_by_name(cat_name)
                if not category:
                    category = self.db.create_category(cat_name)

                product = Product(
                    name=entries['name'].get().strip(),
                    code=entries['code'].get().strip() or str(uuid.uuid4())[:8],
                    category_id=category.id,
                    price=float(entries['price'].get() or 0),
                    cost=float(entries['cost'].get() or 0),
                    stock=float(entries['stock'].get() or 0),
                    min_stock=float(entries['min_stock'].get() or 0),
                    unit=entries['unit'].get(),
                    brand=entries['brand'].get(),
                    ncm=entries['ncm'].get(),
                    tax_exempt=tax_exempt_var.get()
                )
                self.db.create_product(product)
                self.load_products()
                self.load_pdv_products()
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Produto {product.name} cadastrado!")
                self.update_status(f"Produto {product.name} cadastrado")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="💾 Salvar", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def edit_product(self):
        selection = self.products_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return

        item = self.products_table.item(selection[0])
        pid = item['values'][0]
        product = self.db.get_product_by_id(pid)

        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Produto")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Editar Produto", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [
            ("Nome:", product.name), ("Código:", product.code),
            ("Preço:", product.price), ("Custo:", product.cost),
            ("Estoque:", product.stock), ("Mínimo:", product.min_stock),
            ("Unidade:", product.unit), ("Marca:", product.brand), ("NCM:", product.ncm)
        ]

        entries = {}
        for i, (label, value) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entry = tk.Entry(frame, width=35)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

        def update():
            product.name = entries['Nome:'].get()
            product.code = entries['Código:'].get()
            product.price = float(entries['Preço:'].get())
            product.cost = float(entries['Custo:'].get())
            product.stock = float(entries['Estoque:'].get())
            product.min_stock = float(entries['Mínimo:'].get())
            product.unit = entries['Unidade:'].get()
            product.brand = entries['Marca:'].get()
            product.ncm = entries['NCM:'].get()
            self.db.update_product(product)
            self.load_products()
            self.load_pdv_products()
            dialog.destroy()
            messagebox.showinfo("Sucesso", "Produto atualizado!")
            self.update_status(f"Produto {product.name} atualizado")

        tk.Button(dialog, text="Atualizar", command=update, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def delete_product(self):
        selection = self.products_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return
        if messagebox.askyesno("Confirmar", "Excluir este produto? Isso não pode ser desfeito!"):
            pid = self.products_table.item(selection[0])['values'][0]
            self.db.delete_product(pid)
            self.load_products()
            self.load_pdv_products()
            self.update_status("Produto excluído")

    # ========== CLIENTES ==========
    def create_clients_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👥 Clientes")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Novo Cliente", command=self.new_client_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="✏️ Editar", command=self.edit_client_dialog,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="🗑️ Excluir", command=self.delete_client,
                 bg=self.colors['danger'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Nome', 'NIF', 'Telefone', 'Email', 'Compras', 'Tipo')
        self.clients_table = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.clients_table.heading(col, text=col)
            if col == 'Nome':
                self.clients_table.column(col, width=150)
            elif col == 'Email':
                self.clients_table.column(col, width=150)
            else:
                self.clients_table.column(col, width=100)
        self.clients_table.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_clients()

    def load_clients(self):
        if not hasattr(self, 'clients_table') or not self.clients_table:
            return
        for item in self.clients_table.get_children():
            self.clients_table.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for c in self.db.get_clients():
            tipo = "⭐ VIP" if c.type == 'vip' else "Normal"
            self.clients_table.insert('', 'end', values=(
                c.id, c.name, c.nif, c.phone, c.email,
                f"{currency} {c.total_purchases:.2f}", tipo
            ))

    def new_client_dialog(self):
        # ... (código do método permanece igual)
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Cliente")
        dialog.geometry("450x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Novo Cliente", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [("Nome:", "name"), ("NIF:", "nif"), ("Telefone:", "phone"),
                  ("Email:", "email"), ("Endereço:", "address"), ("Limite de Crédito:", "credit_limit")]

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entry = tk.Entry(frame, width=35)
            if key == "credit_limit":
                entry.insert(0, "0")
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry

        def save():
            if not entries['name'].get().strip():
                messagebox.showerror("Erro", "Nome é obrigatório!")
                return

            client = Client(
                name=entries['name'].get().strip(),
                nif=entries['nif'].get(),
                phone=entries['phone'].get(),
                email=entries['email'].get(),
                address=entries['address'].get(),
                credit_limit=float(entries['credit_limit'].get() or 0)
            )
            self.db.create_client(client)
            self.load_clients()
            dialog.destroy()
            messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            self.update_status(f"Cliente {client.name} cadastrado")

        tk.Button(dialog, text="Salvar", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def edit_client_dialog(self):
        selection = self.clients_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente!")
            return

        item = self.clients_table.item(selection[0])
        cid = item['values'][0]
        client = self.db.get_client_by_id(cid)

        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Cliente")
        dialog.geometry("450x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"Editar Cliente: {client.name}", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [("Nome:", client.name), ("NIF:", client.nif), ("Telefone:", client.phone),
                  ("Email:", client.email), ("Endereço:", client.address), ("Limite de Crédito:", client.credit_limit)]

        entries = {}
        for i, (label, value) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entry = tk.Entry(frame, width=35)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

        def update():
            client.name = entries['Nome:'].get()
            client.nif = entries['NIF:'].get()
            client.phone = entries['Telefone:'].get()
            client.email = entries['Email:'].get()
            client.address = entries['Endereço:'].get()
            client.credit_limit = float(entries['Limite de Crédito:'].get())
            self.db.update_client(client)
            self.load_clients()
            dialog.destroy()
            messagebox.showinfo("Sucesso", "Cliente atualizado!")
            self.update_status(f"Cliente {client.name} atualizado")

        tk.Button(dialog, text="Atualizar", command=update, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def delete_client(self):
        selection = self.clients_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente!")
            return
        if messagebox.askyesno("Confirmar", "Excluir este cliente? Todas as vendas serão mantidas."):
            cid = self.clients_table.item(selection[0])['values'][0]
            self.db.delete_client(cid)
            self.load_clients()
            self.update_status("Cliente excluído")

    # ========== FORNECEDORES ==========
    def create_suppliers_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏢 Fornecedores")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Novo Fornecedor", command=self.new_supplier_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="✏️ Editar", command=self.edit_supplier_dialog,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="🗑️ Excluir", command=self.delete_supplier,
                 bg=self.colors['danger'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Nome', 'Telefone', 'Email', 'NIF', 'Contato')
        self.suppliers_table = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.suppliers_table.heading(col, text=col)
            self.suppliers_table.column(col, width=120)
        self.suppliers_table.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_suppliers()

    def load_suppliers(self):
        if not hasattr(self, 'suppliers_table') or not self.suppliers_table:
            return
        for item in self.suppliers_table.get_children():
            self.suppliers_table.delete(item)

        for s in self.db.get_suppliers():
            self.suppliers_table.insert('', 'end', values=(
                s.id, s.name, s.phone, s.email, s.tax_id, s.contact_person
            ))

    def new_supplier_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Fornecedor")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Novo Fornecedor", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [("Nome:", "name"), ("NIF:", "tax_id"), ("Telefone:", "phone"),
                  ("Email:", "email"), ("Endereço:", "address"), ("Pessoa de Contato:", "contact_person")]

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entry = tk.Entry(frame, width=35)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry

        def save():
            if not entries['name'].get().strip():
                messagebox.showerror("Erro", "Nome é obrigatório!")
                return

            supplier = Supplier(
                name=entries['name'].get().strip(),
                tax_id=entries['tax_id'].get(),
                phone=entries['phone'].get(),
                email=entries['email'].get(),
                address=entries['address'].get(),
                contact_person=entries['contact_person'].get()
            )
            self.db.create_supplier(supplier)
            self.load_suppliers()
            dialog.destroy()
            messagebox.showinfo("Sucesso", "Fornecedor cadastrado!")
            self.update_status(f"Fornecedor {supplier.name} cadastrado")

        tk.Button(dialog, text="Salvar", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def edit_supplier_dialog(self):
        selection = self.suppliers_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um fornecedor!")
            return

        item = self.suppliers_table.item(selection[0])
        sid = item['values'][0]
        supplier = self.db.get_supplier_by_id(sid)

        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Fornecedor")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"Editar Fornecedor: {supplier.name}", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [("Nome:", supplier.name), ("NIF:", supplier.tax_id), ("Telefone:", supplier.phone),
                  ("Email:", supplier.email), ("Endereço:", supplier.address), ("Contato:", supplier.contact_person)]

        entries = {}
        for i, (label, value) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entry = tk.Entry(frame, width=35)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

        def update():
            supplier.name = entries['Nome:'].get()
            supplier.tax_id = entries['NIF:'].get()
            supplier.phone = entries['Telefone:'].get()
            supplier.email = entries['Email:'].get()
            supplier.address = entries['Endereço:'].get()
            supplier.contact_person = entries['Contato:'].get()
            self.db.update_supplier(supplier)
            self.load_suppliers()
            dialog.destroy()
            messagebox.showinfo("Sucesso", "Fornecedor atualizado!")
            self.update_status(f"Fornecedor {supplier.name} atualizado")

        tk.Button(dialog, text="Atualizar", command=update, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def delete_supplier(self):
        selection = self.suppliers_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um fornecedor!")
            return
        if messagebox.askyesno("Confirmar", "Excluir este fornecedor?"):
            sid = self.suppliers_table.item(selection[0])['values'][0]
            self.db.delete_supplier(sid)
            self.load_suppliers()
            self.update_status("Fornecedor excluído")

    # ========== ORÇAMENTOS ==========
    def create_quotes_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📋 Orçamentos")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Novo Orçamento", command=self.new_quote,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="✅ Aprovar", command=self.approve_quote,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="🚫 Rejeitar", command=self.reject_quote,
                 bg=self.colors['danger'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Número', 'Cliente', 'Total', 'Status', 'Validade', 'Data')
        self.quotes_table = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.quotes_table.heading(col, text=col)
            self.quotes_table.column(col, width=120)
        self.quotes_table.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_quotes()

    def load_quotes(self):
        if not hasattr(self, 'quotes_table') or not self.quotes_table:
            return
        for item in self.quotes_table.get_children():
            self.quotes_table.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for q in self.db.get_quotes():
            status_icon = "⏳" if q.status == "Pendente" else "✅" if q.status == "Aprovado" else "❌"
            self.quotes_table.insert('', 'end', values=(
                q.id, q.number, q.client_name,
                f"{currency} {q.total_amount:.2f}",
                f"{status_icon} {q.status}",
                q.valid_until[:10] if q.valid_until else "-",
                q.created_at[:10] if q.created_at else "-"
            ))

    def new_quote(self):
        # Selecionar cliente
        client = self.select_client_dialog()
        if not client:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Novo Orçamento - {client.name}")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"Orçamento para: {client.name}", font=self.fonts['heading']).pack(pady=10)

        # Frame para itens
        items_frame = tk.LabelFrame(dialog, text="Itens do Orçamento")
        items_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ('Produto', 'Quantidade', 'Preço', 'Total', 'Ações')
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=10)
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=150)
        items_tree.pack(fill='both', expand=True)

        items = []

        def add_product():
            prod_dialog = tk.Toplevel(dialog)
            prod_dialog.title("Adicionar Produto")
            prod_dialog.geometry("500x400")
            prod_dialog.transient(dialog)
            prod_dialog.grab_set()

            tk.Label(prod_dialog, text="Selecione o Produto", font=self.fonts['heading']).pack(pady=10)

            listbox = tk.Listbox(prod_dialog, font=self.fonts['normal'], height=15)
            listbox.pack(fill='both', expand=True, padx=10, pady=5)

            for p in self.db.get_products():
                listbox.insert(tk.END, f"{p.id} - {p.name} - {p.price:.2f}")

            def select():
                sel = listbox.curselection()
                if sel:
                    text = listbox.get(sel[0])
                    pid = int(text.split(' - ')[0])
                    product = self.db.get_product_by_id(pid)

                    qty = simpledialog.askfloat("Quantidade", "Quantidade:", initialvalue=1, minvalue=0.1)
                    if qty:
                        total = qty * product.price
                        items.append({
                            'product_id': pid,
                            'name': product.name,
                            'quantity': qty,
                            'price': product.price,
                            'total': total
                        })
                        items_tree.insert('', 'end', values=(
                            product.name, f"{qty:.2f}", f"{product.price:.2f}", f"{total:.2f}", "❌"
                        ))
                        update_total()
                prod_dialog.destroy()

            tk.Button(prod_dialog, text="Adicionar", command=select, bg=self.colors['success'], fg='white').pack(pady=10)

        def remove_product():
            sel = items_tree.selection()
            if sel:
                idx = items_tree.index(sel[0])
                items.pop(idx)
                items_tree.delete(sel[0])
                update_total()

        def update_total():
            total = sum(i['total'] for i in items)
            total_label.config(text=f"Total: {currency} {total:.2f}")

        btn_frame = tk.Frame(items_frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="➕ Adicionar Produto", command=add_product, bg=self.colors['info'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Remover", command=remove_product, bg=self.colors['danger'], fg='white').pack(side='left', padx=5)

        # Validade
        validity_frame = tk.Frame(dialog)
        validity_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(validity_frame, text="Validade (dias):").pack(side='left')
        validity_entry = tk.Entry(validity_frame, width=10)
        validity_entry.insert(0, "30")
        validity_entry.pack(side='left', padx=5)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        total_label = tk.Label(dialog, text=f"Total: {currency} 0.00", font=self.fonts['heading'])
        total_label.pack(pady=10)

        def save_quote():
            if not items:
                messagebox.showwarning("Aviso", "Adicione pelo menos um item!")
                return

            valid_days = int(validity_entry.get())
            valid_until = (datetime.date.today() + datetime.timedelta(days=valid_days)).isoformat()
            total = sum(i['total'] for i in items)

            quote = Quote(
                number=generate_quote_number(),
                client_id=client.id,
                client_name=client.name,
                total_amount=total,
                status="Pendente",
                valid_until=valid_until,
                user_id=self.current_user.id,
                user_name=self.current_user.name
            )
            quote = self.db.create_quote(quote)

            for i in items:
                quote_item = QuoteItem(
                    quote_id=quote.id,
                    product_id=i['product_id'],
                    product_name=i['name'],
                    quantity=i['quantity'],
                    unit_price=i['price'],
                    total_price=i['total']
                )
                self.db.create_quote_item(quote_item)

            dialog.destroy()
            self.load_quotes()
            messagebox.showinfo("Sucesso", f"Orçamento {quote.number} criado!")
            self.update_status(f"Orçamento {quote.number} criado para {client.name}")

        tk.Button(dialog, text="Salvar Orçamento", command=save_quote, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def approve_quote(self):
        selection = self.quotes_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um orçamento!")
            return

        item = self.quotes_table.item(selection[0])
        qid = item['values'][0]
        quote = self.db.get_quote_by_id(qid)

        if quote.status != "Pendente":
            messagebox.showwarning("Aviso", "Este orçamento já foi processado!")
            return

        if messagebox.askyesno("Aprovar", f"Aprovar orçamento {quote.number} e converter em venda?"):
            sale = self.db.convert_quote_to_sale(qid)
            if sale:
                self.db.update_quote_status(qid, "Aprovado")
                self.load_quotes()
                messagebox.showinfo("Sucesso", f"Orçamento {quote.number} aprovado e convertido na venda {sale.invoice_number}")
                self.update_status(f"Orçamento {quote.number} convertido em venda")
            else:
                messagebox.showerror("Erro", "Erro ao converter orçamento!")

    def reject_quote(self):
        selection = self.quotes_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um orçamento!")
            return

        item = self.quotes_table.item(selection[0])
        qid = item['values'][0]
        quote = self.db.get_quote_by_id(qid)

        if messagebox.askyesno("Rejeitar", f"Rejeitar orçamento {quote.number}?"):
            self.db.update_quote_status(qid, "Rejeitado")
            self.load_quotes()
            messagebox.showinfo("Sucesso", f"Orçamento {quote.number} rejeitado!")
            self.update_status(f"Orçamento {quote.number} rejeitado")

    # ========== COMPRAS ==========
    def create_purchases_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Compras")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Nova Compra", command=self.new_purchase,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="✅ Receber", command=self.receive_purchase,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Número', 'Fornecedor', 'Total', 'Status', 'Data')
        self.purchases_table = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.purchases_table.heading(col, text=col)
            self.purchases_table.column(col, width=120)
        self.purchases_table.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_purchases()

    def load_purchases(self):
        if not hasattr(self, 'purchases_table') or not self.purchases_table:
            return
        for item in self.purchases_table.get_children():
            self.purchases_table.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for p in self.db.get_purchases():
            status_icon = "⏳" if p.status == "Pendente" else "✅"
            self.purchases_table.insert('', 'end', values=(
                p.id, p.number, p.supplier_name,
                f"{currency} {p.total_amount:.2f}",
                f"{status_icon} {p.status}",
                p.created_at[:10] if p.created_at else "-"
            ))

    def new_purchase(self):
        # Selecionar fornecedor
        supplier = self.select_supplier_dialog()
        if not supplier:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Nova Compra - {supplier.name}")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"Pedido de Compra - {supplier.name}", font=self.fonts['heading']).pack(pady=10)

        # Frame para itens
        items_frame = tk.LabelFrame(dialog, text="Itens da Compra")
        items_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ('Produto', 'Quantidade', 'Custo Unit.', 'Total', 'Ações')
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=10)
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=150)
        items_tree.pack(fill='both', expand=True)

        items = []

        def add_product():
            prod_dialog = tk.Toplevel(dialog)
            prod_dialog.title("Adicionar Produto")
            prod_dialog.geometry("500x400")
            prod_dialog.transient(dialog)
            prod_dialog.grab_set()

            tk.Label(prod_dialog, text="Selecione o Produto", font=self.fonts['heading']).pack(pady=10)

            listbox = tk.Listbox(prod_dialog, font=self.fonts['normal'], height=15)
            listbox.pack(fill='both', expand=True, padx=10, pady=5)

            for p in self.db.get_products():
                listbox.insert(tk.END, f"{p.id} - {p.name} - Custo: {p.cost:.2f}")

            def select():
                sel = listbox.curselection()
                if sel:
                    text = listbox.get(sel[0])
                    pid = int(text.split(' - ')[0])
                    product = self.db.get_product_by_id(pid)

                    qty = simpledialog.askfloat("Quantidade", "Quantidade:", initialvalue=1, minvalue=0.1)
                    if qty:
                        cost = simpledialog.askfloat("Custo", "Custo unitário:", initialvalue=product.cost, minvalue=0)
                        if cost:
                            total = qty * cost
                            items.append({
                                'product_id': pid,
                                'name': product.name,
                                'quantity': qty,
                                'cost': cost,
                                'total': total
                            })
                            items_tree.insert('', 'end', values=(
                                product.name, f"{qty:.2f}", f"{cost:.2f}", f"{total:.2f}", "❌"
                            ))
                            update_total()
                prod_dialog.destroy()

            tk.Button(prod_dialog, text="Adicionar", command=select, bg=self.colors['success'], fg='white').pack(pady=10)

        def remove_product():
            sel = items_tree.selection()
            if sel:
                idx = items_tree.index(sel[0])
                items.pop(idx)
                items_tree.delete(sel[0])
                update_total()

        def update_total():
            total = sum(i['total'] for i in items)
            total_label.config(text=f"Total: {currency} {total:.2f}")

        btn_frame = tk.Frame(items_frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="➕ Adicionar Produto", command=add_product, bg=self.colors['info'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Remover", command=remove_product, bg=self.colors['danger'], fg='white').pack(side='left', padx=5)

        # Forma de pagamento
        payment_frame = tk.Frame(dialog)
        payment_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(payment_frame, text="Forma de Pagamento:").pack(side='left')
        payment_var = tk.StringVar(value="À vista")
        payment_combo = ttk.Combobox(payment_frame, textvariable=payment_var,
                                     values=["À vista", "30 dias", "60 dias", "90 dias"],
                                     state='readonly', width=15)
        payment_combo.pack(side='left', padx=5)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        total_label = tk.Label(dialog, text=f"Total: {currency} 0.00", font=self.fonts['heading'])
        total_label.pack(pady=10)

        def save_purchase():
            if not items:
                messagebox.showwarning("Aviso", "Adicione pelo menos um item!")
                return

            total = sum(i['total'] for i in items)

            purchase = Purchase(
                number=generate_purchase_number(),
                supplier_id=supplier.id,
                supplier_name=supplier.name,
                total_amount=total,
                payment_method=payment_var.get(),
                status="Pendente",
                user_id=self.current_user.id,
                user_name=self.current_user.name
            )
            purchase = self.db.create_purchase(purchase)

            for i in items:
                purchase_item = PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=i['product_id'],
                    product_name=i['name'],
                    quantity=i['quantity'],
                    unit_cost=i['cost'],
                    total_cost=i['total']
                )
                self.db.create_purchase_item(purchase_item)

            dialog.destroy()
            self.load_purchases()
            messagebox.showinfo("Sucesso", f"Pedido de compra {purchase.number} criado!")
            self.update_status(f"Pedido de compra {purchase.number} criado para {supplier.name}")

        tk.Button(dialog, text="Salvar Pedido", command=save_purchase, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def select_supplier_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Selecionar Fornecedor")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Selecionar Fornecedor", font=self.fonts['heading']).pack(pady=10)

        supplier_list = tk.Listbox(dialog, font=self.fonts['normal'], height=15)
        supplier_list.pack(fill='both', expand=True, padx=10, pady=5)

        for s in self.db.get_suppliers():
            supplier_list.insert(tk.END, f"{s.id} - {s.name} (Contato: {s.contact_person})")

        result = None

        def select():
            nonlocal result
            sel = supplier_list.curselection()
            if sel:
                text = supplier_list.get(sel[0])
                sid = int(text.split(' - ')[0])
                result = self.db.get_supplier_by_id(sid)
                dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(btn_frame, text="✅ Selecionar", command=select, bg=self.colors['success'], fg='white').pack(side='right', padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=dialog.destroy, bg=self.colors['danger'], fg='white').pack(side='right', padx=5)

        dialog.wait_window()
        return result

    def receive_purchase(self):
        selection = self.purchases_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um pedido de compra!")
            return

        item = self.purchases_table.item(selection[0])
        pid = item['values'][0]
        purchase = self.db.get_purchase_by_id(pid)

        if purchase.status != "Pendente":
            messagebox.showwarning("Aviso", "Este pedido já foi recebido!")
            return

        if messagebox.askyesno("Receber", f"Confirmar recebimento do pedido {purchase.number}?\nIsso atualizará o estoque."):
            self.db.cursor.execute("UPDATE purchases SET status='Recebido' WHERE id=?", (pid,))
            self.db.conn.commit()
            self.load_purchases()
            messagebox.showinfo("Sucesso", f"Pedido {purchase.number} recebido com sucesso!")
            self.update_status(f"Pedido {purchase.number} recebido e estoque atualizado")

    # ========== DEVOLUÇÕES ==========
    def create_returns_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔄 Devoluções")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Nova Devolução", command=self.new_return,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Venda', 'Cliente', 'Total', 'Motivo', 'Status', 'Data')
        self.returns_table = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.returns_table.heading(col, text=col)
            self.returns_table.column(col, width=120)
        self.returns_table.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_returns()

    def load_returns(self):
        if not hasattr(self, 'returns_table') or not self.returns_table:
            return
        for item in self.returns_table.get_children():
            self.returns_table.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for r in self.db.get_returns():
            status_icon = "⏳" if r.status == "Pendente" else "✅"
            self.returns_table.insert('', 'end', values=(
                r.id, r.invoice_number, r.client_name,
                f"{currency} {r.total_amount:.2f}",
                r.reason[:30], f"{status_icon} {r.status}",
                r.created_at[:10] if r.created_at else "-"
            ))

    def new_return(self):
        # Selecionar venda
        sale = self.select_sale_for_return()
        if not sale:
            return

        # Obter itens da venda
        sale_items = self.db.get_sale_items(sale.id)
        if not sale_items:
            messagebox.showwarning("Aviso", "Esta venda não possui itens para devolução!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Devolução - Venda {sale.invoice_number}")
        dialog.geometry("700x500")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"Devolução - Venda {sale.invoice_number}", font=self.fonts['heading']).pack(pady=10)

        # Informações da venda
        info_frame = tk.Frame(dialog, bg=self.colors['light'], relief='groove', bd=1)
        info_frame.pack(fill='x', padx=10, pady=10)

        client = self.db.get_client_by_id(sale.client_id)
        client_name = client.name if client else "N/A"

        tk.Label(info_frame, text=f"Cliente: {client_name}", font=self.fonts['normal']).pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Data: {sale.created_at[:10] if sale.created_at else '-'}", font=self.fonts['normal']).pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Total Original: {sale.total:.2f}", font=self.fonts['normal']).pack(anchor='w', padx=10, pady=2)

        # Frame para itens
        items_frame = tk.LabelFrame(dialog, text="Itens para Devolução")
        items_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ('Produto', 'Quantidade Vendida', 'Quantidade a Devolver', 'Valor Unit.', 'Total')
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=8)
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=130)
        items_tree.pack(fill='both', expand=True)

        return_items = []
        entries = {}

        for item in sale_items:
            frame = tk.Frame(items_frame)
            frame.pack(fill='x', padx=5, pady=2)

            tk.Label(frame, text=item.product_name, width=30, anchor='w').pack(side='left')
            tk.Label(frame, text=str(int(item.quantity)), width=10).pack(side='left')

            qty_entry = tk.Entry(frame, width=10)
            qty_entry.insert(0, "0")
            qty_entry.pack(side='left', padx=5)

            entries[item.id] = {'entry': qty_entry, 'item': item, 'max': item.quantity}

        # Motivo
        reason_frame = tk.Frame(dialog)
        reason_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(reason_frame, text="Motivo da Devolução:").pack(anchor='w')
        reason_text = tk.Text(reason_frame, height=3, width=60)
        reason_text.pack(fill='x', pady=5)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        total_label = tk.Label(dialog, text=f"Total a Devolver: {currency} 0.00", font=self.fonts['heading'])
        total_label.pack(pady=10)

        def update_total():
            total = 0
            return_items.clear()
            for key, data in entries.items():
                try:
                    qty = float(data['entry'].get())
                    if qty > 0 and qty <= data['max']:
                        item_total = qty * data['item'].unit_price
                        total += item_total
                        return_items.append({
                            'product_id': data['item'].product_id,
                            'product_name': data['item'].product_name,
                            'quantity': qty,
                            'unit_price': data['item'].unit_price,
                            'total': item_total
                        })
                except:
                    pass
            total_label.config(text=f"Total a Devolver: {currency} {total:.2f}")
            return total

        def update_total_callback(event=None):
            update_total()

        for key, data in entries.items():
            data['entry'].bind('<KeyRelease>', update_total_callback)

        def save_return():
            total = update_total()
            if total == 0:
                messagebox.showwarning("Aviso", "Selecione pelo menos um item para devolução!")
                return

            reason = reason_text.get("1.0", tk.END).strip()
            if not reason:
                reason = "Devolução sem motivo especificado"

            # Criar devolução
            return_obj = Return(
                sale_id=sale.id,
                invoice_number=sale.invoice_number,
                client_id=sale.client_id,
                client_name=client_name,
                total_amount=total,
                reason=reason,
                status="Processada",
                user_id=self.current_user.id,
                user_name=self.current_user.name
            )
            return_obj = self.db.create_return(return_obj)

            # Criar itens da devolução e devolver ao estoque
            for item in return_items:
                return_item = ReturnItem(
                    return_id=return_obj.id,
                    product_id=item['product_id'],
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    total_price=item['total']
                )
                self.db.create_return_item(return_item)
                self.db.update_product_stock(item['product_id'], item['quantity'],
                                            reason=f"Devolução da venda #{sale.invoice_number}")

            dialog.destroy()
            self.load_returns()
            messagebox.showinfo("Sucesso", f"Devolução registrada! Total devolvido: {currency} {total:.2f}")
            self.update_status(f"Devolução da venda {sale.invoice_number} registrada")

        tk.Button(dialog, text="Registrar Devolução", command=save_return,
                 bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def select_sale_for_return(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Selecionar Venda para Devolução")
        dialog.geometry("700x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Selecione a Venda", font=self.fonts['heading']).pack(pady=10)

        columns = ('ID', 'NF', 'Cliente', 'Data', 'Total')
        sales_tree = ttk.Treeview(dialog, columns=columns, show='headings', height=15)
        for col in columns:
            sales_tree.heading(col, text=col)
            sales_tree.column(col, width=120)
        sales_tree.pack(fill='both', expand=True, padx=10, pady=10)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for s in self.db.get_sales():
            if s.status == "completed":
                client = self.db.get_client_by_id(s.client_id)
                client_name = client.name if client else "N/A"
                sales_tree.insert('', 'end', values=(
                    s.id, s.invoice_number, client_name,
                    s.created_at[:10] if s.created_at else "-",
                    f"{currency} {s.total:.2f}"
                ))

        result = None

        def select():
            nonlocal result
            sel = sales_tree.selection()
            if sel:
                item = sales_tree.item(sel[0])
                sid = item['values'][0]
                result = self.db.get_sale_by_id(sid)
                dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(btn_frame, text="✅ Selecionar", command=select, bg=self.colors['success'], fg='white').pack(side='right', padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=dialog.destroy, bg=self.colors['danger'], fg='white').pack(side='right', padx=5)

        dialog.wait_window()
        return result

    # ========== FINANCEIRO ==========
    def create_finance_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💰 Financeiro")

        # Resumo financeiro
        summary = self.db.get_financial_summary()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        summary_frame = tk.Frame(tab, bg=self.colors['light'])
        summary_frame.pack(fill='x', padx=10, pady=10)

        metrics = [
            ("💰 Receita Total", f"{currency} {summary['receita_total']:,.2f}", self.colors['success']),
            ("💸 Despesa Total", f"{currency} {summary['despesa_total']:,.2f}", self.colors['danger']),
            ("📈 Lucro Líquido", f"{currency} {summary['lucro_real']:,.2f}", self.colors['info']),
            ("🏦 Saldo Caixa", f"{currency} {summary['saldo_caixa']:,.2f}", self.colors['primary'])
        ]

        for i, (title, value, color) in enumerate(metrics):
            card = tk.Frame(summary_frame, bg='white', relief='raised', bd=1)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            summary_frame.grid_columnconfigure(i, weight=1)
            tk.Label(card, text=title, font=self.fonts['small'], bg='white', fg='gray').pack(pady=(10, 0))
            tk.Label(card, text=value, font=('Arial', 16, 'bold'), bg='white', fg=color).pack(pady=5)

        # Notebook para abas internas
        finance_nb = ttk.Notebook(tab)
        finance_nb.pack(fill='both', expand=True, padx=10, pady=10)

        # Aba: Transações
        trans_frame = ttk.Frame(finance_nb)
        finance_nb.add(trans_frame, text="📋 Transações")

        toolbar_trans = tk.Frame(trans_frame, bg=self.colors['light'])
        toolbar_trans.pack(fill='x', padx=10, pady=5)
        tk.Button(toolbar_trans, text="➕ Nova Transação", command=self.new_transaction,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)

        columns = ('Data', 'Tipo', 'Categoria', 'Descrição', 'Valor', 'Status')
        trans_tree = ttk.Treeview(trans_frame, columns=columns, show='headings', height=12)
        for col in columns:
            trans_tree.heading(col, text=col)
            trans_tree.column(col, width=120)
        trans_tree.pack(fill='both', expand=True, padx=10, pady=10)

        for t in self.db.get_transactions():
            icon = "💰" if t.type == "Entrada" else "💸"
            trans_tree.insert('', 'end', values=(
                t.created_at[:10] if t.created_at else "-",
                f"{icon} {t.type}", t.category, t.description[:30],
                f"{currency} {t.amount:.2f}", t.status
            ))

        # Aba: Despesas
        exp_frame = ttk.Frame(finance_nb)
        finance_nb.add(exp_frame, text="💸 Despesas")

        toolbar_exp = tk.Frame(exp_frame, bg=self.colors['light'])
        toolbar_exp.pack(fill='x', padx=10, pady=5)
        tk.Button(toolbar_exp, text="➕ Nova Despesa", command=self.open_expenses_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)

        columns_exp = ('Data', 'Categoria', 'Descrição', 'Valor', 'Vencimento', 'Status')
        exp_tree = ttk.Treeview(exp_frame, columns=columns_exp, show='headings', height=12)
        for col in columns_exp:
            exp_tree.heading(col, text=col)
            exp_tree.column(col, width=120)
        exp_tree.pack(fill='both', expand=True, padx=10, pady=10)

        for e in self.db.get_expenses():
            status = "✅ Pago" if e.paid else "⏳ Pendente"
            exp_tree.insert('', 'end', values=(
                e.created_at[:10] if e.created_at else "-",
                e.category, e.description[:30],
                f"{currency} {e.amount:.2f}",
                e.due_date[:10] if e.due_date else "-", status
            ))

    def new_transaction(self):
        # ... (código do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Nova Transação")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Nova Transação Financeira", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [
            ("Tipo:", "type", ["Entrada", "Saída"]),
            ("Categoria:", "category", ["Venda", "Salário", "Aluguel", "Fornecedor", "Imposto", "Outros"]),
            ("Descrição:", "description", None),
            ("Valor:", "amount", None),
            ("Forma de Pagamento:", "payment_method", ["Dinheiro", "Cartão", "Transferência", "PIX"]),
            ("Data Vencimento:", "due_date", None)
        ]

        entries = {}
        for i, (label, key, values) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            if values:
                entry = ttk.Combobox(frame, values=values, state='readonly', width=30)
                if key == "type":
                    entry.set("Entrada")
                elif key == "category":
                    entry.set("Venda")
                elif key == "payment_method":
                    entry.set("Dinheiro")
            else:
                entry = tk.Entry(frame, width=32)
                if key == "due_date":
                    entry.insert(0, datetime.date.today().isoformat())
                elif key == "amount":
                    entry.insert(0, "0")
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry

        def save():
            try:
                trans = Transaction(
                    type=entries['type'].get(),
                    category=entries['category'].get(),
                    description=entries['description'].get(),
                    amount=float(entries['amount'].get()),
                    payment_method=entries['payment_method'].get(),
                    status="Pendente",
                    due_date=entries['due_date'].get(),
                    user_id=self.current_user.id,
                    user_name=self.current_user.name
                )
                self.db.create_transaction(trans)
                dialog.destroy()
                messagebox.showinfo("Sucesso", "Transação registrada!")
                self.update_status(f"Transação {trans.type} de {trans.amount:.2f} registrada")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="Salvar", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def open_expenses_dialog(self):
        # ... (código do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Nova Despesa")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Nova Despesa", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        categories = ["Salário", "Aluguel", "Água", "Luz", "Internet", "Fornecedor", "Imposto", "Manutenção", "Outros"]

        fields = [
            ("Categoria:", "category", categories),
            ("Descrição:", "description", None),
            ("Valor:", "amount", None),
            ("Data Vencimento:", "due_date", None),
            ("Pago?", "paid", ["Sim", "Não"])
        ]

        entries = {}
        for i, (label, key, values) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            if values:
                entry = ttk.Combobox(frame, values=values, state='readonly', width=30)
                if key == "category":
                    entry.set(categories[0])
                elif key == "paid":
                    entry.set("Não")
            else:
                entry = tk.Entry(frame, width=32)
                if key == "due_date":
                    entry.insert(0, datetime.date.today().isoformat())
                elif key == "amount":
                    entry.insert(0, "0")
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry

        def save():
            try:
                expense = Expense(
                    category=entries['category'].get(),
                    description=entries['description'].get(),
                    amount=float(entries['amount'].get()),
                    due_date=entries['due_date'].get(),
                    paid=entries['paid'].get() == "Sim",
                    paid_date=datetime.date.today().isoformat() if entries['paid'].get() == "Sim" else "",
                    user_id=self.current_user.id,
                    user_name=self.current_user.name
                )
                self.db.create_expense(expense)
                dialog.destroy()
                messagebox.showinfo("Sucesso", "Despesa registrada!")
                self.update_status(f"Despesa de {expense.amount:.2f} registrada")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="Salvar", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    # ========== RELATÓRIOS ==========
    def create_reports_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📈 Relatórios")

        # Frame rolável
        canvas = tk.Canvas(tab, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.colors['light'])

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Título
        tk.Label(scrollable, text="Relatórios do Sistema", font=self.fonts['title'],
                bg=self.colors['light'], fg=self.colors['dark']).pack(pady=20)

        btn_frame = tk.Frame(scrollable, bg=self.colors['light'])
        btn_frame.pack(expand=True, fill='both', padx=40, pady=20)

        reports = [
            ("📊 Vendas por Período", self.sales_period_report),
            ("📦 Produtos Mais Vendidos", self.top_products_report),
            ("💰 Fluxo de Caixa", self.cashflow_report),
            ("👥 Clientes VIP", self.vip_clients_report),
            ("⚠️ Estoque Baixo", self.low_stock_report),
            ("📤 Exportar Vendas", self.export_sales_excel),
            ("📄 Relatório Geral", self.general_report)
        ]

        for i, (text, cmd) in enumerate(reports):
            btn = tk.Button(btn_frame, text=text, command=cmd,
                           bg=self.colors['primary'], fg='white',
                           font=self.fonts['heading'], padx=30, pady=15, width=25)
            btn.grid(row=i//2, column=i%2, padx=20, pady=15, sticky='nsew')

        btn_frame.grid_rowconfigure(0, weight=1)
        btn_frame.grid_rowconfigure(1, weight=1)
        btn_frame.grid_rowconfigure(2, weight=1)
        btn_frame.grid_rowconfigure(3, weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

    def sales_period_report(self):
        start = simpledialog.askstring("Período", "Data inicial (YYYY-MM-DD):",
                                       initialvalue=datetime.date.today().replace(day=1).isoformat())
        end = simpledialog.askstring("Período", "Data final (YYYY-MM-DD):",
                                     initialvalue=datetime.date.today().isoformat())

        if start and end:
            sales = self.db.get_sales_by_period(start, end)
            company = self.db.get_company()
            currency = company.currency if company else DEFAULT_CURRENCY

            report = f"RELATÓRIO DE VENDAS\nPeríodo: {start} a {end}\n{'='*60}\n\n"
            total = 0
            for s in sales:
                client = self.db.get_client_by_id(s.client_id)
                client_name = client.name if client else "N/A"
                report += f"NF: {s.invoice_number} | Cliente: {client_name} | Data: {s.created_at[:10]} | Total: {currency} {s.total:.2f}\n"
                total += s.total

            report += f"\n{'='*60}\n"
            report += f"Total de Vendas: {len(sales)}\n"
            report += f"Valor Total: {currency} {total:,.2f}\n"
            report += f"Ticket Médio: {currency} {total/len(sales) if sales else 0:.2f}\n"

            self.show_report_window("Relatório de Vendas", report)

    def stock_report(self):
        products = self.db.get_products()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        report = "RELATÓRIO DE ESTOQUE ATUAL\n" + "="*60 + "\n\n"
        report += f"{'Produto':<35} {'Estoque':>10} {'Mínimo':>10} {'Valor Estoque':>15}\n"
        report += "-"*70 + "\n"

        total_value = 0
        for p in products:
            value = p.stock * p.cost
            total_value += value
            report += f"{p.name[:35]:<35} {p.stock:>10.0f} {p.min_stock:>10.0f} {currency} {value:>12,.2f}\n"

        report += "-"*70 + "\n"
        report += f"VALOR TOTAL DO ESTOQUE: {currency} {total_value:,.2f}\n"

        self.show_report_window("Relatório de Estoque", report)

    def top_products_report(self):
        query = """
            SELECT product_name, SUM(quantity) as total_qtd, SUM(total_price) as total_valor
            FROM sale_items
            GROUP BY product_name
            ORDER BY total_qtd DESC
            LIMIT 10
        """
        results = self.db.cursor.execute(query).fetchall()

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        report = f"TOP 10 PRODUTOS MAIS VENDIDOS\n{'='*60}\n\n"
        report += f"{'Produto':<35} {'Quantidade':>12} {'Faturamento':>15}\n"
        report += "-"*62 + "\n"

        for row in results:
            report += f"{row['product_name'][:35]:<35} {row['total_qtd']:>12.0f} {currency} {row['total_valor']:>12,.2f}\n"

        self.show_report_window("Produtos Mais Vendidos", report)

    def cashflow_report(self):
        summary = self.db.get_financial_summary()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        report = f"FLUXO DE CAIXA\n{'='*50}\n\n"
        report += f"Entradas (Receitas):     {currency} {summary['receita_total']:>12,.2f}\n"
        report += f"Saídas (Despesas):       {currency} {summary['despesa_total']:>12,.2f}\n"
        report += "-"*50 + "\n"
        report += f"SALDO LÍQUIDO:           {currency} {summary['lucro_real']:>12,.2f}\n\n"

        report += "\nÚLTIMAS TRANSAÇÕES:\n" + "-"*50 + "\n"
        for t in self.db.get_transactions()[:10]:
            icon = "→" if t.type == "Entrada" else "←"
            report += f"{icon} {t.created_at[:10]} | {t.category} | {currency} {t.amount:.2f} | {t.status}\n"

        self.show_report_window("Fluxo de Caixa", report)

    def vip_clients_report(self):
        vips = self.db.get_vip_clients()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        report = f"CLIENTES VIP\n{'='*50}\n\n"
        if not vips:
            report += "Nenhum cliente VIP encontrado.\nClientes se tornam VIP após 100 compras.\n"
        else:
            report += f"{'Nome':<30} {'Compras':>8} {'Total Gasto':>15}\n"
            report += "-"*55 + "\n"
            for c in vips:
                report += f"{c.name[:30]:<30} {c.purchase_count:>8} {currency} {c.total_purchases:>12,.2f}\n"

        self.show_report_window("Clientes VIP", report)

    def low_stock_report(self):
        products = self.db.get_products_low_stock()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        report = f"PRODUTOS COM ESTOQUE BAIXO\n{'='*50}\n\n"
        if not products:
            report += "✅ Todos os produtos estão com estoque adequado!\n"
        else:
            report += f"{'Produto':<35} {'Estoque':>10} {'Mínimo':>10} {'Status':>12}\n"
            report += "-"*70 + "\n"
            for p in products:
                status = "CRÍTICO" if p.stock <= p.min_stock * 0.3 else "ATENÇÃO"
                report += f"{p.name[:35]:<35} {p.stock:>10.0f} {p.min_stock:>10.0f} {status:>12}\n"

        self.show_report_window("Estoque Baixo", report)

    def general_report(self):
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        total_products = len(self.db.get_products())
        total_clients = len(self.db.get_clients())
        total_sales = len(self.db.get_sales())
        total_revenue = sum(s.total for s in self.db.get_sales())
        low_stock = len(self.db.get_products_low_stock())
        vips = len(self.db.get_vip_clients())

        report = f"RELATÓRIO GERAL DO SISTEMA\n{'='*60}\n"
        report += f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        report += f"Empresa: {company.name if company else 'N/A'}\n"
        report += f"Nível: {company.level if company else 'N/A'}\n\n"

        report += "📊 RESUMO GERAL\n"
        report += f"• Produtos cadastrados: {total_products}\n"
        report += f"• Clientes cadastrados: {total_clients}\n"
        report += f"• Clientes VIP: {vips}\n"
        report += f"• Vendas realizadas: {total_sales}\n"
        report += f"• Faturamento total: {currency} {total_revenue:,.2f}\n"
        report += f"• Produtos com estoque baixo: {low_stock}\n\n"

        report += "📈 MÉTRICAS\n"
        report += f"• Ticket médio: {currency} {total_revenue/total_sales if total_sales else 0:.2f}\n"

        self.show_report_window("Relatório Geral", report)

    def export_sales_excel(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if filename:
            sales = self.db.get_sales()
            company = self.db.get_company()
            currency = company.currency if company else DEFAULT_CURRENCY

            with open(filename, 'w', encoding='utf-8-sig') as f:
                f.write("NF;Cliente;Data;Total;Forma Pagamento;Status\n")
                for s in sales:
                    client = self.db.get_client_by_id(s.client_id)
                    client_name = client.name if client else "N/A"
                    f.write(f"{s.invoice_number};{client_name};{s.created_at[:10] if s.created_at else '-'};{currency} {s.total:.2f};{s.payment_method};{s.status}\n")

            messagebox.showinfo("Sucesso", f"Vendas exportadas para {filename}")
            self.update_status(f"Relatório de vendas exportado")

    def show_report_window(self, title, content):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("800x600")
        dialog.transient(self.root)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        text_widget = tk.Text(frame, font=('Courier', 10), wrap='word')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        text_widget.insert('1.0', content)
        text_widget.config(state='disabled')

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)

        def save_report():
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt")])
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Sucesso", f"Relatório salvo em {filename}")

        def print_report():
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(content)
                temp_file = f.name
            if platform.system() == 'Windows':
                os.startfile(temp_file, "print")
            else:
                subprocess.call(['lp', temp_file])

        tk.Button(btn_frame, text="💾 Salvar", command=save_report, bg=self.colors['info'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🖨️ Imprimir", command=print_report, bg=self.colors['warning'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Fechar", command=dialog.destroy, bg=self.colors['danger'], fg='white').pack(side='right', padx=5)

    # ========== PRODUÇÃO ==========
    def create_production_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Produção")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Nova Ordem", command=self.new_production_order_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="✅ Concluir", command=self.complete_production_order,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Nº OP', 'Produto', 'Quantidade', 'Status', 'Início', 'Fim')
        self.production_table = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.production_table.heading(col, text=col)
            self.production_table.column(col, width=120)
        self.production_table.column('Produto', width=200)
        self.production_table.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_production_orders()

    def load_production_orders(self):
        if not hasattr(self, 'production_table') or not self.production_table:
            return
        for item in self.production_table.get_children():
            self.production_table.delete(item)

        for po in self.db.get_production_orders():
            status_icon = "⏳" if po.status == "Planejada" else "🔧" if po.status == "Em Produção" else "✅"
            self.production_table.insert('', 'end', values=(
                po.id, po.number, po.product_name, f"{po.quantity:.0f}",
                f"{status_icon} {po.status}",
                po.start_date[:10] if po.start_date else "-",
                po.end_date[:10] if po.end_date else "-"
            ))

    def new_production_order_dialog(self):
        # ... (código do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Nova Ordem de Produção")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Nova Ordem de Produção", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Produto
        tk.Label(frame, text="Produto:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(frame, textvariable=product_var, state='readonly', width=35)
        products = self.db.get_products()
        product_combo['values'] = [f"{p.id} - {p.name}" for p in products]
        product_combo.grid(row=0, column=1, padx=5, pady=5)

        # Quantidade
        tk.Label(frame, text="Quantidade:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        qty_entry = tk.Entry(frame, width=35)
        qty_entry.insert(0, "1")
        qty_entry.grid(row=1, column=1, padx=5, pady=5)

        # Data início
        tk.Label(frame, text="Data Início:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        start_entry = tk.Entry(frame, width=35)
        start_entry.insert(0, datetime.date.today().isoformat())
        start_entry.grid(row=2, column=1, padx=5, pady=5)

        # Status
        tk.Label(frame, text="Status:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        status_var = tk.StringVar(value="Planejada")
        status_combo = ttk.Combobox(frame, textvariable=status_var,
                                   values=["Planejada", "Em Produção"], state='readonly', width=33)
        status_combo.grid(row=3, column=1, padx=5, pady=5)

        # Verificar BOM
        bom_frame = tk.LabelFrame(dialog, text="Lista de Materiais (BOM)")
        bom_frame.pack(fill='both', expand=True, padx=20, pady=10)

        bom_tree = ttk.Treeview(bom_frame, columns=('Componente', 'Quantidade', 'Unidade'), show='headings', height=5)
        for col in ('Componente', 'Quantidade', 'Unidade'):
            bom_tree.heading(col, text=col)
            bom_tree.column(col, width=130)
        bom_tree.pack(fill='both', expand=True, padx=5, pady=5)

        def update_bom(*args):
            for item in bom_tree.get_children():
                bom_tree.delete(item)

            prod_text = product_var.get()
            if prod_text:
                pid = int(prod_text.split(' - ')[0])
                bom_items = self.db.get_bom_by_product_id(pid)
                for bom in bom_items:
                    bom_tree.insert('', 'end', values=(bom.component_name, f"{bom.quantity}", ""))

            if bom_tree.get_children():
                bom_frame.config(text="Lista de Materiais (BOM) - Componentes Necessários")
            else:
                bom_frame.config(text="Lista de Materiais (BOM) - Nenhum componente cadastrado")

        product_var.trace_add('write', update_bom)

        def save():
            prod_text = product_var.get()
            if not prod_text:
                messagebox.showwarning("Aviso", "Selecione um produto!")
                return

            try:
                pid = int(prod_text.split(' - ')[0])
                product = self.db.get_product_by_id(pid)
                qty = float(qty_entry.get())
                start = start_entry.get()
                status = status_var.get()

                po = ProductionOrder(
                    number=generate_op_number(),
                    product_id=pid,
                    product_name=product.name,
                    quantity=qty,
                    status=status,
                    start_date=start,
                    user_id=self.current_user.id,
                    user_name=self.current_user.name
                )
                self.db.create_production_order(po)

                dialog.destroy()
                self.load_production_orders()
                messagebox.showinfo("Sucesso", f"Ordem de Produção {po.number} criada!")
                self.update_status(f"OP {po.number} criada para {product.name}")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="Criar Ordem", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def complete_production_order(self):
        selection = self.production_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma ordem de produção!")
            return

        item = self.production_table.item(selection[0])
        po_id = item['values'][0]
        po = self.db.get_production_order_by_id(po_id)

        if po.status == "Concluída":
            messagebox.showwarning("Aviso", "Esta ordem já está concluída!")
            return

        if messagebox.askyesno("Concluir", f"Confirmar conclusão da OP {po.number}?\nIsso atualizará o estoque do produto."):
            self.db.update_production_order_status(po_id, "Concluída")
            self.load_production_orders()
            messagebox.showinfo("Sucesso", f"OP {po.number} concluída! Estoque atualizado.")
            self.update_status(f"OP {po.number} concluída - Estoque de {po.product_name} atualizado")

    # ========== BOM ==========
    def create_bom_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📋 BOM")

        select_frame = tk.Frame(tab, bg=self.colors['light'])
        select_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(select_frame, text="Produto:").pack(side='left')
        self.bom_product_var = tk.StringVar()
        self.bom_product_combo = ttk.Combobox(select_frame, textvariable=self.bom_product_var,
                                              state='readonly', width=40)
        products = self.db.get_products()
        self.bom_product_combo['values'] = [f"{p.id} - {p.name}" for p in products]
        self.bom_product_combo.pack(side='left', padx=10)
        self.bom_product_combo.bind('<<ComboboxSelected>>', self.load_bom_for_product)

        tk.Button(select_frame, text="➕ Adicionar Componente", command=self.add_bom_component,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Componente', 'Quantidade', 'Unidade', 'Ações')
        self.bom_tree = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.bom_tree.heading(col, text=col)
            self.bom_tree.column(col, width=150)
        self.bom_tree.column('Componente', width=250)
        self.bom_tree.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Button(tab, text="🗑️ Remover Selecionado", command=self.remove_bom_component,
                 bg=self.colors['danger'], fg='white').pack(pady=5)

    def load_bom_for_product(self, event=None):
        if not hasattr(self, 'bom_tree') or not self.bom_tree:
            return
        for item in self.bom_tree.get_children():
            self.bom_tree.delete(item)

        prod_text = self.bom_product_var.get()
        if prod_text:
            pid = int(prod_text.split(' - ')[0])
            bom_items = self.db.get_bom_by_product_id(pid)
            for bom in bom_items:
                comp = self.db.get_product_by_id(bom.component_id)
                unit = comp.unit if comp else "UN"
                self.bom_tree.insert('', 'end', values=(
                    bom.id, bom.component_name, f"{bom.quantity}", unit, "❌"
                ))

    def add_bom_component(self):
        prod_text = self.bom_product_var.get()
        if not prod_text:
            messagebox.showwarning("Aviso", "Selecione um produto primeiro!")
            return

        product_id = int(prod_text.split(' - ')[0])

        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Componente à BOM")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Adicionar Componente", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(frame, text="Componente:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        component_var = tk.StringVar()
        component_combo = ttk.Combobox(frame, textvariable=component_var, state='readonly', width=35)

        components = [p for p in self.db.get_products() if p.id != product_id]
        component_combo['values'] = [f"{p.id} - {p.name}" for p in components]
        component_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Quantidade:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        qty_entry = tk.Entry(frame, width=35)
        qty_entry.insert(0, "1")
        qty_entry.grid(row=1, column=1, padx=5, pady=5)

        def save():
            comp_text = component_var.get()
            if not comp_text:
                messagebox.showwarning("Aviso", "Selecione um componente!")
                return

            try:
                comp_id = int(comp_text.split(' - ')[0])
                qty = float(qty_entry.get())

                bom = BillOfMaterial(
                    product_id=product_id,
                    component_id=comp_id,
                    quantity=qty
                )
                self.db.add_bom_item(bom)

                dialog.destroy()
                self.load_bom_for_product()
                messagebox.showinfo("Sucesso", "Componente adicionado à BOM!")
                self.update_status(f"Componente adicionado à BOM do produto")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="Adicionar", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def remove_bom_component(self):
        selection = self.bom_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um componente para remover!")
            return

        item = self.bom_tree.item(selection[0])
        bom_id = item['values'][0]

        if messagebox.askyesno("Confirmar", "Remover este componente da BOM?"):
            self.db.delete_bom_item(bom_id)
            self.load_bom_for_product()
            messagebox.showinfo("Sucesso", "Componente removido!")
            self.update_status("Componente removido da BOM")

    # ========== MOVIMENTAÇÕES DE ESTOQUE ==========
    def create_stock_movements_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Movimentações")

        filter_frame = tk.Frame(tab, bg=self.colors['light'])
        filter_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(filter_frame, text="Produto:").pack(side='left')
        self.movement_product_var = tk.StringVar()
        product_combo = ttk.Combobox(filter_frame, textvariable=self.movement_product_var, width=30)

        products = self.db.get_products()
        product_combo['values'] = ["Todos"] + [f"{p.id} - {p.name}" for p in products]
        product_combo.set("Todos")
        product_combo.pack(side='left', padx=10)
        product_combo.bind('<<ComboboxSelected>>', self.load_stock_movements)

        tk.Button(filter_frame, text="🔍 Filtrar", command=self.load_stock_movements,
                 bg=self.colors['info'], fg='white').pack(side='left', padx=5)

        columns = ('Data', 'Produto', 'Tipo', 'Quantidade', 'Estoque Anterior', 'Novo Estoque', 'Motivo')
        self.movements_tree = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.movements_tree.heading(col, text=col)
            self.movements_tree.column(col, width=120)
        self.movements_tree.column('Produto', width=200)
        self.movements_tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_stock_movements()

    def load_stock_movements(self, event=None):
        if not hasattr(self, 'movements_tree') or not self.movements_tree:
            return
        for item in self.movements_tree.get_children():
            self.movements_tree.delete(item)

        prod_text = self.movement_product_var.get() if hasattr(self, 'movement_product_var') else "Todos"

        if prod_text and prod_text != "Todos":
            try:
                product_id = int(prod_text.split(' - ')[0])
                movements = self.db.get_stock_movements(product_id=product_id, limit=200)
            except:
                movements = self.db.get_stock_movements(limit=200)
        else:
            movements = self.db.get_stock_movements(limit=200)

        for m in movements:
            icon = "📥" if m.type == "entrada" else "📤" if m.type == "saida" else "📝"
            self.movements_tree.insert('', 'end', values=(
                m.created_at[:16] if m.created_at else "-",
                m.product_name,
                f"{icon} {m.type}",
                f"{m.quantity:.2f}",
                f"{m.old_stock:.2f}",
                f"{m.new_stock:.2f}",
                m.reason[:40] if m.reason else "-"
            ))

    # ========== VENDEDORES ==========
    def create_sellers_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👥 Vendedores")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Novo Vendedor", command=self.new_seller_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="✏️ Editar Limites", command=self.edit_seller_limits,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Nome', 'Email', 'Limite Diário', 'Limite Mensal', 'Vendas Hoje', 'Status')
        self.sellers_tree = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.sellers_tree.heading(col, text=col)
            self.sellers_tree.column(col, width=120)
        self.sellers_tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_sellers_list()

    def load_sellers_list(self):
        if not hasattr(self, 'sellers_tree') or not self.sellers_tree:
            return
        for item in self.sellers_tree.get_children():
            self.sellers_tree.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for s in self.db.get_sellers():
            limit = self.db.get_seller_limit(s.id)
            if limit:
                status = "🟢 Ativo" if limit.current_daily_sales < limit.daily_limit else "🔴 Bloqueado"
                self.sellers_tree.insert('', 'end', values=(
                    s.id, s.name, s.email,
                    f"{currency} {limit.daily_limit:,.2f}",
                    f"{currency} {limit.monthly_limit:,.2f}",
                    f"{currency} {limit.current_daily_sales:,.2f}",
                    status
                ))

    def new_seller_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Vendedor")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Novo Vendedor", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [("Nome:", "name"), ("Email:", "email"), ("Telefone:", "phone"),
                  ("Senha:", "password"), ("Confirmar Senha:", "confirm"),
                  ("Limite Diário (AOA):", "daily_limit"), ("Limite Mensal (AOA):", "monthly_limit")]

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            if "senha" in key.lower() or key == "confirm":
                entry = tk.Entry(frame, show="*", width=35)
            elif key in ["daily_limit", "monthly_limit"]:
                entry = tk.Entry(frame, width=35)
                entry.insert(0, "50000" if key == "daily_limit" else "200000")
            else:
                entry = tk.Entry(frame, width=35)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry

        def save():
            name = entries['name'].get().strip()
            email = entries['email'].get().strip()
            password = entries['password'].get()
            confirm = entries['confirm'].get()
            phone = entries['phone'].get()
            daily = float(entries['daily_limit'].get())
            monthly = float(entries['monthly_limit'].get())

            if not name or not email:
                messagebox.showerror("Erro", "Nome e email são obrigatórios!")
                return
            if password != confirm:
                messagebox.showerror("Erro", "As senhas não coincidem!")
                return
            if len(password) < 4:
                messagebox.showerror("Erro", "A senha deve ter pelo menos 4 caracteres!")
                return

            user = User(
                name=name,
                email=email,
                password=password,
                phone=phone,
                role="seller",
                first_login=True
            )
            user = self.db.create_user(user)
            self.db.create_seller_limit(user.id, name, daily, monthly)

            self.load_sellers_list()
            dialog.destroy()
            messagebox.showinfo("Sucesso", f"Vendedor {name} criado!")
            self.update_status(f"Vendedor {name} criado com limites diário {daily:.0f} e mensal {monthly:.0f}")

        tk.Button(dialog, text="Criar Vendedor", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def edit_seller_limits(self):
        selection = self.sellers_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um vendedor!")
            return

        item = self.sellers_tree.item(selection[0])
        seller_id = item['values'][0]
        limit = self.db.get_seller_limit(seller_id)

        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Limites do Vendedor")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"Limites: {limit.seller_name}", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(frame, text="Limite Diário (AOA):").grid(row=0, column=0, sticky='w', pady=5)
        daily_entry = tk.Entry(frame, width=25)
        daily_entry.insert(0, str(limit.daily_limit))
        daily_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Limite Mensal (AOA):").grid(row=1, column=0, sticky='w', pady=5)
        monthly_entry = tk.Entry(frame, width=25)
        monthly_entry.insert(0, str(limit.monthly_limit))
        monthly_entry.grid(row=1, column=1, pady=5)

        def save():
            try:
                daily = float(daily_entry.get())
                monthly = float(monthly_entry.get())
                self.db.update_seller_limit(seller_id, daily, monthly)
                self.load_sellers_list()
                dialog.destroy()
                messagebox.showinfo("Sucesso", "Limites atualizados!")
                self.update_status(f"Limites do vendedor {limit.seller_name} atualizados")
            except:
                messagebox.showerror("Erro", "Digite valores válidos!")

        tk.Button(dialog, text="Salvar", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    # ========== SESSÕES PDV ==========
    def create_pdv_sessions_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔄 Sessões PDV")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="🔓 Abrir Sessão", command=self.open_pdv_session_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="🔒 Fechar Sessão", command=self.close_pdv_session_dialog,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Vendedor', 'Abertura', 'Fechamento', 'Saldo Inicial', 'Total Vendas', 'Status')
        self.sessions_tree = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.sessions_tree.heading(col, text=col)
            self.sessions_tree.column(col, width=120)
        self.sessions_tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_pdv_sessions()

    def load_pdv_sessions(self):
        if not hasattr(self, 'sessions_tree') or not self.sessions_tree:
            return
        for item in self.sessions_tree.get_children():
            self.sessions_tree.delete(item)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        for s in self.db.get_pdv_sessions():
            status_icon = "🟢" if s.status == "Aberto" else "🔴"
            self.sessions_tree.insert('', 'end', values=(
                s.id, s.user_name,
                s.opening_date[:16] if s.opening_date else "-",
                s.closing_date[:16] if s.closing_date else "-",
                f"{currency} {s.opening_balance:.2f}",
                f"{currency} {s.total_sales:.2f}",
                f"{status_icon} {s.status}"
            ))

    def open_pdv_session_dialog(self):
        active = self.db.get_active_pdv_session(self.current_user.id)
        if active:
            messagebox.showwarning("Aviso", f"Você já tem uma sessão aberta desde {active.opening_date[:16]}")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Abrir Sessão PDV")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Abertura de Sessão PDV", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(frame, text="Saldo Inicial:").grid(row=0, column=0, sticky='w', pady=5)
        balance_entry = tk.Entry(frame, width=25)
        balance_entry.insert(0, "0")
        balance_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Observações:").grid(row=1, column=0, sticky='w', pady=5)
        notes_entry = tk.Entry(frame, width=35)
        notes_entry.grid(row=1, column=1, pady=5)

        def save():
            try:
                balance = float(balance_entry.get())
                session_id = self.db.open_pdv_session(
                    self.current_user.id,
                    self.current_user.name,
                    balance,
                    notes_entry.get()
                )
                if session_id:
                    self.load_pdv_sessions()
                    dialog.destroy()
                    messagebox.showinfo("Sucesso", "Sessão PDV aberta!")
                    self.update_status(f"Sessão PDV aberta com saldo inicial {balance:.2f}")
                else:
                    messagebox.showerror("Erro", "Já existe uma sessão aberta!")
            except:
                messagebox.showerror("Erro", "Valor inválido!")

        tk.Button(dialog, text="Abrir Sessão", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def close_pdv_session_dialog(self):
        active = self.db.get_active_pdv_session(self.current_user.id)
        if not active:
            messagebox.showwarning("Aviso", "Você não tem nenhuma sessão aberta!")
            return

        # Calcular vendas do dia
        sales_today = self.db.get_sales_today()
        total_sales = sum(s.total for s in sales_today)

        dialog = tk.Toplevel(self.root)
        dialog.title("Fechar Sessão PDV")
        dialog.geometry("450x400")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Fechamento de Sessão PDV", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        tk.Label(frame, text=f"Total de Vendas: {currency} {total_sales:.2f}", font=self.fonts['heading']).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Saldo em Caixa:").grid(row=1, column=0, sticky='w', pady=5)
        closing_entry = tk.Entry(frame, width=25)
        closing_entry.insert(0, str(active.opening_balance + total_sales))
        closing_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Observações:").grid(row=2, column=0, sticky='w', pady=5)
        notes_entry = tk.Entry(frame, width=35)
        notes_entry.grid(row=2, column=1, pady=5)

        def save():
            try:
                closing = float(closing_entry.get())
                expected = active.opening_balance + total_sales
                diff = closing - expected

                msg = f"Saldo Inicial: {currency} {active.opening_balance:.2f}\n"
                msg += f"Total Vendas: {currency} {total_sales:.2f}\n"
                msg += f"Esperado: {currency} {expected:.2f}\n"
                msg += f"Apurado: {currency} {closing:.2f}\n"
                msg += f"Diferença: {currency} {diff:.2f}\n\n"

                if abs(diff) > 0.01:
                    msg += f"⚠️ ATENÇÃO: Diferença de {currency} {diff:.2f}!"

                if messagebox.askyesno("Confirmar", msg + "\n\nDeseja fechar a sessão?"):
                    self.db.close_pdv_session(active.id, closing, total_sales, notes_entry.get())
                    self.load_pdv_sessions()
                    dialog.destroy()
                    messagebox.showinfo("Sucesso", "Sessão PDV fechada!")
                    self.update_status(f"Sessão PDV fechada. Total vendido: {currency} {total_sales:.2f}")
            except:
                messagebox.showerror("Erro", "Valor inválido!")

        tk.Button(dialog, text="Fechar Sessão", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    # ========== BACKUP ==========
    def create_backup_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💾 Backup")

        main_frame = tk.Frame(tab, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        btn_frame = tk.Frame(main_frame, bg=self.colors['light'])
        btn_frame.pack(fill='x', pady=10)

        tk.Button(btn_frame, text="💾 Criar Backup Agora", command=self.create_backup_now,
                 bg=self.colors['success'], fg='white', font=self.fonts['heading'], padx=20).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Restaurar Backup", command=self.restore_backup_now,
                 bg=self.colors['warning'], fg='white', font=self.fonts['heading'], padx=20).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Limpar Backups Antigos", command=self.clean_old_backups_now,
                 bg=self.colors['danger'], fg='white', font=self.fonts['heading'], padx=20).pack(side='left', padx=5)

        tk.Label(main_frame, text="Backups Disponíveis:", font=self.fonts['heading']).pack(anchor='w', pady=(20, 5))

        self.backup_listbox = tk.Listbox(main_frame, font=self.fonts['normal'], height=15)
        self.backup_listbox.pack(fill='both', expand=True, pady=5)

        info_frame = tk.Frame(main_frame, bg=self.colors['light'], relief='groove', bd=1)
        info_frame.pack(fill='x', pady=10)

        tk.Label(info_frame, text="ℹ️ Informações:", font=self.fonts['heading']).pack(anchor='w', padx=10, pady=5)
        tk.Label(info_frame, text="• Backups são salvos automaticamente na pasta 'backups'", font=self.fonts['small']).pack(anchor='w', padx=20)
        tk.Label(info_frame, text="• Recomenda-se fazer backup diariamente", font=self.fonts['small']).pack(anchor='w', padx=20)
        tk.Label(info_frame, text="• Backups antigos são mantidos por 30 dias", font=self.fonts['small']).pack(anchor='w', padx=20)

        self.load_backup_list()

    def load_backup_list(self):
        if not hasattr(self, 'backup_listbox') or not self.backup_listbox:
            return
        self.backup_listbox.delete(0, tk.END)

        if os.path.exists(BACKUP_DIR):
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')], reverse=True)
            for b in backups:
                path = os.path.join(BACKUP_DIR, b)
                size = os.path.getsize(path) / (1024 * 1024)
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
                self.backup_listbox.insert(tk.END, f"{b} - {size:.2f} MB - {mtime}")

    def create_backup_now(self):
        try:
            path = self.db.backup_database()
            self.load_backup_list()
            messagebox.showinfo("Sucesso", f"Backup criado com sucesso!\n{path}")
            self.update_status(f"Backup criado: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar backup: {str(e)}")

    def restore_backup_now(self):
        selection = self.backup_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um backup para restaurar!")
            return

        backup_name = self.backup_listbox.get(selection[0]).split(' - ')[0]
        backup_path = os.path.join(BACKUP_DIR, backup_name)

        if messagebox.askyesno("Confirmar",
            f"Restaurar o backup {backup_name}?\n\n"
            "ATENÇÃO: Isso substituirá TODOS os dados atuais!\n"
            "O sistema será reiniciado após a restauração."):

            try:
                self.db.restore_backup(backup_path)
                messagebox.showinfo("Sucesso", "Backup restaurado! O sistema será reiniciado.")
                self.root.quit()
                os.execl(sys.executable, sys.executable, *sys.argv)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao restaurar backup: {str(e)}")

    def clean_old_backups_now(self):
        if messagebox.askyesno("Confirmar", "Limpar backups antigos? (Manterá apenas os 10 mais recentes)"):
            self.db.clean_old_backups(keep=10)
            self.load_backup_list()
            messagebox.showinfo("Sucesso", "Backups antigos removidos!")
            self.update_status("Limpeza de backups antigos concluída")

    # ========== CONFIGURAÇÕES ==========
    def create_settings_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Configurações")

        settings_nb = ttk.Notebook(tab)
        settings_nb.pack(fill='both', expand=True, padx=10, pady=10)

        # Aba: Empresa
        company_frame = ttk.Frame(settings_nb)
        settings_nb.add(company_frame, text="🏢 Empresa")
        self.create_company_settings(company_frame)

        # Aba: Sistema
        system_frame = ttk.Frame(settings_nb)
        settings_nb.add(system_frame, text="⚙️ Sistema")
        self.create_system_settings(system_frame)

        # Aba: Aparência
        appearance_frame = ttk.Frame(settings_nb)
        settings_nb.add(appearance_frame, text="🎨 Aparência")
        self.create_appearance_settings(appearance_frame)

    def create_company_settings(self, parent):
        company = self.db.get_company()

        frame = tk.Frame(parent, bg=self.colors['light'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        fields = [
            ("Nome da Empresa:", "name"),
            ("NIF:", "nif"),
            ("Telefone:", "phone"),
            ("Email:", "email"),
            ("Endereço:", "address"),
            ("Moeda:", "currency"),
            ("Taxa de IVA (%):", "tax_rate"),
            ("Nível:", "level")
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)

            if key == "level":
                entry = ttk.Combobox(frame, values=['micro', 'macro', 'industry'], state='readonly', width=30)
                if company:
                    entry.set(company.level)
                else:
                    entry.set('micro')
            elif key == "tax_rate":
                entry = tk.Entry(frame, width=33)
                if company:
                    entry.insert(0, str(company.tax_rate * 100))
                else:
                    entry.insert(0, str(DEFAULT_TAX_RATE * 100))
            else:
                entry = tk.Entry(frame, width=33)
                if company:
                    value = getattr(company, key, '')
                    entry.insert(0, str(value))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry

        def save_company():
            try:
                if company:
                    company.name = entries['name'].get()
                    company.nif = entries['nif'].get()
                    company.phone = entries['phone'].get()
                    company.email = entries['email'].get()
                    company.address = entries['address'].get()
                    company.currency = entries['currency'].get() or DEFAULT_CURRENCY
                    company.tax_rate = float(entries['tax_rate'].get() or 0) / 100
                    company.level = entries['level'].get()
                    self.db.update_company(company)
                else:
                    new_company = Company(
                        name=entries['name'].get(),
                        nif=entries['nif'].get(),
                        phone=entries['phone'].get(),
                        email=entries['email'].get(),
                        address=entries['address'].get(),
                        currency=entries['currency'].get() or DEFAULT_CURRENCY,
                        tax_rate=float(entries['tax_rate'].get() or 0) / 100,
                        level=entries['level'].get()
                    )
                    self.db.create_company(new_company)
                
                messagebox.showinfo("Sucesso", "Configurações da empresa salvas!")
                self.update_status("Configurações da empresa atualizadas")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(frame, text="Salvar Configurações", command=save_company,
                 bg=self.colors['success'], fg='white', padx=20).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def create_system_settings(self, parent):
        frame = tk.Frame(parent, bg=self.colors['light'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(frame, text="Backup Automático", font=self.fonts['heading']).grid(row=0, column=0, columnspan=2, sticky='w', pady=10)
        
        self.auto_backup_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, text="Ativar backup automático diário", variable=self.auto_backup_var).grid(row=1, column=0, columnspan=2, sticky='w', padx=20)

        tk.Label(frame, text="Notificações", font=self.fonts['heading']).grid(row=2, column=0, columnspan=2, sticky='w', pady=10)
        
        self.notification_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, text="Exibir notificações do sistema", variable=self.notification_var).grid(row=3, column=0, columnspan=2, sticky='w', padx=20)

        self.sound_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, text="Ativar sons do sistema", variable=self.sound_var).grid(row=4, column=0, columnspan=2, sticky='w', padx=20)

        tk.Label(frame, text="Logs", font=self.fonts['heading']).grid(row=5, column=0, columnspan=2, sticky='w', pady=10)
        
        tk.Label(frame, text="Manter logs por (dias):").grid(row=6, column=0, sticky='w', padx=20)
        self.log_days_var = tk.StringVar(value="30")
        tk.Entry(frame, textvariable=self.log_days_var, width=10).grid(row=6, column=1, sticky='w')

        def save_system_settings():
            messagebox.showinfo("Sucesso", "Configurações do sistema salvas!")
            self.update_status("Configurações do sistema atualizadas")

        tk.Button(frame, text="Salvar Configurações", command=save_system_settings,
                 bg=self.colors['success'], fg='white', padx=20).grid(row=7, column=0, columnspan=2, pady=20)

    def create_appearance_settings(self, parent):
        frame = tk.Frame(parent, bg=self.colors['light'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(frame, text="Tema", font=self.fonts['heading']).grid(row=0, column=0, columnspan=2, sticky='w', pady=10)
        
        self.theme_var = tk.StringVar(value="claro")
        themes = [("🌞 Claro", "claro"), ("🌙 Escuro", "escuro"), ("🔵 Azul", "azul"), ("🟢 Verde", "verde")]
        
        for i, (text, value) in enumerate(themes):
            tk.Radiobutton(frame, text=text, variable=self.theme_var, value=value).grid(row=i+1, column=0, sticky='w', padx=20)

        tk.Label(frame, text="Tamanho da Fonte", font=self.fonts['heading']).grid(row=5, column=0, columnspan=2, sticky='w', pady=10)
        
        self.font_scale_var = tk.Scale(frame, from_=80, to=150, orient='horizontal', length=200)
        self.font_scale_var.set(100)
        self.font_scale_var.grid(row=6, column=0, columnspan=2, sticky='w', padx=20)

        def apply_appearance():
            scale = self.font_scale_var.get() / 100
            messagebox.showinfo("Info", "Reinicie o sistema para aplicar todas as alterações de aparência.")
            self.update_status("Configurações de aparência salvas")

        tk.Button(frame, text="Aplicar Alterações", command=apply_appearance,
                 bg=self.colors['success'], fg='white', padx=20).grid(row=7, column=0, columnspan=2, pady=20)

    # ========== USUÁRIOS ==========
    def create_users_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👥 Usuários")

        toolbar = tk.Frame(tab, bg=self.colors['light'])
        toolbar.pack(fill='x', padx=10, pady=5)

        tk.Button(toolbar, text="➕ Novo Usuário", command=self.new_user_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="✏️ Editar", command=self.edit_user_dialog,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)
        tk.Button(toolbar, text="🗑️ Excluir", command=self.delete_user,
                 bg=self.colors['danger'], fg='white').pack(side='left', padx=5)

        columns = ('ID', 'Nome', 'Email', 'Telefone', 'Perfil', 'Status')
        self.users_table = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        for col in columns:
            self.users_table.heading(col, text=col)
            self.users_table.column(col, width=150)
        self.users_table.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_users_list()

    def load_users_list(self):
        if not hasattr(self, 'users_table') or not self.users_table:
            return
        for item in self.users_table.get_children():
            self.users_table.delete(item)

        for u in self.db.get_users():
            status = "🟢 Ativo" if u.first_login == 0 else "🟡 Pendente"
            role_names = {'admin': 'Administrador', 'seller': 'Vendedor', 'stock': 'Almoxarife', 'manager': 'Gerente'}
            role_display = role_names.get(u.role, u.role)
            self.users_table.insert('', 'end', values=(
                u.id, u.name, u.email, u.phone, role_display, status
            ))

    def new_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Usuário")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Novo Usuário", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [
            ("Nome:", "name"),
            ("Email:", "email"),
            ("Senha:", "password"),
            ("Confirmar Senha:", "confirm"),
            ("Telefone:", "phone"),
            ("Perfil:", "role")
        ]

        entries = {}
        roles = [("Administrador", "admin"), ("Vendedor", "seller"), ("Almoxarife", "stock"), ("Gerente", "manager")]

        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            
            if key == "role":
                entry = ttk.Combobox(frame, values=[r[0] for r in roles], state='readonly', width=33)
                entry.set("Vendedor")
            elif key in ["password", "confirm"]:
                entry = tk.Entry(frame, show="*", width=35)
            else:
                entry = tk.Entry(frame, width=35)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry

        def save():
            name = entries['name'].get().strip()
            email = entries['email'].get().strip()
            password = entries['password'].get()
            confirm = entries['confirm'].get()
            phone = entries['phone'].get()
            role_name = entries['role'].get()
            
            role_map = {r[0]: r[1] for r in roles}
            role = role_map.get(role_name, "seller")

            if not name or not email:
                messagebox.showerror("Erro", "Nome e email são obrigatórios!")
                return
            if password != confirm:
                messagebox.showerror("Erro", "As senhas não coincidem!")
                return
            if len(password) < 4:
                messagebox.showerror("Erro", "A senha deve ter pelo menos 4 caracteres!")
                return

            user = User(
                name=name,
                email=email,
                password=password,
                phone=phone,
                role=role,
                first_login=True
            )
            self.db.create_user(user)
            self.load_users_list()
            dialog.destroy()
            messagebox.showinfo("Sucesso", f"Usuário {name} criado!")
            self.update_status(f"Usuário {name} criado com sucesso")

        tk.Button(dialog, text="Criar Usuário", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def edit_user_dialog(self):
        selection = self.users_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return

        item = self.users_table.item(selection[0])
        uid = item['values'][0]
        user = self.db.get_user_by_id(uid)

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar Usuário - {user.name}")
        dialog.geometry("500x550")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"Editar Usuário: {user.name}", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        fields = [
            ("Nome:", user.name),
            ("Email:", user.email),
            ("Telefone:", user.phone or ""),
            ("Perfil:", user.role)
        ]

        entries = {}
        roles = [("Administrador", "admin"), ("Vendedor", "seller"), ("Almoxarife", "stock"), ("Gerente", "manager")]
        role_names = {r[1]: r[0] for r in roles}

        for i, (label, value) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            
            if label == "Perfil:":
                entry = ttk.Combobox(frame, values=[r[0] for r in roles], state='readonly', width=33)
                entry.set(role_names.get(value, value))
            else:
                entry = tk.Entry(frame, width=35)
                entry.insert(0, str(value))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

        tk.Label(frame, text="Nova Senha (opcional):").grid(row=len(fields), column=0, sticky='w', padx=5, pady=5)
        new_pass_entry = tk.Entry(frame, show="*", width=35)
        new_pass_entry.grid(row=len(fields), column=1, padx=5, pady=5)

        tk.Label(frame, text="Confirmar Senha:").grid(row=len(fields)+1, column=0, sticky='w', padx=5, pady=5)
        confirm_pass_entry = tk.Entry(frame, show="*", width=35)
        confirm_pass_entry.grid(row=len(fields)+1, column=1, padx=5, pady=5)

        def update():
            user.name = entries['Nome:'].get()
            user.email = entries['Email:'].get()
            user.phone = entries['Telefone:'].get()
            
            role_name = entries['Perfil:'].get()
            role_map = {r[0]: r[1] for r in roles}
            user.role = role_map.get(role_name, "seller")

            new_pass = new_pass_entry.get()
            if new_pass:
                if new_pass != confirm_pass_entry.get():
                    messagebox.showerror("Erro", "As senhas não coincidem!")
                    return
                if len(new_pass) < 4:
                    messagebox.showerror("Erro", "A senha deve ter pelo menos 4 caracteres!")
                    return
                user.password = new_pass

            self.db.update_user(user)
            self.load_users_list()
            dialog.destroy()
            messagebox.showinfo("Sucesso", f"Usuário {user.name} atualizado!")
            self.update_status(f"Usuário {user.name} atualizado")

        tk.Button(dialog, text="Salvar Alterações", command=update, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def delete_user(self):
        selection = self.users_table.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return

        item = self.users_table.item(selection[0])
        uid = item['values'][0]
        user = self.db.get_user_by_id(uid)

        if user.id == self.current_user.id:
            messagebox.showerror("Erro", "Você não pode excluir seu próprio usuário!")
            return

        if messagebox.askyesno("Confirmar", f"Excluir o usuário {user.name}? Esta ação não pode ser desfeita!"):
            self.db.delete_user(uid)
            self.load_users_list()
            messagebox.showinfo("Sucesso", f"Usuário {user.name} excluído!")
            self.update_status(f"Usuário {user.name} removido do sistema")

    # ========== PERMISSÕES ==========
    def create_permissions_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔐 Permissões")

        tk.Label(tab, text="Gestão de Permissões por Perfil", font=self.fonts['title'],
                bg=self.colors['light'], fg=self.colors['dark']).pack(pady=10)

        select_frame = tk.Frame(tab, bg=self.colors['light'])
        select_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(select_frame, text="Perfil:").pack(side='left')
        self.permission_role_var = tk.StringVar()
        role_combo = ttk.Combobox(select_frame, textvariable=self.permission_role_var,
                                  values=['admin', 'manager', 'seller', 'stock'], state='readonly', width=20)
        role_combo.pack(side='left', padx=10)
        role_combo.bind('<<ComboboxSelected>>', self.load_permissions)

        tk.Button(select_frame, text="Salvar Permissões", command=self.save_permissions,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=10)

        columns = ('Módulo', 'Visualizar', 'Criar', 'Editar', 'Excluir')
        self.permissions_tree = ttk.Treeview(tab, columns=columns, show='headings', height=15)
        for col in columns:
            self.permissions_tree.heading(col, text=col)
            self.permissions_tree.column(col, width=150)
        self.permissions_tree.pack(fill='both', expand=True, padx=20, pady=10)

        self.permission_vars = {}

    def load_permissions(self, event=None):
        if not hasattr(self, 'permissions_tree') or not self.permissions_tree:
            return
        for item in self.permissions_tree.get_children():
            self.permissions_tree.delete(item)

        role = self.permission_role_var.get()
        if not role:
            return

        modules = ['products', 'clients', 'sales', 'purchases', 'stock', 'finance', 'reports', 'users']
        
        self.permission_vars.clear()
        
        for module in modules:
            row = self.db.cursor.execute(
                "SELECT * FROM permissions WHERE role=? AND module=?",
                (role, module)
            ).fetchone()
            
            can_view = "✅" if (row and row['can_view']) or role == 'admin' else "❌"
            can_create = "✅" if (row and row['can_create']) or role == 'admin' else "❌"
            can_edit = "✅" if (row and row['can_edit']) or role == 'admin' else "❌"
            can_delete = "✅" if (row and row['can_delete']) or role == 'admin' else "❌"
            
            self.permissions_tree.insert('', 'end', values=(module, can_view, can_create, can_edit, can_delete))

    def save_permissions(self):
        role = self.permission_role_var.get()
        if not role:
            messagebox.showwarning("Aviso", "Selecione um perfil!")
            return

        # Para edição detalhada, usar o SQLite Browser
        messagebox.showinfo("Info", "Para editar permissões detalhadamente, use um gerenciador SQLite ou entre em contato com o suporte.")
        self.update_status(f"Permissões para {role} visualizadas")

    # ========== MÉTODOS DO MENU (Implementações adicionais) ==========
    def show_sales_history(self):
        self.select_tab(8)  # Aba Financeiro

    def manage_categories(self):
        # ... (código completo do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Gerenciar Categorias")
        dialog.geometry("450x250")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Categorias de Produtos", font=self.fonts['heading']).pack(pady=10)

        add_frame = tk.Frame(dialog, bg=self.colors['light'], relief='groove', bd=1)
        add_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(add_frame, text="Nova Categoria:").pack(side='left', padx=10)
        new_cat_entry = tk.Entry(add_frame, width=30)
        new_cat_entry.pack(side='left', padx=10)

        def add_category():
            name = new_cat_entry.get().strip()
            if name:
                existing = self.db.get_category_by_name(name)
                if existing:
                    messagebox.showwarning("Aviso", "Categoria já existe!")
                    return
                self.db.create_category(name)
                load_categories()
                new_cat_entry.delete(0, tk.END)
                self.update_status(f"Categoria {name} criada")

        tk.Button(add_frame, text="➕ Adicionar", command=add_category,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=10)

        columns = ('ID', 'Nome', 'Descrição', 'Ações')
        cat_tree = ttk.Treeview(dialog, columns=columns, show='headings', height=12)
        for col in columns:
            cat_tree.heading(col, text=col)
            cat_tree.column(col, width=150)
        cat_tree.pack(fill='both', expand=True, padx=10, pady=10)

        def load_categories():
            for item in cat_tree.get_children():
                cat_tree.delete(item)
            for cat in self.db.get_categories():
                cat_tree.insert('', 'end', values=(cat.id, cat.name, cat.description, "✏️ 🗑️"))

        def edit_category():
            sel = cat_tree.selection()
            if sel:
                item = cat_tree.item(sel[0])
                cat_id, old_name, old_desc, _ = item['values']
                
                edit_dialog = tk.Toplevel(dialog)
                edit_dialog.title("Editar Categoria")
                edit_dialog.geometry("400x250")
                edit_dialog.transient(dialog)
                edit_dialog.grab_set()
                
                tk.Label(edit_dialog, text="Editar Categoria", font=self.fonts['heading']).pack(pady=10)
                
                frame = tk.Frame(edit_dialog)
                frame.pack(fill='both', expand=True, padx=20, pady=10)
                
                tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
                name_entry = tk.Entry(frame, width=30)
                name_entry.insert(0, old_name)
                name_entry.grid(row=0, column=1, padx=5, pady=5)
                
                tk.Label(frame, text="Descrição:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
                desc_entry = tk.Entry(frame, width=30)
                desc_entry.insert(0, old_desc)
                desc_entry.grid(row=1, column=1, padx=5, pady=5)
                
                def save():
                    cat = Category(id=cat_id, name=name_entry.get(), description=desc_entry.get())
                    self.db.update_category(cat)
                    load_categories()
                    edit_dialog.destroy()
                    self.update_status(f"Categoria {cat.name} atualizada")
                
                tk.Button(edit_dialog, text="Salvar", command=save, bg=self.colors['success'], fg='white').pack(pady=20)

        def delete_category():
            sel = cat_tree.selection()
            if sel:
                item = cat_tree.item(sel[0])
                cat_id, cat_name, _, _ = item['values']
                
                products = [p for p in self.db.get_products() if p.category_id == cat_id]
                if products:
                    messagebox.showerror("Erro", f"Não é possível excluir a categoria {cat_name} pois existem {len(products)} produtos associados!")
                    return
                
                if messagebox.askyesno("Confirmar", f"Excluir categoria {cat_name}?"):
                    self.db.delete_category(cat_id)
                    load_categories()
                    self.update_status(f"Categoria {cat_name} removida")

        cat_tree.bind('<Double-1>', lambda e: edit_category())

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(btn_frame, text="✏️ Editar", command=edit_category, bg=self.colors['warning'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Excluir", command=delete_category, bg=self.colors['danger'], fg='white').pack(side='left', padx=5)

        load_categories()

    def manage_units(self):
        # ... (código completo do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Unidades de Medida")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Unidades de Medida Padrão", font=self.fonts['heading']).pack(pady=10)

        units = ['UN', 'KG', 'G', 'L', 'ML', 'CX', 'PCT', 'PC', 'MT', 'M2', 'CM', 'M3']

        listbox = tk.Listbox(dialog, font=self.fonts['normal'], height=15)
        for u in units:
            listbox.insert(tk.END, u)
        listbox.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Label(dialog, text="Para adicionar novas unidades, digite diretamente no campo 'Unidade' do produto.",
                font=self.fonts['small'], fg='gray').pack(pady=10)

        tk.Button(dialog, text="Fechar", command=dialog.destroy, bg=self.colors['primary'], fg='white').pack(pady=10)

    def open_stock_entry(self):
        # ... (código completo do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Entrada de Estoque")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Entrada de Estoque", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(frame, text="Produto:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(frame, textvariable=product_var, state='readonly', width=35)
        products = self.db.get_products()
        product_combo['values'] = [f"{p.id} - {p.name} (Estoque: {p.stock:.0f})" for p in products]
        product_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Quantidade:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        qty_entry = tk.Entry(frame, width=35)
        qty_entry.insert(0, "1")
        qty_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Motivo:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        reason_entry = tk.Entry(frame, width=35)
        reason_entry.insert(0, "Ajuste manual")
        reason_entry.grid(row=2, column=1, padx=5, pady=5)

        def save():
            prod_text = product_var.get()
            if not prod_text:
                messagebox.showwarning("Aviso", "Selecione um produto!")
                return

            try:
                pid = int(prod_text.split(' - ')[0])
                qty = float(qty_entry.get())
                reason = reason_entry.get()

                if qty <= 0:
                    messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                    return

                self.db.update_product_stock(pid, qty, reason=reason)
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Entrada de {qty:.0f} unidades realizada!")
                self.update_status(f"Entrada de estoque: +{qty:.0f} unidades")
                self.load_products()
                self.load_pdv_products()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="Registrar Entrada", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def open_stock_exit(self):
        # ... (código completo do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Saída de Estoque")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Saída de Estoque", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(frame, text="Produto:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(frame, textvariable=product_var, state='readonly', width=35)
        products = self.db.get_products()
        product_combo['values'] = [f"{p.id} - {p.name} (Estoque: {p.stock:.0f})" for p in products]
        product_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Quantidade:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        qty_entry = tk.Entry(frame, width=35)
        qty_entry.insert(0, "1")
        qty_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Motivo:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        reason_entry = tk.Entry(frame, width=35)
        reason_entry.insert(0, "Ajuste manual")
        reason_entry.grid(row=2, column=1, padx=5, pady=5)

        def update_max_stock(*args):
            prod_text = product_var.get()
            if prod_text:
                try:
                    pid = int(prod_text.split(' - ')[0])
                    product = self.db.get_product_by_id(pid)
                    if product:
                        qty_entry.delete(0, tk.END)
                        qty_entry.insert(0, "1")
                except:
                    pass

        product_var.trace_add('write', update_max_stock)

        def save():
            prod_text = product_var.get()
            if not prod_text:
                messagebox.showwarning("Aviso", "Selecione um produto!")
                return

            try:
                pid = int(prod_text.split(' - ')[0])
                product = self.db.get_product_by_id(pid)
                qty = float(qty_entry.get())
                reason = reason_entry.get()

                if qty <= 0:
                    messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                    return
                if qty > product.stock:
                    messagebox.showerror("Erro", f"Estoque insuficiente! Disponível: {product.stock:.0f}")
                    return

                self.db.update_product_stock(pid, -qty, reason=reason)
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Saída de {qty:.0f} unidades realizada!")
                self.update_status(f"Saída de estoque: -{qty:.0f} unidades")
                self.load_products()
                self.load_pdv_products()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="Registrar Saída", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def open_stock_transfer(self):
        # ... (código completo do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Transferência entre Locais")
        dialog.geometry("550x450")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Transferência de Estoque", font=self.fonts['heading']).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(frame, text="Produto:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(frame, textvariable=product_var, state='readonly', width=35)
        products = self.db.get_products()
        product_combo['values'] = [f"{p.id} - {p.name} (Estoque: {p.stock:.0f})" for p in products]
        product_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Origem:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        from_var = tk.StringVar()
        from_combo = ttk.Combobox(frame, textvariable=from_var, values=["Armazém Central", "Loja Matriz", "Depósito Norte", "Depósito Sul"], width=33)
        from_combo.set("Armazém Central")
        from_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Destino:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        to_var = tk.StringVar()
        to_combo = ttk.Combobox(frame, textvariable=to_var, values=["Armazém Central", "Loja Matriz", "Depósito Norte", "Depósito Sul"], width=33)
        to_combo.set("Loja Matriz")
        to_combo.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Quantidade:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        qty_entry = tk.Entry(frame, width=35)
        qty_entry.insert(0, "1")
        qty_entry.grid(row=3, column=1, padx=5, pady=5)

        def save():
            prod_text = product_var.get()
            if not prod_text:
                messagebox.showwarning("Aviso", "Selecione um produto!")
                return

            origem = from_var.get()
            destino = to_var.get()

            if origem == destino:
                messagebox.showerror("Erro", "Origem e destino devem ser diferentes!")
                return

            try:
                pid = int(prod_text.split(' - ')[0])
                product = self.db.get_product_by_id(pid)
                qty = float(qty_entry.get())

                if qty <= 0:
                    messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                    return
                if qty > product.stock:
                    messagebox.showerror("Erro", f"Estoque insuficiente! Disponível: {product.stock:.0f}")
                    return

                self.db.update_product_stock(pid, -qty, reason=f"Transferência de {origem} para {destino}")
                
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Transferência de {qty:.0f} {product.unit} de {product.name}!\nDe: {origem}\nPara: {destino}")
                self.update_status(f"Transferência de estoque: {qty:.0f} unidades de {product.name}")
                self.load_products()
                self.load_pdv_products()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="Realizar Transferência", command=save, bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def open_inventory(self):
        # ... (código completo do método permanece igual - omitido para brevidade)
        dialog = tk.Toplevel(self.root)
        dialog.title("Inventário Físico")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Inventário Físico de Estoque", font=self.fonts['heading']).pack(pady=10)

        info_frame = tk.Frame(dialog, bg=self.colors['light'], relief='groove', bd=1)
        info_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(info_frame, text="📋 Instruções:", font=self.fonts['heading']).pack(anchor='w', padx=10, pady=5)
        tk.Label(info_frame, text="1. Conte fisicamente o estoque de cada produto", font=self.fonts['small']).pack(anchor='w', padx=20)
        tk.Label(info_frame, text="2. Informe a quantidade contada na coluna 'Contagem Física'", font=self.fonts['small']).pack(anchor='w', padx=20)
        tk.Label(info_frame, text="3. Clique em 'Ajustar Estoque' para atualizar o sistema", font=self.fonts['small']).pack(anchor='w', padx=20)

        columns = ('ID', 'Produto', 'Estoque Sistema', 'Contagem Física', 'Diferença')
        inventory_tree = ttk.Treeview(dialog, columns=columns, show='headings', height=15)
        for col in columns:
            inventory_tree.heading(col, text=col)
            inventory_tree.column(col, width=150)
        inventory_tree.column('Produto', width=250)
        inventory_tree.pack(fill='both', expand=True, padx=10, pady=10)

        physical_counts = {}

        for p in self.db.get_products():
            item_id = inventory_tree.insert('', 'end', values=(p.id, p.name, f"{p.stock:.0f}", "", 0))
            physical_counts[item_id] = {'product': p, 'entry': None}

        def on_edit(event):
            item = inventory_tree.selection()[0] if inventory_tree.selection() else None
            if item:
                col = inventory_tree.identify_column(event.x)
                if col == '#4':
                    x, y, width, height = inventory_tree.bbox(item, column='#4')
                    entry = tk.Entry(inventory_tree, width=10)
                    entry.place(x=x, y=y, width=width, height=height)
                    entry.focus()
                    
                    def save_edit():
                        try:
                            qty = float(entry.get())
                            values = list(inventory_tree.item(item, 'values'))
                            old_qty = float(values[2]) if values[2] else 0
                            diff = qty - old_qty
                            values[3] = f"{qty:.0f}"
                            values[4] = f"{diff:.0f}"
                            inventory_tree.item(item, values=values)
                            physical_counts[item]['entry'] = qty
                        except:
                            pass
                        entry.destroy()
                    
                    entry.bind('<Return>', lambda e: save_edit())
                    entry.bind('<FocusOut>', lambda e: save_edit())

        inventory_tree.bind('<Double-1>', on_edit)

        def apply_adjustments():
            adjustments = []
            for item_id, data in physical_counts.items():
                if data['entry'] is not None:
                    product = data['product']
                    physical = data['entry']
                    diff = physical - product.stock
                    if abs(diff) > 0.01:
                        adjustments.append((product, diff))
            
            if not adjustments:
                messagebox.showinfo("Inventário", "Nenhum ajuste necessário!")
                dialog.destroy()
                return

            msg = "Ajustes a serem realizados:\n\n"
            for product, diff in adjustments:
                msg += f"• {product.name}: {diff:+.0f} unidades\n"
            msg += "\nDeseja confirmar os ajustes?"

            if messagebox.askyesno("Confirmar", msg):
                for product, diff in adjustments:
                    self.db.update_product_stock(product.id, diff, reason="Ajuste de inventário físico")
                
                self.load_products()
                self.load_pdv_products()
                dialog.destroy()
                messagebox.showinfo("Sucesso", "Estoque ajustado conforme inventário!")
                self.update_status("Inventário físico concluído e estoque ajustado")

        tk.Button(dialog, text="Ajustar Estoque", command=apply_adjustments,
                 bg=self.colors['success'], fg='white', padx=30).pack(pady=20)

    def view_client_history(self):
        sel = self.clients_table.selection() if hasattr(self, 'clients_table') else None
        if sel:
            item = self.clients_table.item(sel[0])
            cid = item['values'][0]
            client = self.db.get_client_by_id(cid)
            
            sales = self.db.get_sales_by_client(cid)
            company = self.db.get_company()
            currency = company.currency if company else DEFAULT_CURRENCY
            
            report = f"HISTÓRICO DO CLIENTE\n{'='*50}\n"
            report += f"Cliente: {client.name}\n"
            report += f"NIF: {client.nif}\n"
            report += f"Total de Compras: {len(sales)}\n"
            report += f"Valor Total: {currency} {client.total_purchases:.2f}\n\n"
            report += "VENDAS REALIZADAS:\n" + "-"*40 + "\n"
            
            for s in sales:
                report += f"{s.invoice_number} | {s.created_at[:10]} | {currency} {s.total:.2f} | {s.payment_method}\n"
            
            self.show_report_window(f"Histórico - {client.name}", report)
        else:
            messagebox.showwarning("Aviso", "Selecione um cliente na aba Clientes!")

    def view_logs(self):
        if os.path.exists(LOGS_DIR):
            if platform.system() == 'Windows':
                os.startfile(LOGS_DIR)
            else:
                subprocess.call(['xdg-open', LOGS_DIR])
        else:
            messagebox.showwarning("Aviso", "Pasta de logs não encontrada!")

    def printer_settings(self):
        messagebox.showinfo("Configuração de Impressora", 
            "Para configurar a impressora térmica:\n\n"
            "1. Conecte a impressora via USB\n"
            "2. Instale os drivers necessários\n"
            "3. Configure no sistema operacional\n\n"
            "Para mais informações, consulte o suporte técnico.")

    def open_quotations(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Cotações")
        dialog.geometry("900x580")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Cotações", font=self.fonts['title']).pack(pady=10)

        columns = ('ID', 'Fornecedor', 'Data', 'Status', 'Total')
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=14)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor='center')
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        for idx, row in enumerate([
            ('COT-001', 'Fornecedor A', datetime.date.today().strftime('%d/%m/%Y'), 'Rascunho', f'{DEFAULT_CURRENCY} 0,00'),
            ('COT-002', 'Fornecedor B', datetime.date.today().strftime('%d/%m/%Y'), 'Pendente', f'{DEFAULT_CURRENCY} 0,00'),
        ]):
            tree.insert('', 'end', values=row)

        info_frame = tk.Frame(dialog, bg=self.colors['light'])
        info_frame.pack(fill='x', padx=10, pady=(0, 10))
        tk.Label(info_frame, text="Este módulo está em desenvolvimento."
                 "\nEm breve será possível solicitar cotações, comparar preços e converter em pedidos.",
                 font=self.fonts['normal'], bg=self.colors['light'], fg='#475569', justify='left').pack(anchor='w')

        tk.Button(dialog, text="Fechar", command=dialog.destroy,
                 bg=self.colors['success'], fg='white', padx=20, pady=8).pack(pady=5)

    def open_receipts(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Recebimentos")
        dialog.geometry("900x580")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Recebimentos", font=self.fonts['title']).pack(pady=10)

        columns = ('ID', 'Pedido', 'Fornecedor', 'Valor', 'Status')
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=14)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor='center')
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        purchases = self.db.get_purchases() if hasattr(self.db, 'get_purchases') else []
        if purchases:
            for purchase in purchases:
                tree.insert('', 'end', values=(purchase.number, purchase.number,
                                               purchase.supplier_name or '-',
                                               f"{DEFAULT_CURRENCY} {purchase.total_amount:,.2f}",
                                               purchase.status or 'Pendente'))
        else:
            tree.insert('', 'end', values=('Nenhum registro', '', '', '', ''))

        info_frame = tk.Frame(dialog, bg=self.colors['light'])
        info_frame.pack(fill='x', padx=10, pady=(0, 10))
        tk.Label(info_frame, text="Este módulo está em desenvolvimento."
                 "\nUse as funcionalidades existentes de compras e estoque enquanto recebimentos avançados são adicionados.",
                 font=self.fonts['normal'], bg=self.colors['light'], fg='#475569', justify='left').pack(anchor='w')

        tk.Button(dialog, text="Fechar", command=dialog.destroy,
                 bg=self.colors['success'], fg='white', padx=20, pady=8).pack(pady=5)

    def open_cash_management(self):
        summary = self.db.get_financial_summary()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        
        report = f"CAIXA - RESUMO\n{'='*40}\n\n"
        report += f"Saldo em Caixa: {currency} {summary['saldo_caixa']:.2f}\n"
        report += f"Entradas Pendentes: {currency} {summary.get('a_receber', 0):.2f}\n"
        report += f"Saídas Pendentes: {currency} {summary.get('a_pagar', 0):.2f}\n"
        
        self.show_report_window("Gestão de Caixa", report)

    def open_cashflow(self):
        self.cashflow_report()

    def view_production_tracking(self):
        orders = self.db.get_production_orders()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        
        if not orders:
            messagebox.showinfo("Acompanhamento", "Nenhuma ordem de produção encontrada.")
            return
        
        report = "ACOMPANHAMENTO DE PRODUÇÃO\n" + "="*60 + "\n\n"
        report += f"{'OP':<15} {'Produto':<25} {'Qtd':>8} {'Status':<15} {'Início':<12} {'Fim':<12}\n"
        report += "-"*80 + "\n"
        
        for po in orders:
            status_icon = "⏳" if po.status == "Planejada" else "🔧" if po.status == "Em Produção" else "✅"
            report += f"{po.number:<15} {po.product_name[:25]:<25} {po.quantity:>8.0f} {status_icon} {po.status:<12} {po.start_date[:10] if po.start_date else '-':<12} {po.end_date[:10] if po.end_date else '-':<12}\n"
        
        self.show_report_window("Acompanhamento de Produção", report)

    def add_production_note(self):
        messagebox.showinfo("Apontamentos", "Registrar horas trabalhadas e observações da produção.\n\nFuncionalidade em desenvolvimento.")

    def manage_routings(self):
        messagebox.showinfo("Roteiros", "Gestão de roteiros de produção.\n\nFuncionalidade em desenvolvimento.")

    def manage_workcenters(self):
        messagebox.showinfo("Centros de Trabalho", "Gestão de centros de trabalho.\n\nFuncionalidade em desenvolvimento.")

    def open_payables(self):
        transactions = self.db.get_transactions(trans_type="Saída", status="Pendente")
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        
        if not transactions:
            messagebox.showinfo("Contas a Pagar", "Nenhuma conta a pagar pendente.")
            return
        
        report = "CONTAS A PAGAR - PENDENTES\n" + "="*50 + "\n\n"
        total = 0
        for t in transactions:
            report += f"📅 {t.due_date[:10]} | {t.category} | {t.description} | {currency} {t.amount:.2f}\n"
            total += t.amount
        report += f"\nTotal Pendente: {currency} {total:.2f}"
        
        self.show_report_window("Contas a Pagar", report)

    def open_receivables(self):
        transactions = self.db.get_transactions(trans_type="Entrada", status="Pendente")
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        
        if not transactions:
            messagebox.showinfo("Contas a Receber", "Nenhuma conta a receber pendente.")
            return
        
        report = "CONTAS A RECEBER - PENDENTES\n" + "="*50 + "\n\n"
        total = 0
        for t in transactions:
            report += f"📅 {t.due_date[:10]} | {t.category} | {t.description} | {currency} {t.amount:.2f}\n"
            total += t.amount
        report += f"\nTotal a Receber: {currency} {total:.2f}"
        
        self.show_report_window("Contas a Receber", report)

    def sales_by_seller_report(self):
        sellers = self.db.get_sellers()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        
        report = "VENDAS POR VENDEDOR\n" + "="*50 + "\n\n"
        
        for seller in sellers:
            sales = [s for s in self.db.get_sales() if s.user_id == seller.id]
            total = sum(s.total for s in sales)
            report += f"{seller.name}:\n"
            report += f"  Vendas: {len(sales)}\n"
            report += f"  Total: {currency} {total:.2f}\n"
            report += f"  Ticket Médio: {currency} {total/len(sales) if sales else 0:.2f}\n\n"
        
        self.show_report_window("Vendas por Vendedor", report)

    def show_mrp_requirements(self):
        self.open_mrp_planning()

    def show_suggested_orders(self):
        low_stock = self.db.get_products_low_stock()
        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY
        
        if not low_stock:
            messagebox.showinfo("Ordens Sugeridas", "Nenhum produto com estoque baixo no momento!")
            return
        
        report = "📋 ORDENS SUGERIDAS - MRP\n" + "="*60 + "\n\n"
        report += "Produtos com estoque abaixo do mínimo:\n\n"
        
        for p in low_stock:
            needed = p.min_stock - p.stock
            report += f"🔴 {p.name}\n"
            report += f"   Estoque atual: {p.stock:.0f} | Mínimo: {p.min_stock:.0f} | Necessário: {needed:.0f}\n"
            report += f"   Sugestão: {'🛒 Comprar' if needed > 0 else '✅ OK'}\n\n"
        
        self.show_report_window("Ordens Sugeridas - MRP", report)

    def manage_lead_times(self):
        messagebox.showinfo("Lead Times", "Gestão de tempos de reposição.\n\nFuncionalidade em desenvolvimento.")

    def client_communication(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Comunicação com Clientes")
        dialog.geometry("950x620")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Comunicação com Clientes", font=self.fonts['title']).pack(pady=10)

        tab_control = ttk.Notebook(dialog)
        email_tab = tk.Frame(tab_control, bg=self.colors['light'])
        sms_tab = tk.Frame(tab_control, bg=self.colors['light'])
        tab_control.add(email_tab, text='📧 Email')
        tab_control.add(sms_tab, text='📱 SMS')
        tab_control.pack(fill='both', expand=True, padx=10, pady=10)

        clients = self.db.get_clients() if hasattr(self.db, 'get_clients') else []
        client_list = [f"{c.id} - {c.name} <{c.email}>" for c in clients if c.email]

        # Email Tab
        tk.Label(email_tab, text="Destinatário", bg=self.colors['light']).pack(anchor='w', padx=10, pady=(10, 0))
        recipient_email = ttk.Combobox(email_tab, values=client_list, width=90)
        recipient_email.pack(fill='x', padx=10, pady=5)

        tk.Label(email_tab, text="Assunto", bg=self.colors['light']).pack(anchor='w', padx=10, pady=(10, 0))
        subject_entry = tk.Entry(email_tab, width=100)
        subject_entry.pack(fill='x', padx=10, pady=5)
        subject_entry.insert(0, 'Oferta especial para clientes')

        tk.Label(email_tab, text="Mensagem", bg=self.colors['light']).pack(anchor='w', padx=10, pady=(10, 0))
        message_text = tk.Text(email_tab, height=12)
        message_text.pack(fill='both', expand=True, padx=10, pady=5)
        message_text.insert('1.0', 'Olá,\n\nConfira nossas novidades e promoções exclusivas.\n\nAtenciosamente,\nEquipe Kanawa Soft')

        email_buttons = tk.Frame(email_tab, bg=self.colors['light'])
        email_buttons.pack(fill='x', padx=10, pady=10)
        tk.Button(email_buttons, text="Enviar Email",
                 command=lambda: messagebox.showinfo('Email', 'Envio de email está em desenvolvimento.'),
                 bg=self.colors['success'], fg='white', padx=20).pack(side='left')
        tk.Button(email_buttons, text="Fechar", command=dialog.destroy,
                 bg=self.colors['danger'], fg='white', padx=20).pack(side='right')

        # SMS Tab
        tk.Label(sms_tab, text="Destinatário", bg=self.colors['light']).pack(anchor='w', padx=10, pady=(10, 0))
        recipient_sms = ttk.Combobox(sms_tab, values=client_list, width=90)
        recipient_sms.pack(fill='x', padx=10, pady=5)

        tk.Label(sms_tab, text="Mensagem SMS", bg=self.colors['light']).pack(anchor='w', padx=10, pady=(10, 0))
        sms_text = tk.Text(sms_tab, height=10)
        sms_text.pack(fill='both', expand=True, padx=10, pady=5)
        sms_text.insert('1.0', 'Olá! Confira nossas ofertas e visite a loja hoje mesmo.')

        sms_buttons = tk.Frame(sms_tab, bg=self.colors['light'])
        sms_buttons.pack(fill='x', padx=10, pady=10)
        tk.Button(sms_buttons, text="Enviar SMS",
                 command=lambda: messagebox.showinfo('SMS', 'Envio de SMS está em desenvolvimento.'),
                 bg=self.colors['success'], fg='white', padx=20).pack(side='left')
        tk.Button(sms_buttons, text="Fechar", command=dialog.destroy,
                 bg=self.colors['danger'], fg='white', padx=20).pack(side='right')

        note = tk.Label(dialog, text="Os recursos de e-mail e SMS estão em desenvolvimento.",
                        bg=self.colors['light'], fg='#475569')
        note.pack(fill='x', padx=10, pady=(0, 10))

    def open_mrp_planning(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Planejamento MRP")
        dialog.geometry("700x600")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Planejamento de Materiais (MRP)", font=self.fonts['title']).pack(pady=10)

        select_frame = tk.Frame(dialog, bg=self.colors['light'], relief='groove', bd=1)
        select_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(select_frame, text="Produto Final:").pack(side='left', padx=10)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(select_frame, textvariable=product_var, state='readonly', width=40)
        products = self.db.get_products()
        product_combo['values'] = [f"{p.id} - {p.name}" for p in products]
        product_combo.pack(side='left', padx=10)

        tk.Label(select_frame, text="Quantidade:").pack(side='left', padx=10)
        qty_entry = tk.Entry(select_frame, width=10)
        qty_entry.insert(0, "100")
        qty_entry.pack(side='left', padx=10)

        result_text = tk.Text(dialog, font=('Courier', 10), height=20)
        result_text.pack(fill='both', expand=True, padx=10, pady=10)

        def calculate_mrp():
            prod_text = product_var.get()
            if not prod_text:
                messagebox.showwarning("Aviso", "Selecione um produto!")
                return

            try:
                pid = int(prod_text.split(' - ')[0])
                qty = float(qty_entry.get())
                
                result = self.db.calculate_mrp(pid, qty)
                if not result:
                    result_text.delete('1.0', tk.END)
                    result_text.insert('1.0', "Erro ao calcular MRP. Verifique se o produto existe.")
                    return
                
                company = self.db.get_company()
                currency = company.currency if company else DEFAULT_CURRENCY
                
                output = f"PLANEJAMENTO MRP - {result['product'].name}\n"
                output += "="*60 + "\n\n"
                output += f"Demanda: {qty:.0f} {result['product'].unit}\n"
                output += f"Estoque atual: {result['stock']:.0f} {result['product'].unit}\n"
                output += f"Quantidade a produzir: {result['to_produce']:.0f} {result['product'].unit}\n\n"
                
                output += "COMPONENTES NECESSÁRIOS:\n"
                output += "-"*60 + "\n"
                output += f"{'Componente':<30} {'Por unidade':>12} {'Total':>12} {'Estoque':>10} {'Faltante':>10}\n"
                output += "-"*75 + "\n"
                
                total_cost = 0
                for comp in result['components']:
                    p = comp['product']
                    output += f"{p.name[:30]:<30} {comp['quantity_per_unit']:>12.2f} {comp['total_needed']:>12.2f} {comp['stock']:>10.2f} {comp['to_produce']:>10.2f}\n"
                    total_cost += comp['to_produce'] * p.cost
                
                output += "\n" + "="*60 + "\n"
                output += f"CUSTO ESTIMADO DE MATERIAIS: {currency} {total_cost:,.2f}\n"
                
                result_text.delete('1.0', tk.END)
                result_text.insert('1.0', output)
                
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="🔍 Calcular MRP", command=calculate_mrp,
                 bg=self.colors['primary'], fg='white', font=self.fonts['heading'], padx=20).pack(pady=10)

    def on_barcode_scan(self, event):
        barcode = self.barcode_entry.get().strip()
        if barcode:
            product = self.db.get_product_by_code(barcode)
            if product:
                if product.stock > 0:
                    self.cart.append({
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'quantity': 1,
                        'total': product.price
                    })
                    self.update_cart_display()
                    self.update_status(f"✓ {product.name} adicionado ao carrinho")
                    self.barcode_entry.delete(0, tk.END)
                    
                    if hasattr(self, 'sound_var') and self.sound_var.get():
                        try:
                            import winsound
                            winsound.Beep(800, 100)
                        except:
                            pass
                else:
                    messagebox.showwarning("Estoque", f"Produto {product.name} sem estoque!")
                    self.barcode_entry.delete(0, tk.END)
            else:
                if messagebox.askyesno("Produto não encontrado", 
                    f"Código {barcode} não cadastrado.\nDeseja cadastrar um novo produto?"):
                    self.open_product_dialog()
                    self.barcode_entry.delete(0, tk.END)

    def show_documentation(self):
        doc_text = f"""
📚 DOCUMENTAÇÃO {APP_NAME} v{VERSION}
{'='*50}

🏪 VISÃO GERAL
Sistema ERP completo para gestão de negócios, com módulos para:
- PDV (Ponto de Venda)
- Controle de Estoque
- Gestão de Clientes e Fornecedores
- Financeiro e Fluxo de Caixa
- Produção e MRP
- Relatórios Gerenciais

🛒 PDV - PONTO DE VENDA
• Leitura de código de barras
• Venda com múltiplos itens
• Orçamentos e conversão em venda
• Devoluções de produtos
• Histórico de vendas por cliente

📦 ESTOQUE
• Cadastro de produtos com categorias
• Entrada, saída e transferência
• Inventário físico
• Controle de estoque mínimo
• Alertas de estoque baixo

🏭 PRODUÇÃO E MRP
• Ordem de Produção (OP)
• Lista de Materiais (BOM)
• Planejamento de necessidades (MRP)
• Acompanhamento de produção

💰 FINANCEIRO
• Transações (receitas/despesas)
• Contas a pagar/receber
• Fluxo de caixa
• Relatórios financeiros

👥 ACESSO
• Perfis: Administrador, Vendedor, Almoxarife, Gerente
• Permissões por perfil
• Backup e restauração de dados

⌨️ ATALHOS DE TECLADO
F2 - Abrir PDV
Ctrl+Q - Sair do sistema
F5 - Atualizar tela atual
F1 - Ajuda

📞 SUPORTE
Desenvolvedor: {DEVELOPER}
Empresa: {COMPANY_NAME}
Email: dpedroservice@gmail.com
Tel: +244 946 299 834 / +244 959 777 301

© {datetime.datetime.now().year} - Todos os direitos reservados
"""
        messagebox.showinfo("Documentação", doc_text)

    def show_support(self):
        support_text = f"""
📞 SUPORTE TÉCNICO - {APP_NAME}

Desenvolvedor: {DEVELOPER}
Empresa: {COMPANY_NAME}
Email: dpedroservice@gmail.com
Telefone: +244 946 299 834 / +244 959 777 301

🕐 Horário de Atendimento:
Segunda a Sexta: 8h às 21h
Sábado: 8h às 17h

💡 DICAS:
1. Faça backup regularmente (menu Admin > Backup)
2. Mantenha o estoque mínimo configurado
3. Utilize códigos de barras para agilizar o PDV
4. Revise os relatórios periodicamente

📧 Para suporte técnico, envie um email com:
- Descrição detalhada do problema
- Versão do sistema
- Passos para reproduzir o erro
- Screenshot se possível
"""
        messagebox.showinfo("Suporte", support_text)

    def show_about(self):
        about_text = f"""
🏪 {APP_NAME} v{VERSION}

Sistema de Gestão Empresarial Completo
ERP para Micro, Macro e Indústria

Desenvolvido por: {DEVELOPER}
Empresa: {COMPANY_NAME}

{"="*40}

MÓDULOS INCLUÍDOS:
✅ PDV (Ponto de Venda)
✅ Controle de Estoque
✅ Gestão de Clientes
✅ Gestão de Fornecedores
✅ Orçamentos e Vendas
✅ Devoluções
✅ Financeiro e Fluxo de Caixa
✅ Produção e MRP
✅ Lista de Materiais (BOM)
✅ Relatórios Gerenciais
✅ Backup e Restauração
✅ Controle de Usuários

{"="*40}

Tecnologias utilizadas:
• Python 3.11+
• Tkinter (Interface)
• SQLite (Banco de Dados)

© {datetime.datetime.now().year} - Todos os direitos reservados

Licença: Uso exclusivo para clientes autorizados.
"""
        messagebox.showinfo("Sobre", about_text)

    # ========== CAIXA DIÁRIO ==========
    def create_cash_register_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💵 Caixa")

        hdr = tk.Frame(tab, bg=self.colors['primary'], height=50)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text="💵 CAIXA DIÁRIO", font=self.fonts['heading'],
                 bg=self.colors['primary'], fg='white').pack(side='left', padx=20, pady=12)

        body = tk.Frame(tab, bg=self.colors['light'])
        body.pack(fill='both', expand=True, padx=20, pady=15)

        # KPIs do dia
        today = datetime.date.today().isoformat()
        sales_today = self.db.get_sales_today() if hasattr(self.db, 'get_sales_today') else []
        total_today = sum(s.total for s in sales_today)
        count_today = len(sales_today)

        kpi_frame = tk.Frame(body, bg=self.colors['light'])
        kpi_frame.pack(fill='x', pady=(0, 15))

        company = self.db.get_company()
        currency = company.currency if company else DEFAULT_CURRENCY

        kpis = [
            ("🛒 Vendas Hoje",   str(count_today),                  self.colors['info']),
            ("💰 Total Hoje",    f"{currency} {total_today:,.2f}",   self.colors['success']),
            ("📅 Data",          datetime.date.today().strftime('%d/%m/%Y'), self.colors['primary']),
            ("🕐 Hora",          datetime.datetime.now().strftime('%H:%M'),  self.colors['warning']),
        ]
        for i, (title, value, color) in enumerate(kpis):
            card = tk.Frame(kpi_frame, bg='white', relief='flat', bd=0,
                            highlightbackground='#e2e8f0', highlightthickness=1)
            card.grid(row=0, column=i, padx=8, pady=5, sticky='nsew')
            kpi_frame.grid_columnconfigure(i, weight=1)
            tk.Label(card, text=title, font=self.fonts['small'],
                     bg='white', fg='#64748b').pack(pady=(10, 2))
            tk.Label(card, text=value, font=('Segoe UI', 16, 'bold'),
                     bg='white', fg=color).pack(pady=(0, 10))

        # Tabela de vendas do dia
        tk.Label(body, text="Vendas do Dia", font=self.fonts['heading'],
                 bg=self.colors['light']).pack(anchor='w', pady=(0, 5))

        cols = ('NF', 'Cliente', 'Pagamento', 'Total', 'Hora')
        tree = ttk.Treeview(body, columns=cols, show='headings', height=14)
        for col in cols:
            tree.heading(col, text=col)
        tree.column('NF', width=160); tree.column('Cliente', width=0, stretch=True)
        tree.column('Pagamento', width=110); tree.column('Total', width=110); tree.column('Hora', width=75)

        vsb = ttk.Scrollbar(body, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)

        for s in sales_today:
            client = self.db.get_client_by_id(s.client_id) if s.client_id else None
            cname = client.name if client else "Consumidor Final"
            hora = ""
            if s.created_at:
                try:
                    hora = datetime.datetime.fromisoformat(s.created_at).strftime('%H:%M')
                except Exception:
                    hora = ""
            tree.insert('', 'end', values=(s.invoice_number, cname, s.payment_method,
                                            f"{currency} {s.total:.2f}", hora))

        btn_frame = tk.Frame(body, bg=self.colors['light'])
        btn_frame.pack(fill='x', pady=10)
        tk.Button(btn_frame, text="🔄 Actualizar", command=self.create_cash_register_tab,
                  bg=self.colors['info'], fg='white', font=self.fonts['normal'],
                  bd=0, padx=16, cursor='hand2').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🖨️ Imprimir Resumo",
                  command=lambda: messagebox.showinfo("Caixa", f"Vendas hoje: {count_today}\nTotal: {currency} {total_today:,.2f}"),
                  bg=self.colors['primary'], fg='white', font=self.fonts['normal'],
                  bd=0, padx=16, cursor='hand2').pack(side='left', padx=5)

    # ========== PROMOÇÕES ==========
    def create_promotions_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏷️ Promoções")

        hdr = tk.Frame(tab, bg='#7c3aed', height=50)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🏷️ GESTÃO DE PROMOÇÕES", font=self.fonts['heading'],
                 bg='#7c3aed', fg='white').pack(side='left', padx=20, pady=12)
        tk.Button(hdr, text="＋ Nova Promoção",
                  command=self._open_new_promotion_dialog,
                  bg='#6d28d9', fg='white', font=self.fonts['normal'],
                  bd=0, padx=14, cursor='hand2').pack(side='right', padx=15, pady=10)

        body = tk.Frame(tab, bg=self.colors['light'])
        body.pack(fill='both', expand=True, padx=15, pady=15)

        info = tk.Label(body,
            text="ℹ️  Configure promoções por produto ou categoria: desconto percentual ou preço fixo.",
            font=self.fonts['normal'], bg='#ede9fe', fg='#4c1d95',
            relief='flat', bd=0, padx=12, pady=8)
        info.pack(fill='x', pady=(0, 10))

        cols = ('Produto/Categoria', 'Tipo', 'Valor', 'Validade', 'Estado')
        self._promo_tree = ttk.Treeview(body, columns=cols, show='headings', height=16)
        for col in cols:
            self._promo_tree.heading(col, text=col)
        self._promo_tree.column('Produto/Categoria', stretch=True, minwidth=200)
        self._promo_tree.column('Tipo', width=120)
        self._promo_tree.column('Valor', width=90)
        self._promo_tree.column('Validade', width=100)
        self._promo_tree.column('Estado', width=80)

        vsb = ttk.Scrollbar(body, orient='vertical', command=self._promo_tree.yview)
        self._promo_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self._promo_tree.pack(fill='both', expand=True)

        # Pré-carregar da BD se existir tabela
        try:
            rows = self.db.cursor.execute(
                "SELECT * FROM promotions ORDER BY id DESC").fetchall()
            for row in rows:
                self._promo_tree.insert('', 'end', values=(
                    row['target'], row['promo_type'], row['promo_value'],
                    row['valid_until'], row['status']
                ))
        except Exception:
            pass

    def _open_new_promotion_dialog(self):
        # Garantir tabela de promoções
        try:
            self.db.cursor.execute('''CREATE TABLE IF NOT EXISTS promotions (
                id INTEGER PRIMARY KEY, target TEXT, promo_type TEXT,
                promo_value REAL, valid_until TEXT, status TEXT DEFAULT "Ativa",
                created_at TIMESTAMP)''')
            self.db.conn.commit()
        except Exception:
            pass

        dialog = tk.Toplevel(self.root)
        dialog.title("Nova Promoção")
        dialog.geometry("440x360")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="🏷️ Nova Promoção", font=self.fonts['heading']).pack(pady=15)

        frame = tk.Frame(dialog)
        frame.pack(fill='both', padx=20, pady=5)

        fields = [("Produto/Categoria:", "entry"), ("Tipo:", "combo"),
                  ("Valor (% ou AOA):", "entry"), ("Validade (dd/mm/aaaa):", "entry")]
        widgets = {}
        for label, kind in fields:
            row = tk.Frame(frame)
            row.pack(fill='x', pady=4)
            tk.Label(row, text=label, width=22, anchor='w').pack(side='left')
            if kind == 'entry':
                w = tk.Entry(row, font=self.fonts['normal'])
                w.pack(side='left', fill='x', expand=True)
            else:
                w = ttk.Combobox(row, values=["% Desconto", "Preço Fixo"], state='readonly', width=18)
                w.current(0)
                w.pack(side='left')
            widgets[label] = w

        def save():
            try:
                self.db.cursor.execute('''INSERT INTO promotions
                    (target, promo_type, promo_value, valid_until, status, created_at)
                    VALUES (?,?,?,?,?,?)''', (
                    widgets["Produto/Categoria:"].get(),
                    widgets["Tipo:"].get(),
                    float(widgets["Valor (% ou AOA):"].get() or 0),
                    widgets["Validade (dd/mm/aaaa):"].get(),
                    "Ativa",
                    datetime.datetime.now().isoformat()
                ))
                self.db.conn.commit()
                messagebox.showinfo("Sucesso", "Promoção criada com sucesso!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="💾 Guardar", command=save,
                  bg=self.colors['success'], fg='white', font=self.fonts['heading'],
                  bd=0, padx=20, cursor='hand2').pack(pady=15)

    # ========== ORDENS DE SERVIÇO ==========
    def create_service_orders_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 O. Serviço")

        hdr = tk.Frame(tab, bg='#0f766e', height=50)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🔧 ORDENS DE SERVIÇO", font=self.fonts['heading'],
                 bg='#0f766e', fg='white').pack(side='left', padx=20, pady=12)
        tk.Button(hdr, text="＋ Nova O.S.",
                  command=self._open_new_os_dialog,
                  bg='#0d9488', fg='white', font=self.fonts['normal'],
                  bd=0, padx=14, cursor='hand2').pack(side='right', padx=15, pady=10)

        body = tk.Frame(tab, bg=self.colors['light'])
        body.pack(fill='both', expand=True, padx=15, pady=15)

        # Garantir tabela
        try:
            self.db.cursor.execute('''CREATE TABLE IF NOT EXISTS service_orders (
                id INTEGER PRIMARY KEY, number TEXT UNIQUE, client_id INTEGER,
                client_name TEXT, equipment TEXT, problem TEXT, solution TEXT,
                status TEXT DEFAULT "Aberta", technician TEXT,
                entry_date TEXT, exit_date TEXT, total_amount REAL DEFAULT 0,
                user_id INTEGER, user_name TEXT, created_at TIMESTAMP)''')
            self.db.conn.commit()
        except Exception:
            pass

        # Filtros
        filter_frame = tk.Frame(body, bg=self.colors['light'])
        filter_frame.pack(fill='x', pady=(0, 8))
        tk.Label(filter_frame, text="Status:", bg=self.colors['light']).pack(side='left')
        self._os_status_var = tk.StringVar(value="Todas")
        ttk.Combobox(filter_frame, textvariable=self._os_status_var,
                     values=["Todas", "Aberta", "Em Andamento", "Aguardando Peça",
                              "Concluída", "Entregue", "Cancelada"],
                     state='readonly', width=18).pack(side='left', padx=5)
        tk.Button(filter_frame, text="🔄 Filtrar",
                  command=self._load_os_list,
                  bg=self.colors['info'], fg='white', bd=0, padx=10, cursor='hand2').pack(side='left')

        cols = ('Nº O.S.', 'Cliente', 'Equipamento', 'Problema', 'Status', 'Técnico', 'Data')
        self._os_tree = ttk.Treeview(body, columns=cols, show='headings', height=16)
        col_w = {'Nº O.S.': 120, 'Cliente': 0, 'Equipamento': 130, 'Problema': 0,
                 'Status': 110, 'Técnico': 110, 'Data': 90}
        for col in cols:
            self._os_tree.heading(col, text=col)
            w = col_w.get(col, 100)
            if w == 0:
                self._os_tree.column(col, stretch=True, minwidth=120)
            else:
                self._os_tree.column(col, width=w, stretch=False)

        self._os_tree.tag_configure('open',     background='#dcfce7')
        self._os_tree.tag_configure('pending',  background='#fef9c3')
        self._os_tree.tag_configure('done',     background='#dbeafe')
        self._os_tree.tag_configure('canceled', background='#fee2e2')

        vsb = ttk.Scrollbar(body, orient='vertical', command=self._os_tree.yview)
        self._os_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self._os_tree.pack(fill='both', expand=True)
        self._os_tree.bind('<Double-1>', lambda e: self._open_os_detail())

        self._load_os_list()

    def _load_os_list(self):
        if not hasattr(self, '_os_tree'):
            return
        for item in self._os_tree.get_children():
            self._os_tree.delete(item)
        try:
            status_filter = self._os_status_var.get() if hasattr(self, '_os_status_var') else "Todas"
            if status_filter == "Todas":
                rows = self.db.cursor.execute(
                    "SELECT * FROM service_orders ORDER BY created_at DESC").fetchall()
            else:
                rows = self.db.cursor.execute(
                    "SELECT * FROM service_orders WHERE status=? ORDER BY created_at DESC",
                    (status_filter,)).fetchall()
            tag_map = {'Aberta': 'open', 'Em Andamento': 'pending',
                       'Concluída': 'done', 'Cancelada': 'canceled'}
            for row in rows:
                tag = tag_map.get(row['status'], '')
                self._os_tree.insert('', 'end', tags=(tag,), values=(
                    row['number'], row['client_name'], row['equipment'],
                    row['problem'][:40] if row['problem'] else '',
                    row['status'], row['technician'] or '',
                    row['entry_date'] or ''
                ))
        except Exception:
            pass

    def _open_new_os_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nova Ordem de Serviço")
        dialog.geometry("520x480")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="🔧 Nova Ordem de Serviço",
                 font=self.fonts['heading']).pack(pady=15)

        canvas = tk.Canvas(dialog, highlightthickness=0)
        sb = ttk.Scrollbar(dialog, orient='vertical', command=canvas.yview)
        sf = tk.Frame(canvas)
        sf.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=sf, anchor='nw')
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        canvas.pack(fill='both', expand=True, padx=20)

        clients = self.db.get_clients()
        client_names = [f"{c.id} - {c.name}" for c in clients]

        fields_cfg = [
            ("Cliente:", "combo", client_names),
            ("Equipamento:", "entry", None),
            ("Nº Série/IMEI:", "entry", None),
            ("Problema Reportado:", "text", None),
            ("Técnico Responsável:", "entry", None),
            ("Data de Entrada:", "entry", datetime.date.today().strftime('%d/%m/%Y')),
            ("Valor Estimado (AOA):", "entry", "0"),
            ("Status:", "combo", ["Aberta", "Em Andamento", "Aguardando Peça",
                                   "Concluída", "Entregue"]),
        ]
        widgets = {}
        for label, kind, options in fields_cfg:
            row = tk.Frame(sf)
            row.pack(fill='x', pady=4)
            tk.Label(row, text=label, width=22, anchor='w').pack(side='left')
            if kind == 'entry':
                w = tk.Entry(row, font=self.fonts['normal'])
                if options:
                    w.insert(0, options)
                w.pack(side='left', fill='x', expand=True)
            elif kind == 'combo':
                w = ttk.Combobox(row, values=options, state='readonly', width=28)
                w.pack(side='left')
            elif kind == 'text':
                w = tk.Text(row, font=self.fonts['normal'], height=3, width=30)
                w.pack(side='left', fill='x', expand=True)
            widgets[label] = w

        def save_os():
            try:
                client_val = widgets["Cliente:"].get()
                client_id = int(client_val.split(' - ')[0]) if client_val and ' - ' in client_val else 0
                client_name = client_val.split(' - ')[1] if client_val and ' - ' in client_val else "Anónimo"
                problem = widgets["Problema Reportado:"].get('1.0', tk.END).strip()
                number = generate_os_number()
                self.db.cursor.execute('''INSERT INTO service_orders
                    (number, client_id, client_name, equipment, problem,
                     status, technician, entry_date, total_amount, user_id, user_name, created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (
                    number, client_id, client_name,
                    widgets["Equipamento:"].get(),
                    problem,
                    widgets["Status:"].get() or "Aberta",
                    widgets["Técnico Responsável:"].get(),
                    widgets["Data de Entrada:"].get(),
                    float(widgets["Valor Estimado (AOA):"].get() or 0),
                    self.current_user.id, self.current_user.name,
                    datetime.datetime.now().isoformat()
                ))
                self.db.conn.commit()
                messagebox.showinfo("Sucesso", f"O.S. {number} criada!")
                self._load_os_list()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(dialog, text="💾 Guardar O.S.", command=save_os,
                  bg=self.colors['success'], fg='white', font=self.fonts['heading'],
                  bd=0, padx=20, cursor='hand2').pack(pady=12)

    def _open_os_detail(self):
        if not hasattr(self, '_os_tree'):
            return
        sel = self._os_tree.selection()
        if not sel:
            return
        vals = self._os_tree.item(sel[0])['values']
        if vals:
            messagebox.showinfo("O.S. Detalhes",
                f"Nº: {vals[0]}\nCliente: {vals[1]}\nEquipamento: {vals[2]}\n"
                f"Problema: {vals[3]}\nStatus: {vals[4]}\nTécnico: {vals[5]}")

    def logout(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.db.create_activity("logout", f"Usuário {self.current_user.name} saiu do sistema", "")
            self.root.quit()


# ==================== PONTO DE ENTRADA ====================
if __name__ == "__main__":
    root = tk.Tk()
    db = Database()
    app = KanawaApp(root, db)
    
    # Aplicar patches de melhoria
    apply_patches(app)
    
    def on_closing():
        try:
            if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
                root.destroy()
        except KeyboardInterrupt:
            root.destroy()
        except Exception as e:
            print(f"Erro ao fechar aplicação: {e}")
            try:
                root.destroy()
            except Exception:
                pass
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
