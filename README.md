# Chemical Equipment Parameter Visualizer -- Hybrid Web + Desktop App

## Overview

This project is a hybrid application designed to visualize and analyze chemical equipment data. It runs both as a 
**Web App (React +Chart.js)** and a **Desktop App (PyQt5 + Matplotlib)**, connected to a
**Django REST API backend**.

### Key Capabilities

-   CSV upload and parsing\
-   Summary statistics (total equipment, average flowrate, pressure,
    temperature)\
-   Bar & pie charts for equipment type distribution\
-   History management (stores last 5 uploaded datasets)\
-   PDF report generation and download\
-   Basic authentication for secure API access

------------------------------------------------------------------------

## Tech Stack

  Layer              Technology           Purpose
  ------------------ -------------------- ---------------------------
  Backend            Django + DRF         API & data processing
  Database           SQLite               Store history & summaries
  Web Frontend       React + Chart.js     Data visualization
  Desktop Frontend   PyQt5 + Matplotlib   Desktop visualization
  Data Handling      Pandas               CSV parsing & analytics
  PDF Generation     ReportLab            Export summary reports
  HTTP Requests      Axios / Requests     API communication
  Version Control    Git & GitHub         Source code management

------------------------------------------------------------------------

## Project Structure

    project-root/
    ├─ backend/
    |  ├─ backend/
    │  ├─ equipments/
    │  ├─ manage.py
    │  ├─ db.sqlite3
    │  └─ requirements.txt
    ├─ frontend/
    │  ├─ src/
    │  ├─ public/
    │  ├─ .env
    │  └─ package.json
    ├─ desktop_app/
    |  ├─ backend/
    │  ├─ ui/
    │  ├─ utils/
    │  └─ main.py
    └─ README.md

------------------------------------------------------------------------

## Setup Instructions

### 1. Backend Setup

``` bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### API Endpoints

  Method   Endpoint                                  Description
  -------- ----------------------------------------- -----------------
  POST     /api/upload/                              Upload CSV
  GET      /api/history/                             Last 5 datasets
  GET      /api/download/?id=`<dataset_id>`{=html}   Download PDF

*All API routes require Basic Authentication.*

------------------------------------------------------------------------

## 2. Web Frontend Setup

``` bash
cd frontend
npm install
```

Create `.env`:

    VITE_API_BASE=http://127.0.0.1:8000/api
    VITE_USERNAME=<your superuser username>
    VITE_PASSWORD=<your superuser password>

Run:

``` bash
npm run dev
```

------------------------------------------------------------------------

## 3. Desktop App Setup

``` bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac
pip install -r requirements.txt
cd desktop_app
python main.py
```

Update credentials in `desktop_app/backend/config.py`:

``` python
auth=("your_username", "your_password")
```

------------------------------------------------------------------------

## CSV Format

    Equipment Name,Type,Flowrate,Pressure,Temperature
    Pump-1,Pump,120,5.2,110
    Compressor-1,Compressor,95,8.4,95
    Valve-1,Valve,60,4.1,105
    HeatExchanger-1,HeatExchanger,150,6.2,130

------------------------------------------------------------------------

## Features Summary

-   CSV Upload\
-   Data Summary API\
-   Bar & Pie Charts\
-   Last 5 Datasets History\
-   PDF Report\
-   Basic Authentication

------------------------------------------------------------------------

## Optional Enhancements

-   User login system\
-   Dataset filtering/sorting\
-   Export history as CSV\
-   PyInstaller executable\

------------------------------------------------------------------------
