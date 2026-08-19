from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection

app = Flask(__name__)

app.secret_key = "royalstay_hotel_secret_key"


# =========================================================
# DEMO LOGIN ACCOUNTS
# =========================================================

DEMO_ACCOUNTS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },

    "guest": {
        "password": "guest123",
        "role": "user"
    }
}


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    return render_template("index.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # -------------------------------------------------
        # FIRST CHECK DEMO ACCOUNTS
        # -------------------------------------------------

        if username in DEMO_ACCOUNTS:

            account = DEMO_ACCOUNTS[username]

            if password == account["password"]:

                session["user_id"] = username
                session["username"] = username
                session["role"] = account["role"]

                if account["role"] == "admin":
                    return redirect(url_for("dashboard"))

                else:
                    return redirect(url_for("guest_home"))

            else:

                error = "Invalid username or password."

        else:

            # -------------------------------------------------
            # CHECK MYSQL USERS TABLE
            # -------------------------------------------------

            connection = get_db_connection()

            if connection:

                cursor = connection.cursor(dictionary=True)

                query = """
                    SELECT *
                    FROM users
                    WHERE username = %s
                    AND password = %s
                """

                cursor.execute(
                    query,
                    (username, password)
                )

                user = cursor.fetchone()

                cursor.close()
                connection.close()

                if user:

                    session["user_id"] = user["user_id"]
                    session["username"] = user["username"]
                    session["role"] = user["role"]

                    if user["role"] == "admin":
                        return redirect(url_for("dashboard"))

                    else:
                        return redirect(url_for("guest_home"))

                else:

                    error = "Invalid username or password."

            else:

                error = "Unable to connect to database."

    return render_template(
        "login.html",
        error=error
    )


# =========================================================
# NORMAL USER HOME
# =========================================================

@app.route("/guest-home")
def guest_home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") == "admin":
        return redirect(url_for("dashboard"))

    return render_template("guest_home.html")


# =========================================================
# ADMIN ACCESS CHECK
# =========================================================

def admin_required():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return redirect(url_for("guest_home"))

    return None


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    access = admin_required()

    if access:
        return access

    connection = get_db_connection()

    stats = {
        "rooms": 0,
        "guests": 0,
        "bookings": 0,
        "payments": 0
    }

    if connection:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM rooms"
        )

        stats["rooms"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM guests"
        )

        stats["guests"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM bookings"
        )

        stats["bookings"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM payments"
        )

        stats["payments"] = cursor.fetchone()[0]

        cursor.close()
        connection.close()

    return render_template(
        "dashboard.html",
        stats=stats
    )


# =========================================================
# ROOMS
# =========================================================

@app.route("/rooms")
def rooms():

    access = admin_required()

    if access:
        return access

    connection = get_db_connection()

    rooms_data = []

    if connection:

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM rooms
            ORDER BY room_id DESC
            """
        )

        rooms_data = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template(
        "rooms.html",
        rooms=rooms_data
    )


# =========================================================
# BOOKINGS
# =========================================================

@app.route("/booking")
def booking():

    access = admin_required()

    if access:
        return access

    connection = get_db_connection()

    bookings = []

    if connection:

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                bookings.booking_id,
                guests.first_name,
                guests.last_name,
                rooms.room_number,
                rooms.room_type,
                bookings.check_in,
                bookings.check_out,
                bookings.number_of_guests,
                bookings.booking_status,
                bookings.total_amount

            FROM bookings

            INNER JOIN guests
                ON bookings.guest_id = guests.guest_id

            INNER JOIN rooms
                ON bookings.room_id = rooms.room_id

            ORDER BY bookings.booking_id DESC
        """

        cursor.execute(query)

        bookings = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template(
        "booking.html",
        bookings=bookings
    )


# =========================================================
# GUESTS
# =========================================================

@app.route("/guests")
def guests():

    access = admin_required()

    if access:
        return access

    connection = get_db_connection()

    guests_data = []

    if connection:

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM guests
            ORDER BY guest_id DESC
            """
        )

        guests_data = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template(
        "guests.html",
        guests=guests_data
    )


# =========================================================
# PAYMENTS
# =========================================================

@app.route("/payments")
def payments():

    access = admin_required()

    if access:
        return access

    connection = get_db_connection()

    payments_data = []

    if connection:

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                payments.payment_id,
                payments.booking_id,
                guests.first_name,
                guests.last_name,
                payments.amount,
                payments.payment_method,
                payments.payment_status,
                payments.payment_date

            FROM payments

            INNER JOIN bookings
                ON payments.booking_id = bookings.booking_id

            INNER JOIN guests
                ON bookings.guest_id = guests.guest_id

            ORDER BY payments.payment_id DESC
        """

        cursor.execute(query)

        payments_data = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template(
        "payments.html",
        payments=payments_data
    )


# =========================================================
# STAFF
# =========================================================

@app.route("/staff")
def staff():

    access = admin_required()

    if access:
        return access

    connection = get_db_connection()

    staff_data = []

    if connection:

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM staff
            ORDER BY staff_id DESC
            """
        )

        staff_data = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template(
        "staff.html",
        staff=staff_data
    )


# =========================================================
# REPORTS
# =========================================================

@app.route("/reports")
def reports():

    access = admin_required()

    if access:
        return access

    connection = get_db_connection()

    report = {
        "total_rooms": 0,
        "available_rooms": 0,
        "occupied_rooms": 0,
        "total_guests": 0,
        "total_bookings": 0,
        "total_revenue": 0
    }

    if connection:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM rooms"
        )

        report["total_rooms"] = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM rooms
            WHERE status = 'Available'
            """
        )

        report["available_rooms"] = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM rooms
            WHERE status = 'Occupied'
            """
        )

        report["occupied_rooms"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM guests"
        )

        report["total_guests"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM bookings"
        )

        report["total_bookings"] = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM payments
            WHERE payment_status = 'Paid'
            """
        )

        report["total_revenue"] = cursor.fetchone()[0]

        cursor.close()
        connection.close()

    return render_template(
        "reports.html",
        report=report
    )


# =========================================================
# SETTINGS
# =========================================================

@app.route("/settings")
def settings():

    access = admin_required()

    if access:
        return access

    return render_template(
        "settings.html"
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )