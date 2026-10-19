# Railway Reservation System (DBMS / CAM-5 Assignment)

A simple, student-friendly **Railway Reservation System** web application developed with **Python Flask**, **MySQL**, and **HTML/CSS**.

---

## 1. Project Overview

- **Front-End:** Plain HTML5 and basic custom CSS (No Bootstrap, no external frameworks, no complicated JS).
- **Back-End:** Python 3 + Flask.
- **Database:** MySQL (using `mysql-connector-python`).
- **Templating:** Jinja2 templates extending `base.html`.

The application demonstrates database-driven CRUD operations, parameterized SQL queries, searches via `LIKE`, sorting, filtering, and aggregate queries (`COUNT`, `SUM`).

---

## 2. Database Schema Details

Database name: `railway_reservation`

Contains 10 tables meeting all assignment criteria:
1. `RAILWAY_ZONE (Zone_Id, Zone_Name)` - Primary key `Zone_Id`.
2. `STATION (Station_Code, Station_Name, City, Zone_Id)` - Primary key `Station_Code`, FK referencing `RAILWAY_ZONE(Zone_Id)`.
3. `TRAIN (Train_No, Train_Name, Type, Zone_Id)` - Primary key `Train_No`, FK referencing `RAILWAY_ZONE(Zone_Id)`.
4. `COACH (Coach_No, Coach_Type, Train_No)` - Primary key `Coach_No`, FK referencing `TRAIN(Train_No)`.
5. `PASSENGER (Passenger_Id, Passenger_Name, DOB)` - Primary key `Passenger_Id` (AUTO_INCREMENT).
6. `TICKET (Ticket_No, Journey_Date, Fare, Passenger_Id, Train_No, Coach_No)` - Primary key `Ticket_No`, FKs to `PASSENGER`, `TRAIN`, and `COACH`.
7. `EMPLOYEE (Eid, Ename, Designation, Zone_Id)` - Primary key `Eid`, FK referencing `RAILWAY_ZONE(Zone_Id)`.
8. `PLATFORM (Platform_No, Capacity, Station_Code)` - Primary key `Platform_No`, FK referencing `STATION(Station_Code)`.
9. `PAYMENT (Payment_Id, Amount, Mode, Ticket_No)` - Primary key `Payment_Id`, FK referencing `TICKET(Ticket_No)`.
10. `CANCELLATION (Cancel_Id, Refund_Amount, Ticket_No)` - Primary key `Cancel_Id`, FK referencing `TICKET(Ticket_No)`.

---

## 3. SQL Queries Mapping (Assignment Demonstrations)

| Feature / Requirement | SQL Query Used in Backend | Page Location |
|---|---|---|
| **1. Display all records** | `SELECT * FROM <TABLE_NAME>` | All pages |
| **2. Search stations by city/name** | `SELECT * FROM STATION WHERE Station_Name LIKE %s OR City LIKE %s` | `/stations` |
| **3. Search trains by name or type** | `SELECT * FROM TRAIN WHERE Train_Name LIKE %s OR Type LIKE %s` | `/trains` |
| **4. Search passengers by name** | `SELECT * FROM PASSENGER WHERE Passenger_Name LIKE %s` | `/passengers` |
| **5. Filter tickets by journey date** | `SELECT * FROM TICKET WHERE Journey_Date = %s` | `/tickets` |
| **6. Filter payments by payment mode** | `SELECT * FROM PAYMENT WHERE Mode = %s` | `/payments` |
| **7. Sort trains by name** | `SELECT * FROM TRAIN ORDER BY Train_Name ASC` | `/trains?sort=name` |
| **8. Total trains & passengers (Aggregate)** | `SELECT COUNT(*) AS cnt FROM TRAIN` / `FROM PASSENGER` | `/` (Home page) |
| **9. Total ticket fare (Aggregate)** | `SELECT SUM(Fare) AS total FROM TICKET` | `/` and `/tickets` |
| **10. Total refund amount (Aggregate)** | `SELECT SUM(Refund_Amount) AS total FROM CANCELLATION` | `/cancellations` |
| **Search platform by capacity** | `SELECT * FROM PLATFORM WHERE Capacity >= %s ORDER BY Capacity DESC` | `/platforms` |
| **Search cancellation by refund** | `SELECT * FROM CANCELLATION WHERE Refund_Amount >= %s` | `/cancellations` |

---

## 4. How to Set Up and Run in VS Code

### Step 1: Open the Project in VS Code
Open VS Code, choose **File > Open Folder...**, and select the `railway_reservation` folder:
`c:\Users\anura\Downloads\da3dbms\railway_reservation`

### Step 2: Set Up MySQL Database
1. Open MySQL Command Line Client, MySQL Workbench, or run via terminal:
   ```bash
   mysql -u root -p
   ```
2. Run the `schema.sql` script to create the database, tables, and sample data:
   ```sql
   source c:/Users/anura/Downloads/da3dbms/railway_reservation/schema.sql;
   ```
   *(Or copy-paste the contents of `schema.sql` into MySQL Workbench / phpMyAdmin SQL query window and click Execute).*

### Step 3: Configure Database Credentials in `.env`
Open the `.env` file in the project folder and adjust your MySQL password:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_actual_mysql_password
DB_NAME=railway_reservation
SECRET_KEY=railway_secret_2024
```

### Step 4: Install Dependencies
Open a PowerShell or Command Prompt terminal in VS Code (`Ctrl + ~`) and run:
```powershell
pip install -r requirements.txt
```

### Step 5: Start the Flask Application
Run:
```powershell
python app.py
```

### Step 6: Open in Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

You can now navigate between all 11 pages using the navigation bar, search and filter records, and add or delete data.
