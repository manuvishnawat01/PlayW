# Beginner Playwright Python Web Automation Testing Project

Welcome to the **Web Automation Testing Project** built with **Playwright for Python**, **Pytest**, **CSV Data-Driven Testing**, and the **Page Object Model (POM)** pattern.

---

## 📌 Project Overview

This project automates an e-commerce website flow on **Automation Exercise** (`https://automationexercise.com`).

It demonstrates **two main testing suites**:

1. **Test Suite 1 — Data-Driven Login Test (`test_data_driven_login.py`)**: Data-driven testing reading 4 user credentials from `test_data/login_data.csv` via Pytest parameterization. Includes **3 positive login cases** and **1 negative login case**. Performs login validation with **no screenshots**.
2. **Test Suite 2 — Complete End-to-End Test (`test_complete_flow.py`)**: Automates the full user journey with **dynamic category & product detection**, **random selection at runtime**, product cart verification, and 7 flat screenshots saved directly to `screenshots/`.

---

## 🎲 Dynamic Detection & Random Selection Architecture

In the Complete End-to-End Test (`test_complete_flow.py`):

1. **Dynamic Category Detection**:
   * The test reads available product categories directly from the website DOM at runtime using locator `a[href^='/category_products/']`.
   * Python's `random.randint(0, count - 1)` selects a random category index.
   * `selected_category` name is stored in a variable and logged.

2. **Dynamic Product Detection**:
   * After navigating to the category page, available products are dynamically detected using `.features_items .single-products .productinfo p`.
   * Python's `random.randint(0, count - 1)` selects a random product index.
   * `selected_product` name is stored in a variable and logged.

3. **Cart Verification**:
   * The test adds the randomly selected product to the cart and opens the cart page.
   * `CartPage.verify_product_in_cart(selected_product)` asserts that the **exact same product** selected during runtime is present in the cart.

---

## 🛠️ Technology Stack

* **Python 3.x**: Programming language.
* **Playwright for Python**: Modern web automation library.
* **Pytest**: Test framework and runner.
* **Page Object Model (POM)**: Design pattern separating locators/actions from test code.
* **CSV Data-Driven Testing**: Standard `csv` library integration.

---

## 📁 Project Directory Structure

```text
PlayWrite_Project/
│
├── pages/                   # Page Object Model classes
│   ├── __init__.py
│   ├── login_page.py        # Login page elements (positive & negative testing)
│   ├── home_page.py         # Dynamic category detection & selection
│   ├── category_page.py     # Dynamic product detection & selection
│   ├── product_page.py      # Product details view & add to cart
│   └── cart_page.py         # Cart table verification & logout
│
├── tests/                   # Pytest test execution modules
│   ├── __init__.py
│   ├── test_data_driven_login.py # Test 1: Data-Driven Login (No screenshots)
│   └── test_complete_flow.py      # Test 2: Complete E2E Flow (Dynamic selection + 7 Screenshots)
│
├── test_data/               # External test data
│   └── login_data.csv       # CSV file storing 4 user records (3 success, 1 failure)
│
├── utils/                   # Helper utilities
│   ├── __init__.py
│   └── csv_reader.py        # CSV parsing utility for Pytest parameterization
│
├── screenshots/             # Flat output directory (NO inner subfolders)
│   ├── 01_website_launched.png
│   ├── 02_login_success.png
│   ├── 03_category_selected.png
│   ├── 04_product_selected.png
│   ├── 05_product_added_to_cart.png
│   ├── 06_cart_verified.png
│   ├── 07_logout.png
│   └── failure_test_complete_flow.png (only if test unexpectedly fails)
│
├── conftest.py              # Pytest fixture & flat failure screenshot hook
├── config.py                # Central constants
├── pytest.ini               # Pytest configuration settings
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 📸 Screenshots Policy

* **Screenshots are generated ONLY by the Complete End-to-End Test (`test_complete_flow.py`)**.
* The `screenshots/` directory is **completely flat with NO subfolders**.
* Milestone PNG files:
  1. `01_website_launched.png`
  2. `02_login_success.png`
  3. `03_category_selected.png`
  4. `04_product_selected.png`
  5. `05_product_added_to_cart.png`
  6. `06_cart_verified.png`
  7. `07_logout.png`

---

## 🚀 Setup & Execution Commands

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Run Data-Driven Login Test (Test 1 - No Screenshots)
```bash
pytest tests/test_data_driven_login.py -v
```

### Step 3: Run Complete End-to-End Test (Test 2 - Dynamic Selection + Screenshots)
```bash
pytest tests/test_complete_flow.py -v
```

### Step 4: Run ALL Tests Together
```bash
pytest -v
```
