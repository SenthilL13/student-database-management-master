from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "123"

# Create database if not exists
con = sqlite3.connect("database.db")
con.execute(
    """CREATE TABLE IF NOT EXISTS student_record(
        reg_no INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT,
        dob DATE,
        sex TEXT,
        department TEXT,
        address TEXT,
        contact INTEGER,
        mail TEXT)      
    """
)
con.close()


# Home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


# Add student record page
@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/addata', methods=['POST', 'GET'])
def addata():
    if request.method == "POST":
        try:
            name = request.form['name']
            dob = request.form['dob']
            sex = request.form['sex']
            department = request.form['department']
            address = request.form['address']
            contact = request.form['contact']
            mail = request.form['mail']
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            sqlstr = "INSERT INTO student_record (name, dob, sex, department, address, contact, mail) VALUES (?, ?, ?, ?, ?, ?, ?)"
            print(sqlstr)
            cur.execute(sqlstr,(name, dob, sex, department, address, contact, mail))
            con.commit()

        except Exception as e:
            return jsonify(str(e))
        finally:
            con.close()
            return redirect(url_for("view"))


# View records
@app.route('/view')
def view():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM student_record")
    data = cur.fetchall()
    con.close()
    return render_template("view.html", student_record=data)


# Fetch specific record by name
@app.route('/fetch')
def fetch():
    return render_template('fetch.html')


@app.route('/fetchdata', methods=['POST'])
def fetchdata():
    if request.method == 'POST':
        name = request.form['name']
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM student_record WHERE name=?", (name,))
        data = cur.fetchall()
        con.close()
        return render_template("view.html", student_record=data)


# Fetch student for update
@app.route('/update')
def update_select():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM student_record")
    data = cur.fetchall()
    con.close()
    return render_template('update_select.html', student_record=data)





# Update the record
@app.route("/update/<int:reg_no>", methods=["POST", "GET"])
def update(reg_no):
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM student_record WHERE reg_no=?", (reg_no,))
    data = cur.fetchone()
    con.close()

    if request.method == 'POST':
        try:
            name = request.form['name']
            dob = request.form['dob']
            sex = request.form['sex']
            department = request.form['department']
            address = request.form['address']
            contact = request.form['contact']
            mail = request.form['mail']
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute(
                "UPDATE student_record SET name=?, dob=?, sex=?, department=?, address=?, contact=?, mail=? WHERE "
                "reg_no=?",
                (name, dob, sex, department, address, contact, mail, reg_no))
            con.commit()


        except Exception as e:
            return jsonify(str(e), "danger")

        finally:
            con.close()
            return redirect(url_for("home"))

    return render_template('update.html', student_record=data)


# Delete record
@app.route('/delete/<int:reg_no>')
def delete(reg_no):
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM student_record WHERE reg_no=?", (reg_no,))
        con.commit()


    except Exception as e:
        return jsonify(str(e), "danger")

    finally:
        con.close()
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
