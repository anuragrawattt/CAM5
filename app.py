import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "railway_secret_2024")

def get_connection():
    try:
        conn = mysql.connector.connect(
            host     = os.getenv("DB_HOST",     "localhost"),
            user     = os.getenv("DB_USER",     "root"),
            password = os.getenv("DB_PASSWORD", ""),
            database = os.getenv("DB_NAME",     "railway_reservation")
        )
        return conn
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None

def db_execute(query, params=(), fetch=True):
    conn = get_connection()
    if conn is None:
        return (None, "Could not connect to the database. Check your MySQL settings.")
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        if fetch:
            rows = cur.fetchall()
            return (rows, None)
        else:
            conn.commit()
            return (cur.rowcount, None)
    except Error as e:
        return (None, f"Database error: {e.msg}")
    finally:
        conn.close()

@app.route("/")
def index():
    train_count,     _ = db_execute("SELECT COUNT(*) AS cnt FROM TRAIN")
    passenger_count, _ = db_execute("SELECT COUNT(*) AS cnt FROM PASSENGER")
    ticket_count,    _ = db_execute("SELECT COUNT(*) AS cnt FROM TICKET")
    total_fare,      _ = db_execute("SELECT SUM(Fare) AS total FROM TICKET")

    t_cnt  = train_count[0]["cnt"]     if train_count     else 0
    p_cnt  = passenger_count[0]["cnt"] if passenger_count else 0
    tk_cnt = ticket_count[0]["cnt"]    if ticket_count    else 0
    fare   = total_fare[0]["total"]    if total_fare and total_fare[0]["total"] else 0

    return render_template(
        "index.html",
        train_count=t_cnt,
        passenger_count=p_cnt,
        ticket_count=tk_cnt,
        total_fare=fare
    )

@app.route("/analytics")
def analytics():
    train_type_stats, _ = db_execute(
        "SELECT Type, COUNT(*) AS count FROM TRAIN GROUP BY Type ORDER BY count DESC"
    )

    payment_mode_stats, _ = db_execute(
        "SELECT Mode, COUNT(*) AS count, SUM(Amount) AS total_amount FROM PAYMENT GROUP BY Mode ORDER BY total_amount DESC"
    )

    ticket_fare_stats, _ = db_execute(
        "SELECT COUNT(*) AS total_tickets, SUM(Fare) AS total_fare, AVG(Fare) AS avg_fare, MIN(Fare) AS min_fare, MAX(Fare) AS max_fare FROM TICKET"
    )

    refund_stats, _ = db_execute(
        "SELECT COUNT(*) AS total_cancellations, SUM(Refund_Amount) AS total_refund, AVG(Refund_Amount) AS avg_refund FROM CANCELLATION"
    )

    platform_stats, _ = db_execute(
        "SELECT COUNT(*) AS total_platforms, AVG(Capacity) AS avg_capacity, MIN(Capacity) AS min_capacity, MAX(Capacity) AS max_capacity FROM PLATFORM"
    )

    max_train_count = max([item["count"] for item in train_type_stats]) if train_type_stats else 1
    for t in (train_type_stats or []):
        t["pct"] = round((t["count"] / max_train_count) * 100)

    max_amt = max([float(item["total_amount"]) for item in payment_mode_stats]) if payment_mode_stats else 1.0
    for p in (payment_mode_stats or []):
        p["pct"] = round((float(p["total_amount"]) / max_amt) * 100)

    return render_template(
        "analytics.html",
        train_type_stats=train_type_stats or [],
        payment_mode_stats=payment_mode_stats or [],
        ticket_fare_stats=ticket_fare_stats[0] if ticket_fare_stats else {},
        refund_stats=refund_stats[0] if refund_stats else {},
        platform_stats=platform_stats[0] if platform_stats else {}
    )

@app.route("/zones", methods=["GET", "POST"])
def zones():
    error   = None
    message = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            zone_id   = request.form.get("zone_id",   "").strip()
            zone_name = request.form.get("zone_name", "").strip()
            if not zone_id or not zone_name:
                error = "Both Zone ID and Zone Name are required."
            else:
                _, err = db_execute(
                    "INSERT INTO RAILWAY_ZONE (Zone_Id, Zone_Name) VALUES (%s, %s)",
                    (zone_id, zone_name), fetch=False
                )
                if err:
                    error = err
                else:
                    message = f"Zone '{zone_name}' added successfully."

        elif action == "delete":
            zone_id = request.form.get("zone_id", "").strip()
            if not zone_id:
                error = "Zone ID is required to delete."
            else:
                _, err = db_execute(
                    "DELETE FROM RAILWAY_ZONE WHERE Zone_Id = %s",
                    (zone_id,), fetch=False
                )
                if err:
                    error = err
                else:
                    message = f"Zone ID {zone_id} deleted (if it existed)."

    zones_data, db_err = db_execute("SELECT * FROM RAILWAY_ZONE ORDER BY Zone_Id")
    if db_err:
        error = db_err
        zones_data = []

    return render_template("zones.html", zones=zones_data, error=error, message=message)

@app.route("/stations", methods=["GET", "POST"])
def stations():
    error   = None
    message = None
    search_results = None
    search_term    = ""

    if request.method == "POST":
        code = request.form.get("station_code", "").strip().upper()
        name = request.form.get("station_name", "").strip()
        city = request.form.get("city", "").strip()
        zone = request.form.get("zone_id", "").strip() or None

        if not code or not name or not city:
            error = "Station Code, Name, and City are all required."
        else:
            _, err = db_execute(
                "INSERT INTO STATION (Station_Code, Station_Name, City, Zone_Id) VALUES (%s,%s,%s,%s)",
                (code, name, city, zone), fetch=False
            )
            if err:
                error = err
            else:
                message = f"Station '{name}' ({code}) added."

    search_term = request.args.get("search", "").strip()
    if search_term:
        search_results, err = db_execute(
            "SELECT * FROM STATION WHERE Station_Name LIKE %s OR City LIKE %s ORDER BY Station_Name",
            (f"%{search_term}%", f"%{search_term}%")
        )
        if err:
            error = err
            search_results = []

    all_stations, db_err = db_execute("SELECT * FROM STATION ORDER BY Station_Name")
    if db_err:
        error = db_err
        all_stations = []

    return render_template(
        "stations.html",
        stations=all_stations,
        search_results=search_results,
        search_term=search_term,
        error=error, message=message
    )

@app.route("/trains", methods=["GET", "POST"])
def trains():
    error   = None
    message = None
    search_results = None
    search_term    = ""
    sort_by        = request.args.get("sort", "")

    if request.method == "POST":
        train_no   = request.form.get("train_no",   "").strip()
        train_name = request.form.get("train_name", "").strip()
        t_type     = request.form.get("type",       "").strip()
        zone       = request.form.get("zone_id",    "").strip() or None

        if not train_no or not train_name or not t_type:
            error = "Train No, Name, and Type are required."
        else:
            _, err = db_execute(
                "INSERT INTO TRAIN (Train_No, Train_Name, Type, Zone_Id) VALUES (%s,%s,%s,%s)",
                (train_no, train_name, t_type, zone), fetch=False
            )
            if err:
                error = err
            else:
                message = f"Train {train_no} – '{train_name}' added."

    search_term = request.args.get("search", "").strip()
    if search_term:
        search_results, err = db_execute(
            "SELECT * FROM TRAIN WHERE Train_Name LIKE %s OR Type LIKE %s ORDER BY Train_Name",
            (f"%{search_term}%", f"%{search_term}%")
        )
        if err:
            error = err
            search_results = []

    if sort_by == "name":
        all_trains, db_err = db_execute("SELECT * FROM TRAIN ORDER BY Train_Name ASC")
    else:
        all_trains, db_err = db_execute("SELECT * FROM TRAIN ORDER BY Train_No")

    if db_err:
        error = db_err
        all_trains = []

    return render_template(
        "trains.html",
        trains=all_trains,
        search_results=search_results,
        search_term=search_term,
        sort_by=sort_by,
        error=error, message=message
    )

@app.route("/coaches", methods=["GET", "POST"])
def coaches():
    error   = None
    message = None

    if request.method == "POST":
        coach_no   = request.form.get("coach_no",   "").strip().upper()
        coach_type = request.form.get("coach_type", "").strip()
        train_no   = request.form.get("train_no",   "").strip() or None

        if not coach_no or not coach_type:
            error = "Coach No and Coach Type are required."
        else:
            _, err = db_execute(
                "INSERT INTO COACH (Coach_No, Coach_Type, Train_No) VALUES (%s,%s,%s)",
                (coach_no, coach_type, train_no), fetch=False
            )
            if err:
                error = err
            else:
                message = f"Coach '{coach_no}' ({coach_type}) added."

    all_coaches, db_err = db_execute(
        "SELECT C.Coach_No, C.Coach_Type, C.Train_No, T.Train_Name "
        "FROM COACH C LEFT JOIN TRAIN T ON C.Train_No = T.Train_No "
        "ORDER BY C.Coach_No"
    )
    if db_err:
        error = db_err
        all_coaches = []

    all_trains, _ = db_execute("SELECT Train_No, Train_Name FROM TRAIN ORDER BY Train_Name")

    return render_template(
        "coaches.html",
        coaches=all_coaches,
        trains=all_trains or [],
        error=error, message=message
    )

@app.route("/passengers", methods=["GET", "POST"])
def passengers():
    error   = None
    message = None
    search_results = None
    search_term    = ""

    if request.method == "POST":
        name = request.form.get("passenger_name", "").strip()
        dob  = request.form.get("dob", "").strip()

        if not name or not dob:
            error = "Passenger Name and Date of Birth are required."
        else:
            _, err = db_execute(
                "INSERT INTO PASSENGER (Passenger_Name, DOB) VALUES (%s, %s)",
                (name, dob), fetch=False
            )
            if err:
                error = err
            else:
                message = f"Passenger '{name}' added successfully."

    search_term = request.args.get("search", "").strip()
    if search_term:
        search_results, err = db_execute(
            "SELECT * FROM PASSENGER WHERE Passenger_Name LIKE %s ORDER BY Passenger_Name",
            (f"%{search_term}%",)
        )
        if err:
            error = err
            search_results = []

    all_passengers, db_err = db_execute("SELECT * FROM PASSENGER ORDER BY Passenger_Id")
    if db_err:
        error = db_err
        all_passengers = []

    return render_template(
        "passengers.html",
        passengers=all_passengers,
        search_results=search_results,
        search_term=search_term,
        error=error, message=message
    )

@app.route("/tickets", methods=["GET", "POST"])
def tickets():
    error   = None
    message = None
    search_results = None
    search_date    = ""

    if request.method == "POST":
        journey_date  = request.form.get("journey_date",  "").strip()
        fare          = request.form.get("fare",          "").strip()
        passenger_id  = request.form.get("passenger_id",  "").strip() or None
        train_no      = request.form.get("train_no",      "").strip() or None
        coach_no      = request.form.get("coach_no",      "").strip().upper() or None

        if not journey_date or not fare:
            error = "Journey Date and Fare are required."
        else:
            try:
                fare_val = float(fare)
            except ValueError:
                error = "Fare must be a valid number."
                fare_val = None

            if fare_val is not None:
                _, err = db_execute(
                    "INSERT INTO TICKET (Journey_Date, Fare, Passenger_Id, Train_No, Coach_No) "
                    "VALUES (%s,%s,%s,%s,%s)",
                    (journey_date, fare_val, passenger_id, train_no, coach_no), fetch=False
                )
                if err:
                    error = err
                else:
                    message = "Ticket booked successfully."

    search_date = request.args.get("date", "").strip()
    if search_date:
        search_results, err = db_execute(
            "SELECT T.*, P.Passenger_Name, TR.Train_Name "
            "FROM TICKET T "
            "LEFT JOIN PASSENGER P  ON T.Passenger_Id = P.Passenger_Id "
            "LEFT JOIN TRAIN TR     ON T.Train_No     = TR.Train_No "
            "WHERE T.Journey_Date = %s ORDER BY T.Ticket_No",
            (search_date,)
        )
        if err:
            error = err
            search_results = []

    total_fare_row, _ = db_execute("SELECT SUM(Fare) AS total FROM TICKET")
    total_fare = total_fare_row[0]["total"] if total_fare_row and total_fare_row[0]["total"] else 0

    all_tickets, db_err = db_execute(
        "SELECT T.*, P.Passenger_Name, TR.Train_Name "
        "FROM TICKET T "
        "LEFT JOIN PASSENGER P  ON T.Passenger_Id = P.Passenger_Id "
        "LEFT JOIN TRAIN TR     ON T.Train_No     = TR.Train_No "
        "ORDER BY T.Ticket_No"
    )
    if db_err:
        error = db_err
        all_tickets = []

    all_passengers, _ = db_execute("SELECT Passenger_Id, Passenger_Name FROM PASSENGER ORDER BY Passenger_Name")
    all_trains,     _ = db_execute("SELECT Train_No, Train_Name FROM TRAIN ORDER BY Train_Name")
    all_coaches,    _ = db_execute("SELECT Coach_No, Coach_Type FROM COACH ORDER BY Coach_No")

    return render_template(
        "tickets.html",
        tickets=all_tickets,
        search_results=search_results,
        search_date=search_date,
        total_fare=total_fare,
        passengers=all_passengers or [],
        trains=all_trains or [],
        coaches=all_coaches or [],
        error=error, message=message
    )

@app.route("/employees", methods=["GET"])
def employees():
    error  = None
    search_results = None
    search_term    = request.args.get("search", "").strip()

    if search_term:
        search_results, err = db_execute(
            "SELECT * FROM EMPLOYEE WHERE Ename LIKE %s OR Designation LIKE %s ORDER BY Ename",
            (f"%{search_term}%", f"%{search_term}%")
        )
        if err:
            error = err
            search_results = []

    all_employees, db_err = db_execute("SELECT * FROM EMPLOYEE ORDER BY Eid")
    if db_err:
        error = db_err
        all_employees = []

    return render_template(
        "employees.html",
        employees=all_employees,
        search_results=search_results,
        search_term=search_term,
        error=error
    )

@app.route("/platforms", methods=["GET"])
def platforms():
    error  = None
    search_results = None
    min_cap = request.args.get("min_capacity", "").strip()

    if min_cap:
        try:
            cap_val = int(min_cap)
            search_results, err = db_execute(
                "SELECT PL.*, S.Station_Name FROM PLATFORM PL "
                "LEFT JOIN STATION S ON PL.Station_Code = S.Station_Code "
                "WHERE PL.Capacity >= %s ORDER BY PL.Capacity DESC",
                (cap_val,)
            )
            if err:
                error = err
                search_results = []
        except ValueError:
            error = "Please enter a valid number for minimum capacity."

    all_platforms, db_err = db_execute(
        "SELECT PL.*, S.Station_Name FROM PLATFORM PL "
        "LEFT JOIN STATION S ON PL.Station_Code = S.Station_Code "
        "ORDER BY PL.Platform_No"
    )
    if db_err:
        error = db_err
        all_platforms = []

    return render_template(
        "platforms.html",
        platforms=all_platforms,
        search_results=search_results,
        min_cap=min_cap,
        error=error
    )

@app.route("/payments", methods=["GET"])
def payments():
    error  = None
    search_results = None
    filter_mode    = request.args.get("mode", "").strip()

    if filter_mode:
        search_results, err = db_execute(
            "SELECT * FROM PAYMENT WHERE Mode = %s ORDER BY Payment_Id",
            (filter_mode,)
        )
        if err:
            error = err
            search_results = []

    all_payments, db_err = db_execute("SELECT * FROM PAYMENT ORDER BY Payment_Id")
    if db_err:
        error = db_err
        all_payments = []

    return render_template(
        "payments.html",
        payments=all_payments,
        search_results=search_results,
        filter_mode=filter_mode,
        error=error
    )

@app.route("/cancellations", methods=["GET"])
def cancellations():
    error  = None
    search_results = None
    min_refund     = request.args.get("min_refund", "").strip()

    if min_refund:
        try:
            refund_val = float(min_refund)
            search_results, err = db_execute(
                "SELECT * FROM CANCELLATION WHERE Refund_Amount >= %s ORDER BY Refund_Amount DESC",
                (refund_val,)
            )
            if err:
                error = err
                search_results = []
        except ValueError:
            error = "Please enter a valid number for minimum refund amount."

    all_cancellations, db_err = db_execute(
        "SELECT C.*, T.Journey_Date, T.Fare "
        "FROM CANCELLATION C "
        "LEFT JOIN TICKET T ON C.Ticket_No = T.Ticket_No "
        "ORDER BY C.Cancel_Id"
    )
    if db_err:
        error = db_err
        all_cancellations = []

    total_refund_row, _ = db_execute("SELECT SUM(Refund_Amount) AS total FROM CANCELLATION")
    total_refund = total_refund_row[0]["total"] if total_refund_row and total_refund_row[0]["total"] else 0

    return render_template(
        "cancellations.html",
        cancellations=all_cancellations,
        search_results=search_results,
        min_refund=min_refund,
        total_refund=total_refund,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
