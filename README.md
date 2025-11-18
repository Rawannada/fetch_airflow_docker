# Fetch & Process Amazon Books with Airflow & Docker

![Amazon Books Pipeline Diagram](https://raw.githubusercontent.com/Rawannada/fetch_airflow_docker/main/images/architecture.png)


This project automates the fetching, cleaning, transforming, and storing of Amazon Books data using **Apache Airflow** running inside **Docker Compose**.

---

##  Features
- **Automated Airflow DAG** for fetching, cleaning, transforming, and inserting book data
- **Data Cleaning**
  - Remove duplicates
  - Convert ratings to float
  - Add `recommended_flag` column (Yes/No)
- **MySQL Storage** for structured book data
- **Email Notifications** on success/failure
- **Visualization Output** → `/tmp/top_books.png`
- **Fully containerized** using Docker Compose (Airflow + MySQL + Postgres + Redis)

---
##  Architecture Flow
**Amazon Books → Airflow DAG → MySQL → Visualization → Email Notification**

Inside Docker:
- Airflow Webserver
- Airflow Scheduler
- MySQL
- PostgreSQL (Airflow metadata)
- Redis

---
##  Project Structure
```bash
fetch_with_docker/
├── dags/                # Airflow DAG definitions
├── assets/              # Architecture diagrams (e.g., .png)
├── docker-compose.yml   # Docker services configuration
├── requirements.txt     # Python dependencies
└── README.md            # This document
```

---
##  Quick Setup
### 1️ Build & Start Services
```bash
bash
docker-compose up --build -d
```

### 2️ Access Airflow
- URL: **http://localhost:8080**
- Credentials:
  ```bash
  user: airflow
  password: airflow
  ```

### 3️ Trigger DAG
- Open Airflow UI
- Look for: `amazon_books_pipeline`
- Turn it **ON**
- Click **Trigger DAG**

---
## 🗄️ MySQL Schema
| Column            | Type        | Description           |
|------------------|-------------|-----------------------|
| id               | INT         | Primary key           |
| title            | VARCHAR     | Book title            |
| author           | VARCHAR     | Book author           |
| rating           | FLOAT       | Cleaned rating        |
| recommended_flag | VARCHAR(3)  | Yes / No              |

---
## 🧪 DAG Tasks Overview
1. **fetch_book_data** → Fetch from Amazon
2. **clean_transform_data** → Process dataframe
3. **insert_into_mysql** → Store into MySQL
4. **generate_visualization** → Save `/tmp/top_books.png`
5. **send_email_notification** → SMTP email

---
## 🔌 Connecting Services
### Airflow → MySQL Connection
In Airflow UI:
- Go to **Admin → Connections**
- Add:
  ```bash
  Conn ID: mysql_default
  Conn Type: MySQL
  Host: mysql
  Login: root
  Password: root
  Schema: books_db
  Port: 3306
  ```

### Airflow SMTP Email
Set in `docker-compose.yml`:
```bash
AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
AIRFLOW__SMTP__SMTP_USER=your_email@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD=your_app_password
```

---
## Stop Services
```bash
docker-compose down
```
Reset everything:
```bash
docker-compose down -v
```

- **Email not working** → verify Gmail App Password


**Rawan Nada**  
Email: rwannada22@gmail.com  
LinkedIn: https://www.linkedin.com/in/rawan-nada-a63994281
