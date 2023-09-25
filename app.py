from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
   host="localhost",
   user="root",
   database="employee_db"
)

@app.route('/')
def index():
   cursor = db.cursor(dictionary=True)
   cursor.execute("SELECT * FROM employees")
   employees = cursor.fetchall()
   cursor.close()
   return render_template('index.html', employees=employees)

@app.route('/add_employee', methods=['POST'])
def add_employee():
   cursor = db.cursor()
   name = request.form['name']
   salary = request.form['salary']
   doj = request.form['doj']
   cursor.execute("INSERT INTO employees (employee_name, salary, date_of_join) VALUES (%s, %s, %s)", (name, salary, doj))
   db.commit()
   cursor.close()
   return redirect('/')

@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
   cursor = db.cursor(dictionary=True)

   if request.method == 'POST':
       name = request.form['name']
       salary = request.form['salary']
       doj = request.form['doj']
       cursor.execute("UPDATE employees SET employee_name=%s, salary=%s, date_of_join=%s WHERE id=%s", (name, salary, doj, id))
       db.commit()
       return redirect('/')

   cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
   employee = cursor.fetchone()
   cursor.close()
   return render_template('edit_employee.html', employee=employee)

@app.route('/delete_employee/<int:id>')
def delete_employee(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    return redirect('/')

if __name__ == '__main__':
   app.run(debug=True)
