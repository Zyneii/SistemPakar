import MySQLdb.cursors
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session
)
from flask_mysqldb import MySQL
from functools import wraps
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "aiSistemPakar"


# ======================================================
#  Dekorator LOGIN REQUIRED
# ======================================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin_logged_in" not in session:
            flash("Silakan login dulu!", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated



import os

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", 3306))


mail = Mail(app)

# ======================================================
#  KONFIG APLIKASI & DATABASE
# ======================================================


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "web_sistempakar"

mysql = MySQL(app)


# ======================================================
#  ROUTE: HALAMAN UTAMA
# ======================================================
@app.route("/")
def home():
    return render_template("index.html")




@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/send-contact', methods=['POST'])
def send_contact():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(
            subject=f"Contact Baru dari {name}",
            recipients=['emailtujuan@gmail.com'],
            body=f"""
Nama   : {name}
Email  : {email}

Pesan:
{message}
"""
        )

        mail.send(msg)
        print("EMAIL BERHASIL DIKIRIM")  # 👈 PENTING

        flash("Pesan berhasil dikirim!", "success")

    except Exception as e:
        print("ERROR EMAIL:", e)
        flash("Gagal mengirim pesan.", "danger")

    return redirect(url_for('contact'))



# ======================================================
#  ROUTE: LOGIN ADMIN
# ======================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password_input = request.form["password"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM admin WHERE username = %s",
            (username,)
        )
        admin = cursor.fetchone()
        cursor.close()

        if not admin:
            flash("Username tidak ditemukan!", "danger")
            return render_template("login.html")

        if admin["password"] != password_input:
            flash("Password salah!", "danger")
            return render_template("login.html")

        # Login berhasil
        session["admin_logged_in"] = True
        session["admin_username"] = admin["username"]
        flash("Berhasil login!", "success")
        return redirect(url_for("admin"))

    return render_template("login.html")


# ======================================================
#  ROUTE: DASHBOARD ADMIN
# ======================================================
@app.route("/admin")
@login_required
def admin():
    return render_template("dashboard_admin.html")


# ======================================================
#  ROUTE: LOGOUT ADMIN
# ======================================================
@app.route("/logout")
def logout():
    session.clear()
    flash("Berhasil logout", "info")
    return redirect(url_for("login"))


# ======================================================
#  ROUTE: HALAMAN DIAGNOSA
# ======================================================
@app.route("/diagnosa")
def halaman_diagnosa():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id_gejala, Nama_gejala,kategori FROM tb_gejala")
        semua_gejala = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(f"Error database: {e}", "danger")
        semua_gejala = []

    return render_template("diagnosa.html", daftar_gejala=semua_gejala)


# ======================================================
#  ROUTE: PROSES DIAGNOSA (FORWARD CHAINING)
# ======================================================
@app.route("/proses_diagnosa", methods=["POST"])
def proses_diagnosa():
    cursor = None
    try:
        # Ambil gejala dari user
        gejala_terpilih = request.form.getlist("gejala")
        print("DEBUG gejala_terpilih =", gejala_terpilih)

        if not gejala_terpilih:
            flash("Anda belum memilih gejala apapun.", "warning")
            return redirect(url_for("halaman_diagnosa"))

        # Jadikan SET untuk forward chaining
        facts = set(gejala_terpilih)
        print("DEBUG facts =", facts)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Ambil semua rule
        cursor.execute("SELECT * FROM tb_rules")
        rules = cursor.fetchall()
        print("DEBUG KEYS tb_rules:", list(rules[0].keys()))

        hasil_diagnosa = []

        # Forward Chaining
        for rule in rules:
            antecedent_list = {
                x.strip() for x in rule["antecedents"].split(",")
                if x.strip()
            }

            print("DEBUG antecedents =", antecedent_list)

            if antecedent_list.issubset(facts):
                print("MATCH RULE:", rule["antecedents"])

                cursor.execute(
                    "SELECT * FROM tb_penyakit WHERE id_penyakit = %s",
                    (rule["consequent_penyakit"],)
                )
                penyakit = cursor.fetchone()

                if penyakit:
                    hasil_diagnosa.append({
                        "nama": penyakit["Nama_penyakit"],
                        "solusi": (penyakit.get("solusi") or "").split("\n"),
                        "rule": rule["antecedents"]
                    })

        print("DEBUG hasil_diagnosa =", hasil_diagnosa)

        if not hasil_diagnosa:
            flash("Tidak ada penyakit yang cocok dengan gejala tersebut.", "info")
            return redirect(url_for("halaman_diagnosa"))

        return render_template("hasil.html", hasil=hasil_diagnosa)

    except Exception as e:
        print("DEBUG ERROR:", e)
        flash(f"Terjadi error: {e}", "danger")
        return redirect(url_for("halaman_diagnosa"))

    finally:
        if cursor:
            cursor.close()


@app.route("/hasil")
def halaman_hasil():
    return render_template("hasil.html")



# ===================================
# CRUD DATA GEJALA
# ===================================
@app.route('/gejala')
@login_required
def admin_gejala():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM tb_gejala")
    data = cursor.fetchall()
    cursor.close()

    return render_template("admin_data_gejala.html", gejala=data, active="gejala")

# --- TAMBAH GEJALA ---
@app.route('/gejala/tambah', methods=['POST'])
@login_required
def tambah_gejala():
    idg = request.form['id_gejala']
    nama = request.form['nama_gejala']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO tb_gejala (id_gejala, Nama_gejala) VALUES (%s,%s)", (idg, nama))
    mysql.connection.commit()
    cursor.close()

    flash("Gejala berhasil ditambahkan!", "success")
    return redirect(url_for('admin_gejala'))


# --- EDIT GEJALA ---
@app.route('/gejala/edit', methods=['POST'])
@login_required
def edit_gejala():
    idg = request.form['id_gejala']
    nama = request.form['nama_gejala']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE tb_gejala SET Nama_gejala=%s WHERE id_gejala=%s",
                   (nama, idg))
    mysql.connection.commit()
    cursor.close()

    flash("Gejala berhasil diperbarui!", "success")
    return redirect(url_for('admin_gejala'))

# --- HAPUS GEJALA ---
@app.route('/gejala/hapus/<id>', methods=['POST'])
@login_required
def hapus_gejala(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM tb_gejala WHERE id_gejala=%s", (id,))
    mysql.connection.commit()
    cursor.close()

    flash("Gejala berhasil dihapus!", "success")
    return redirect(url_for('admin_gejala'))



# ===================================
# CRUD DATA PENYAKIT
# ===================================
@app.route('/penyakit')
@login_required
def admin_penyakit():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM tb_penyakit")
    data = cursor.fetchall()
    cursor.close()

    return render_template("admin_data_penyakit.html", penyakit=data, active="penyakit")

# --- TAMBAH ---
@app.route('/penyakit/tambah', methods=['GET', 'POST'])
@login_required
def tambah_penyakit():
    if request.method == 'POST':
        idp = request.form['id_penyakit']
        nama = request.form['nama_penyakit']
        solusi = request.form['solusi']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO tb_penyakit (id_penyakit, Nama_penyakit, solusi) VALUES (%s,%s,%s)",
                       (idp, nama, solusi))
        mysql.connection.commit()
        cursor.close()

        flash("Penyakit berhasil ditambahkan!", "success")
        return redirect(url_for('admin_penyakit'))

    return render_template("form_penyakit.html")

# --- EDIT ---
@app.route('/penyakit/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_penyakit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM tb_penyakit WHERE id_penyakit=%s", (id,))
    data = cursor.fetchone()

    if request.method == 'POST':
        nama = request.form['nama_penyakit']
        solusi = request.form['solusi']

        cursor2 = mysql.connection.cursor()
        cursor2.execute("""
            UPDATE tb_penyakit SET Nama_penyakit=%s, solusi=%s WHERE id_penyakit=%s
        """, (nama, solusi, id))
        mysql.connection.commit()
        cursor2.close()

        flash("Berhasil diperbarui!", "success")
        return redirect(url_for('admin_penyakit'))

    return render_template("form_penyakit_edit.html", penyakit=data)

# --- HAPUS ---
@app.route('/penyakit/hapus/<id>', methods=['POST'])
@login_required
def hapus_penyakit(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM tb_penyakit WHERE id_penyakit=%s", (id,))
    mysql.connection.commit()
    cursor.close()

    flash("Penyakit berhasil dihapus!", "danger")
    return redirect(url_for('admin_penyakit'))

# ===================================
# CRUD RULE
# ===================================
@app.route('/rule')
@login_required
def admin_rule():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        SELECT r.id_rule, r.antecedents,
               p.Nama_penyakit AS penyakit
        FROM tb_rules r
        LEFT JOIN tb_penyakit p ON r.consequent_penyakit = p.id_penyakit
    """)
    data = cursor.fetchall()


    cursor.execute("SELECT * FROM tb_penyakit")
    penyakit = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin_data_rule.html",
        rules=data,
        penyakit=penyakit,     
        active="rule"
    )


# --- TAMBAH RULE ---
@app.route('/rule/tambah', methods=['GET', 'POST'])
@login_required
def tambah_rule():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM tb_gejala")
    gejala = cursor.fetchall()

    cursor.execute("SELECT * FROM tb_penyakit")
    penyakit = cursor.fetchall()

    if request.method == 'POST':
        idr = request.form['id_rule']
        antecedents = ",".join(request.form.getlist('gejala'))
        consequent = request.form['penyakit']

        cursor2 = mysql.connection.cursor()
        cursor2.execute("""
            INSERT INTO tb_rules (id_rule, antecedents, consequent_penyakit)
            VALUES (%s,%s,%s)
        """, (idr, antecedents, consequent))
        mysql.connection.commit()
        cursor2.close()

        flash("Rule berhasil ditambahkan!", "success")
        return redirect(url_for('admin_rule'))

    return render_template("form_rule.html", gejala=gejala, penyakit=penyakit)

# --- EDIT RULE ---
@app.route('/rule/edit/<string:id>', methods=['POST'])
@login_required
def edit_rule(id):
    id_rule = request.form['id_rule']
    antecedents = request.form['gejala']
    penyakit = request.form['penyakit']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE tb_rules
        SET id_rule=%s, antecedents=%s, consequent_penyakit=%s
        WHERE id_rule=%s
    """, (id_rule, antecedents, penyakit, id))

    mysql.connection.commit()
    cursor.close()

    flash("Rule berhasil diperbarui!", "success")
    return redirect(url_for('admin_rule'))

# --- HAPUS RULE ---
@app.route('/rule/hapus/<string:id>', methods=['POST'])
@login_required
def hapus_rule(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM tb_rules WHERE id_rule=%s", (id,))
    mysql.connection.commit()
    cursor.close()

    flash("Rule berhasil dihapus!", "danger")
    return redirect(url_for('admin_rule'))



app = Flask(__name__)
