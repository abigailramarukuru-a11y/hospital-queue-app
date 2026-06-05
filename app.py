from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "hospital_secret_key"


def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            status TEXT DEFAULT 'Waiting'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (1, ?, ?)",
        ("admin", "admin123")
    )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect("/login")


@app.route("/search")
def search_page():
    return render_template("search.html")


@app.route("/search_patient", methods=["POST"])
def search_patient():
    name = request.form["name"]

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, department, status FROM patients WHERE name = ?",
        (name,)
    )

    patients = cursor.fetchall()
    conn.close()

    return render_template("search_results.html", patients=patients)


@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    department = request.form["department"]

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO patients (name, department, status) VALUES (?, ?, ?)",
        (name, department, "Waiting")
    )

    conn.commit()
    conn.close()

    return redirect("/queue")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/queue")

        return "Invalid username or password"

    return render_template("login.html")


@app.route("/queue")
def view_queue():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, department, status
        FROM patients
        WHERE status != 'Served'
    """)

    patients = cursor.fetchall()
    conn.close()

    queues = {
        "General": [],
        "Emergency": [],
        "Maternity": [],
        "Dental": []
    }

    for patient in patients:
        patient_id = patient[0]
        name = patient[1]
        department = patient[2]
        status = patient[3]

        if department not in queues:
            queues[department] = []

        ticket_number = len(queues[department]) + 1
        wait_time = (ticket_number - 1) * 15

        queues[department].append({
            "id": patient_id,
            "ticket": ticket_number,
            "name": name,
            "department": department,
            "status": status,
            "wait_time": wait_time
        })

    return render_template("queue.html", queues=queues)


@app.route("/call_next/<department>")
def call_next(department):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM patients
        WHERE department = ? AND status = 'Waiting'
        ORDER BY id
        LIMIT 1
    """, (department,))

    patient = cursor.fetchone()

    if patient:
        cursor.execute(
            "UPDATE patients SET status = 'In Consultation' WHERE id = ?",
            (patient[0],)
        )

        conn.commit()

    conn.close()

    return redirect("/queue")


@app.route("/serve/<int:id>")
def serve_patient(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE patients SET status = 'Served' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/queue")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]

        cursor.execute("""
            UPDATE patients
            SET name=?, department=?
            WHERE id=?
        """, (name, department, id))

        conn.commit()
        conn.close()

        return redirect("/queue")

    cursor.execute(
        "SELECT id, name, department, status FROM patients WHERE id=?",
        (id,)
    )

    patient = cursor.fetchone()
    conn.close()

    return render_template("edit.html", patient=patient)


@app.route("/stats")
def stats():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE department='General'")
    general = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE department='Emergency'")
    emergency = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE department='Maternity'")
    maternity = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE department='Dental'")
    dental = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "stats.html",
        total=total,
        general=general,
        emergency=emergency,
        maternity=maternity,
        dental=dental
    )


@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, department, status
        FROM patients
        WHERE status='Served'
    """)

    patients = cursor.fetchall()
    conn.close()

    return render_template("history.html", patients=patients)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
