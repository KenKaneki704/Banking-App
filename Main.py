from flask import Flask, render_template, url_for, redirect, request, session, flash
import sqlite3
import random
import smtplib
from email.message import EmailMessage
import ssl
email_sender = "yasoobkazmi1243@gmail.com"
email_password = 'ftcv gbgc nrrp kkrs'


app = Flask(__name__)
conn = sqlite3.connect('Bank_Details_DB.db', check_same_thread=False)
c = conn.cursor()

app.secret_key = "dev"

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        banking_id = request.form.get("unique_ID")
        password = request.form.get("pswd")
        session["banking_id_store"] = banking_id
        session["password_store"] = password
        return validate_credentials(banking_id, password)
    return render_template('Basic.html')

def validate_credentials(banking_id, password):
    conn = sqlite3.connect('Bank_Details_DB.db', check_same_thread=False)
    query = "SELECT * FROM customer_details WHERE unique_id=? AND password=?"

    try:
        cursor = conn.cursor()
        cursor.execute(query, (banking_id, password))
        result = cursor.fetchone()

        if result:
            flash("You Have Successfully Logged IN")
            return redirect(url_for('details'))
        else:
            return "INVALID CREDENTIALS"
            
    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        conn.close()

@app.route('/')
def indexing():
    return render_template('indexing.html')

@app.route('/details', methods=["POST", "GET"])
def details():
    withdrawl = request.form.get("withdrawl-")
    deposit = request.form.get("deposit-")
    banking_id_store = session["banking_id_store"]
    password_store = session["password_store"]

    if withdrawl is not None and withdrawl != "":
        int_withdrawl = int(withdrawl)
        c.execute("UPDATE customer_details SET bank_amount = bank_amount - ? WHERE unique_id = ? AND password = ?", (int_withdrawl, banking_id_store, password_store))
        conn.commit()

    if deposit is not None and deposit != "":
        amount = int(deposit)
        c.execute("UPDATE customer_details SET bank_amount = bank_amount + ? WHERE unique_id = ? AND password = ?", (amount, banking_id_store, password_store))
        conn.commit()

    # Fetch the updated Total_Balance after potential updates
    bank_balance = c.execute("SELECT bank_amount FROM customer_details WHERE unique_id = ?", (banking_id_store,))
    result = bank_balance.fetchone()
    Total_Balance = result[0]

    return render_template('details.html', Total_Balance=Total_Balance)

bank_id = random.randrange(10000, 100000)
@app.route("/Page2.html", methods = ["GET", "POST"])
def Page2():
    if request.method == "POST":
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        email = request.form.get("email-")
        contact_no = request.form.get("telephone")
        address = request.form.get("address-")
        age = request.form.get("age-")
        password = request.form.get("password-")
        conn.commit()
        return SIGN_UP(first_name, last_name, email, contact_no, address, age, password)
    conn.commit()
    return render_template("Page2.html")

@app.route('/sending_email')
def sending_email():
    Email_store = session["Email_store"]
    Bank_id_store = session["Bank_id_Store"]
    subject = 'Bank ID'

    body = """
    The Bank ID for your bank is """ + str(Bank_id_store)

    em = EmailMessage()

    em['From'] = email_sender
    em['To'] = Email_store
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, Email_store, em.as_string())
    conn.commit()

    return render_template('sending_email.html')


def SIGN_UP(first_name, last_name, email, contact_no, address, age, password):
    conn = sqlite3.connect('Bank_Details_DB.db', check_same_thread=False)
    unique_id  = bank_id
    session["Bank_id_Store"] = unique_id
    bank_amount = 0
    all_data = [bank_amount,unique_id,first_name,last_name,email,contact_no,address,age,password]
    c.execute("INSERT INTO customer_details(bank_amount,unique_id,first_name,last_name,email,contact_no,address,age,password) VALUES(?,?,?,?,?,?,?,?,?)", all_data)
    session["Email_store"] = email
    conn.commit()
    conn.close()
    try:
        return render_template('Page2.html')
    finally:
        return redirect(url_for("sending_email"))
            




if __name__ == "__main__":
    app.run(debug=True)
conn.commit()

conn.close()

