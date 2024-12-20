from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sam26&S10",
        database="hr_dashboard"
    )

# Helper function to convert timedelta to a string
def convert_timedelta_to_str(timedelta_obj):
    if isinstance(timedelta_obj, timedelta):
        return str(timedelta_obj)  # Convert to a string representation
    return timedelta_obj

# Helper function to format time
def format_time(time_obj):
    if isinstance(time_obj, datetime):  # If it's a datetime object
        return time_obj.strftime('%H:%M:%S')
    elif isinstance(time_obj, timedelta):  # If it's a timedelta object
        total_seconds = int(time_obj.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f'{hours:02}:{minutes:02}:{seconds:02}'
    return None

# -------------------- Route: Home --------------------

@app.route('/')
@app.route('/dashboard')
def dashboard():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # 1. Total Employees
        cursor.execute("SELECT COUNT(*) as total_employees FROM employee")
        total_employees = cursor.fetchone()['total_employees']

        # 2. Leaves This Month
        current_month = datetime.now().month
        cursor.execute("""
            SELECT COUNT(*) as total_leaves 
            FROM leave_requests 
            WHERE MONTH(start_date) = %s
        """, (current_month,))
        total_leaves = cursor.fetchone()['total_leaves']

        # 3. New Employees This Month
        cursor.execute("""
        SELECT COUNT(*) as new_employees
        FROM employee
        WHERE employee_id >= (
            SELECT COALESCE(MAX(employee_id), 0) 
            FROM employee
            WHERE DATE_SUB(CURDATE(), INTERVAL 1 MONTH) <= CURDATE()
        )
        """)
        new_employees = cursor.fetchone()['new_employees']

        # 4. Women Ratio
        cursor.execute("SELECT COUNT(*) as total_women FROM employee WHERE gender = 'Female'")
        total_women = cursor.fetchone()['total_women']
        women_ratio = round((total_women / total_employees) * 100, 2)

        # Close the connection
        connection.close()

        # Pass data to the dashboard
        return render_template('dashboard.html', 
            total_employees=total_employees, 
            total_leaves=total_leaves,
            new_employees=new_employees,
            women_ratio=women_ratio
        )

    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Error loading dashboard"
    
@app.route('/today-attendance', methods=['GET'])
def gettoday_attendance():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Query to count today's attendance
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE DATE(login_time) = CURDATE()")
        logged_in = cursor.fetchone()[0]

        # Query to count the total number of employees
        cursor.execute("SELECT COUNT(*) FROM employee")
        total_employees = cursor.fetchone()[0]
    finally:
        # Ensure proper cleanup
        cursor.close()
        connection.close()

    # Return JSON response with both logged-in and total employees
    return jsonify({
        'loggedIn': logged_in,
        'totalEmployees': total_employees
    })

@app.route('/get_funnel_chart_data')
def get_funnel_chart_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Query the database for hiring and termination data
        cursor.execute("SELECT month, num_hirings AS hirings, num_terminations AS terminations FROM hiring")
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/salary-data', methods=['GET'])
def get_salary_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Query all salary distribution data
        cursor.execute("SELECT department, entry_level, junior, mid_level, senior, leader, manager FROM salary_distribution")
        salary_data = cursor.fetchall()

        # Prepare the response data
        labels = ["Entry Level", "Junior", "Mid-Level", "Senior", "Leader", "Manager"]
        series = []

        # For each department, add the salary values to the series
        for department in salary_data:
            series.append({
                "name": department['department'],
                "data": [
                    department['entry_level'],
                    department['junior'],
                    department['mid_level'],
                    department['senior'],
                    department['leader'],
                    department['manager']
                ]
            })

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return the data as JSON
        return jsonify({
            "labels": labels,
            "series": series
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/data', methods=['GET'])
def getchart_data():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Query to Count Statuses
    query = """
    SELECT status, COUNT(*) as count 
    FROM employee 
    GROUP BY status
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    
    # Map Status to Colors
    color_map = {
        'Intern': '#FF6B6B',
        'Permanent': '#4ECDC4',
        'Temporary': '#45B7D1'
    }

    # Format the Data for the Frontend
    chart_data = [
        {'label': row['status'], 'value': row['count'], 'color': color_map[row['status']]} 
        for row in results
    ]
    
    return jsonify(chart_data)


@app.route('/get-attendance-data')
def get_attendance_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Correct table name: attendance
        cursor.execute("SELECT month, attendance_percentage FROM attendance_percentage")
        result = cursor.fetchall()

        # Close the connection
        connection.close()

        # Convert the result into a dictionary
        attendance_data = {row[0]: row[1] for row in result}

        # Return the data as a JSON response
        return jsonify(attendance_data)

    except Exception as e:
        return jsonify({"error": str(e)})

    
# Add cache control headers
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/get-working-format')
def get_working_format():
    try:
        # Establish the database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to fetch format and percentage from the working_format table
        cursor.execute("SELECT format, percentage FROM working_format")
        result = cursor.fetchall()
        print(result)

        # Close the connection
        connection.close()

        # Convert the result into a dictionary
        working_format_data = {row[0]: row[1] for row in result}
        print(working_format_data)

        # Return the data as JSON
        return jsonify(working_format_data)

    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/datas')
def getdata():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Query to fetch age, count, and gender
    query = """
        SELECT age, gender, COUNT(*) as count
        FROM employee
        GROUP BY age, gender
        ORDER BY age ASC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    # Structure data for Chart.js
    data = {}
    for row in results:
        age = row['age']
        gender = row['gender']
        count = row['count']
        if age not in data:
            data[age] = {"Male": 0, "Female": 0}
        data[age][gender] = count


    # Convert to JSON-friendly format
    chart_data = {
        "ages": list(data.keys()),
        "male_counts": [data[age]["Male"] for age in data],
        "female_counts": [data[age]["Female"] for age in data],
    }

    cursor.close()
    connection.close()
    print(chart_data)

    return jsonify(chart_data)


@app.route('/dat')
def fetch_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
   
    query = """
    SELECT 
        CASE
            WHEN location LIKE '%North%' THEN 'North Chennai'
            WHEN location LIKE '%South%' THEN 'South Chennai'
            WHEN location LIKE '%East%' THEN 'East Chennai'
            WHEN location LIKE '%West%' THEN 'West Chennai'
            ELSE 'Other'
        END AS grouped_location,
        SUM(male_count) AS total_male_count,
        SUM(female_count) AS total_female_count,
        SUM(other_count) AS total_other_count
    FROM emp_locations
    GROUP BY grouped_location
    ORDER BY FIELD(grouped_location, 'North Chennai', 'South Chennai', 'East Chennai', 'West Chennai', 'Other');
    """
    
    
    cursor.execute(query)
    data = cursor.fetchall()
    
    
    cursor.close()
    connection.close()
    
    
    locations = [row['grouped_location'] for row in data]
    male_counts = [row['total_male_count'] for row in data]
    female_counts = [row['total_female_count'] for row in data]
    other_counts = [row['total_other_count'] for row in data]
    
    return jsonify({
        "locations": locations,
        "male_counts": male_counts,
        "female_counts": female_counts,
        "other_counts": other_counts
    })


@app.route('/attendance')
def attendance():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch the last 10 employees who logged in
    query_last_logged_in = """
        SELECT emp_id, name, domain, login_time, timing
        FROM attendance
        ORDER BY login_time DESC
        LIMIT 10;
    """
    cursor.execute(query_last_logged_in)
    last_logged_in = cursor.fetchall()

    # Fetch the total present employees for today
    query_present_count = """
        SELECT COUNT(*) as present
        FROM attendance
        WHERE DATE(login_time) = CURDATE();
    """
    cursor.execute(query_present_count)
    present_count = cursor.fetchone()['present']

    # Fetch the total employees
    query_total_count = "SELECT COUNT(*) as total FROM employee;"
    cursor.execute(query_total_count)
    total_count = cursor.fetchone()['total']

    cursor.close()
    connection.close()

    # Render all data to the attendance.html page
    return render_template(
        'attendance.html',
        last_logged_in=last_logged_in,
        present_count=present_count,
        total_count=total_count
    )
@app.route('/today-attendance', methods=['GET'])
def get_today_attendance():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Query to count today's attendance
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE DATE(login_time) = CURDATE()")
        logged_in = cursor.fetchone()[0]

        # Query to count the total number of employees
        cursor.execute("SELECT COUNT(*) FROM employee")
        total_employees = cursor.fetchone()[0]
    finally:
        # Ensure proper cleanup
        cursor.close()
        connection.close()

    # Return JSON response with both logged-in and total employees
    return jsonify({
        'loggedIn': logged_in,
        'totalEmployees': total_employees
    })

# -------------------- Other Sections --------------------


# Functions for fetching data
def get_employees(page, domain):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    offset = (page - 1) * 10
    if domain == "all":
        query = "SELECT * FROM employee LIMIT 10 OFFSET %s"
        cursor.execute(query, (offset,))
    else:
        query = "SELECT * FROM employee WHERE department = %s LIMIT 10 OFFSET %s"
        cursor.execute(query, (domain, offset))
    employees = cursor.fetchall()
    conn.close()
    return employees

def get_domains():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT department FROM employee")
    domains = [row[0] for row in cursor.fetchall()]
    conn.close()
    return domains

def get_leave_requests():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM leave_requests WHERE status = 'Pending'")
    leave_requests = cursor.fetchall()
    conn.close()
    return leave_requests

def get_permission_requests():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM permission_requests WHERE status = 'Pending'")
    permission_requests = cursor.fetchall()
    conn.close()
    return permission_requests

def get_request_details(req_type, emp_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if req_type == "leave":
        cursor.execute("SELECT * FROM leave_requests WHERE employee_id = %s", (emp_id,))
    elif req_type == "permission":
        cursor.execute("SELECT * FROM permission_requests WHERE employee_id = %s", (emp_id,))
    details = cursor.fetchone()
    conn.close()

    if details:
        # Convert any timedelta fields to serializable format
        for key, value in details.items():
            details[key] = convert_timedelta_to_str(value)

    return details

# Update request status
def update_request_status(req_type, emp_id, action):
    conn = get_db_connection()
    cursor = conn.cursor()
    status = "Accepted" if action == "accept" else "Declined"
    if req_type == "leave":
        cursor.execute("UPDATE leave_requests SET status = %s WHERE employee_id = %s", (status, emp_id))
    elif req_type == "permission":
        cursor.execute("UPDATE permission_requests SET status = %s WHERE employee_id = %s", (status, emp_id))
    conn.commit()
    conn.close()


@app.route("/register")
def register():
    """Render the employee registration form."""
    return render_template("emp_register.html")


@app.route("/submit", methods=["POST"])
def submit_registration():
    """Handle employee registration form submission."""
    try:
        # Fetch form data
        form_data = {
            "first_name": request.form["firstName"],
            "middle_name": request.form.get("middleName", ""),  # Optional
            "last_name": request.form["lastName"],
            "dob": request.form["dob"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            "mobile": request.form["mobile"],
            "email": request.form["email"],
            "emergency_contact": request.form.get("emergencyContact", ""),  # Optional
            "area": request.form["area"],
            "street": request.form["street"],
            "city": request.form["city"],
            "district": request.form["district"],
            "state": request.form["state"],
            "country": request.form["country"],
            "pincode": request.form["pincode"],
            "permanent_address": request.form["permanentAddress"],
            "employee_id": request.form["employeeId"],
            "designation": request.form["designation"],
            "department": request.form["department"],
            "status": request.form["status"],
            "working_format": request.form["working_format"],
            "account_number": request.form["accountNumber"],
            "bank_name": request.form["bankName"],
            "ifsc_code": request.form["ifscCode"],
            "pan_number": request.form["panNumber"],
        }

        # Establish a database connection
        conn = get_db_connection()
        if conn is None:
            flash('Failed to connect to the database. Please try again later.', 'danger')
            return redirect(url_for('register'))

        cursor = conn.cursor()

        # SQL query for inserting data
        query = """
            INSERT INTO employees (
                first_name, middle_name, last_name, dob, age, gender, mobile, email, emergency_contact,
                area, street, city, district, state, country, pincode, permanent_address, employee_id,
                designation, department, status, working_format, account_number, bank_name, ifsc_code, pan_number
            )
            VALUES (%(first_name)s, %(middle_name)s, %(last_name)s, %(dob)s, %(age)s, %(gender)s, %(mobile)s,
                    %(email)s, %(emergency_contact)s, %(area)s, %(street)s, %(city)s, %(district)s,
                    %(state)s, %(country)s, %(pincode)s, %(permanent_address)s, %(employee_id)s,
                    %(designation)s, %(department)s, %(status)s, %(working_format)s, %(account_number)s, %(bank_name)s, %(ifsc_code)s,
                    %(pan_number)s)
        """

        cursor.execute(query, form_data)
        conn.commit()
        flash("Employee registration successful!", "success")

    except mysql.connector.Error as e:
        flash(f"Database error: {e}", "danger")
        print(f"Database error: {e}")

    except Exception as e:
        flash(f"Unexpected error: {e}", "danger")
        print(f"Unexpected error: {e}")

    finally:
        if "cursor" in locals() and cursor:
            cursor.close()
        if "conn" in locals() and conn:
            conn.close()

    # Redirect to the registration page with a flash message
    return redirect(url_for('register'))

@app.route('/leave')
def leave_form():
    return render_template('req_leave.html')


# Route for handling form submission
@app.route('/submit-leave', methods=['POST'])
def submit_leave():
    if request.method == 'POST':
        # Get form data
        employee_name = request.form['employee_name']
        department = request.form['department']
        designation = request.form['designation']
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']
        print(employee_name)

        # Database operation
        conn = get_db_connection()
        if conn is None:
            flash('Failed to connect to the database. Please try again later.')
            return redirect(url_for('leave_form'))

        try:
            cursor = conn.cursor()

            # Insert data into the SQL table
            query = """
            INSERT INTO leave_applications (employee_name, department, designation, leave_type, start_date, end_date, reason)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (employee_name, department, designation, leave_type, start_date, end_date, reason)
            cursor.execute(query, values)
            conn.commit()

            flash('Leave application submitted successfully!')
        except mysql.connector.Error as err:
            print(f"SQL error: {err}")
            flash('An error occurred while submitting your application. Please try again.')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('leave_form'))
    

@app.route('/permission')
def permission_form():
    return render_template('req_permission.html')  # Ensure 'index.html' matches your HTML file name


@app.route('/submit-permission', methods=['POST'])
def submit_permision():
    # Get form data
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    employee_id = request.form['employeeID']
    department = request.form['department']
    absence_types = ', '.join(request.form.getlist('absenceType'))
    reason = request.form['reason']
    absence_from = request.form['absenceFrom']
    absence_to = request.form['absenceTo']
    total_hours = request.form['totalHours']

    # Store data in MySQL
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO permission (first_name, last_name, employee_id, department, absence_types, reason, absence_from, absence_to, total_hours)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, employee_id, department, absence_types, reason, absence_from, absence_to, total_hours))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/permission')  # Redirect to the form after submission
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/emp-list')
def emp_list():
    page = int(request.args.get('page', 1))
    domain = request.args.get('domain', 'all')
    employees = get_employees(page, domain)
    domains = get_domains()
    leave_requests = get_leave_requests()
    permission_requests = get_permission_requests()


    return render_template(
        "emp_list.html",
        employees=employees,
        domains=domains,
        page=page,
        leave_requests=leave_requests,
        permission_requests=permission_requests,
    )

@app.route('/get-request-details', methods=['GET'])
def get_request_details_endpoint():
    req_type = request.args.get("type")
    emp_id = request.args.get("emp_id")
    details = get_request_details(req_type, emp_id)
    if details:
        return jsonify(success=True, details=details)
    return jsonify(success=False)

@app.route('/update-request', methods=['POST'])
def update_request_endpoint():
    data = request.json
    req_type = data["type"]
    emp_id = data["emp_id"]
    action = data["action"]
    update_request_status(req_type, emp_id, action)
    return jsonify(success=True)





# -------------------- Employee Details --------------------

@app.route('/employee/<int:employee_id>', methods=['GET', 'POST'])
def employee_details(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Collect updated data
        updated_data = {
            'name': request.form['name'],
            'dob': request.form['dob'],
            'gender': request.form['gender'],
            'mobile': request.form['mobile'],
            'email': request.form['email'],
            'emergency_contact': request.form['emergency_contact'],
            'current_address': request.form['current_address'],
            'permanent_address': request.form['permanent_address'],
            'designation': request.form['designation'],
            'department': request.form['department'],
            'account_number': request.form['account_number'],
            'bank_name': request.form['bank_name'],
            'ifsc_code': request.form['ifsc_code'],
            'pan_number': request.form['pan_number']
        }

        # Update query
        query = """
            UPDATE employee SET 
            emp_name = %(name)s, dob = %(dob)s, gender = %(gender)s, 
            mobile = %(mobile)s, email = %(email)s, emergency_contact = %(emergency_contact)s, 
            current_address = %(current_address)s, permanent_address = %(permanent_address)s, 
            designation = %(designation)s, department = %(department)s, 
            account_number = %(account_number)s, bank_name = %(bank_name)s, 
            ifsc_code = %(ifsc_code)s, pan_number = %(pan_number)s 
            WHERE employee_id = %(employee_id)s
        """
        updated_data['employee_id'] = employee_id
        cursor.execute(query, updated_data)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(f'/employee/{employee_id}')

    # Fetch employee details
    cursor.execute("SELECT * FROM employee WHERE employee_id = %s", (employee_id,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('emp_details.html', employee=employee)


@app.route('/schedule')
def schedule_meet():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch upcoming meetings
        cursor.execute( """
        SELECT id, name, DATE_FORMAT(date, '%Y-%m-%d') as date, 
               DATE_FORMAT(start_time, '%H:%i') as start_time, 
               DATE_FORMAT(end_time, '%H:%i') as end_time, 
               location, meet_url 
        FROM meetings
        WHERE date >= CURDATE()
        ORDER BY date, start_time
        LIMIT 6;
        """)
        upcoming_meetings = cursor.fetchall()

        # Convert datetime and timedelta objects to strings
        for meeting in upcoming_meetings:
            # Format the date
            if isinstance(meeting['date'], datetime):
                meeting['date'] = meeting['date'].strftime('%Y-%m-%d')  # Format date as string
            
            # Convert timedelta to HH:MM:SS format
            if isinstance(meeting['start_time'], timedelta):
                start_time_seconds = meeting['start_time'].total_seconds()
                hours = int(start_time_seconds // 3600)
                minutes = int((start_time_seconds % 3600) // 60)
                seconds = int(start_time_seconds % 60)
                meeting['start_time'] = f"{hours:02}:{minutes:02}:{seconds:02}"

            if isinstance(meeting['end_time'], timedelta):
                end_time_seconds = meeting['end_time'].total_seconds()
                hours = int(end_time_seconds // 3600)
                minutes = int((end_time_seconds % 3600) // 60)
                seconds = int(end_time_seconds % 60)
                meeting['end_time'] = f"{hours:02}:{minutes:02}:{seconds:02}"

        print("Upcoming Meetings:", upcoming_meetings)

        # Fetch feedbacks
        cursor.execute("""
            SELECT f.feedback, f.employee_name, m.name, m.date 
            FROM feedbacks f 
            JOIN meetings m ON f.meeting_id = m.id 
            ORDER BY m.date DESC
        """)
        feedbacks = cursor.fetchall()

        # Convert datetime objects in feedbacks (if any)
        for feedback in feedbacks:
            if isinstance(feedback['date'], datetime):
                feedback['date'] = feedback['date'].strftime('%Y-%m-%d')

        print("Feedbacks:", feedbacks)

        connection.close()

        # Pass the data to the template
        return render_template('meet.html', feedbacks=feedbacks)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Error loading page"
    

@app.route('/upcoming_meetings')
def upcoming_meetings():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, name, location, DATE_FORMAT(start_time, '%H:%i:%s') AS start_time,
               DATE_FORMAT(end_time, '%H:%i:%s') AS end_time, 
               DATE_FORMAT(date, '%Y-%m-%d') AS date, meet_url
        FROM meetings
        WHERE date >= CURDATE()
        ORDER BY date, start_time
        LIMIT 6
    """
    cursor.execute(query)
    meetings = cursor.fetchall()

    cursor.close()
    connection.close()
    return jsonify(meetings)

# Fetch meetings for a specific date
@app.route('/get_events_for_date', methods=['GET'])
def get_events_for_date():
    date = request.args.get('date')  

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM meetings WHERE date = %s"
    cursor.execute(query, (date,))
    
    events = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Prepare the event data for response
    event_list = []
    for event in events:
        event_list.append({
            'id': event['id'],
            'name': event['name'],
            'location': event['location'],
            'start_time': format_time(event['start_time']),
            'end_time': format_time(event['end_time']),
            'meet_url': event['meet_url']
        })
    
    return jsonify(event_list)


@app.route('/events')
def get_events():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch meeting data
    cursor.execute('SELECT * FROM meetings')
    meetings = cursor.fetchall()

    # Prepare the events for FullCalendar
    events = []
    for meeting in meetings:
        event = {
            'title': meeting['name'],
            'location': meeting['location'],
            'start': f"{meeting['date']}T{meeting['start_time']}",
            'end': f"{meeting['date']}T{meeting['end_time']}",
            'url': meeting['meet_url']
        }
        events.append(event)

    cursor.close()
    connection.close()

    return jsonify(events)
# Add Event
@app.route('/add_event', methods=['POST'])
def add_event():
    # Get event data from the request
    event_name = request.form['name']
    event_location = request.form['location']
    event_start_time = request.form['start_time']
    event_end_time = request.form['end_time']
    event_url = request.form['meet_url']
    event_date = request.form['date']  # Assuming the date is being sent

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "INSERT INTO meetings (name, location, date, start_time, end_time, meet_url) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (event_name, event_location, event_date, event_start_time, event_end_time, event_url)

    # Execute the query
    cursor.execute(query, values)
    connection.commit() 

    cursor.close()
    connection.close()
    return jsonify({"message": "Event added successfully!"})

# Delete Event
@app.route('/delete_event', methods=['DELETE'])
def delete_event():
    # Get the event ID from the query string
    event_id = request.args.get('id')
    if not event_id:
        return jsonify({'error': 'Event ID is missing'}), 400

    try:
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Delete the event from the database
        cursor.execute("DELETE FROM meetings WHERE id = %s", (event_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'success': True, 'message': 'Event deleted successfully!'})
        else:
            return jsonify({'error': 'Event not found'}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to delete event'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/data', methods=['GET'])
def get_chart_data():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Query to Count Statuses
    query = """
    SELECT status, COUNT(*) as count 
    FROM employee 
    GROUP BY status
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    
    # Map Status to Colors
    color_map = {
        'Intern': '#FF6B6B',
        'Permanent': '#4ECDC4',
        'Temporary': '#45B7D1'
    }

    # Format the Data for the Frontend
    chart_data = [
        {'label': row['status'], 'value': row['count'], 'color': color_map[row['status']]} 
        for row in results
    ]
    
    return jsonify(chart_data)

@app.route('/datas')
def get_data():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Query to fetch age, count, and gender
    query = """
        SELECT age, gender, COUNT(*) as count
        FROM employee
        GROUP BY age, gender
        ORDER BY age ASC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    # Structure data for Chart.js
    data = {}
    for row in results:
        age = row['age']
        gender = row['gender']
        count = row['count']
        if age not in data:
            data[age] = {"Male": 0, "Female": 0}
        data[age][gender] = count


    # Convert to JSON-friendly format
    chart_data = {
        "ages": list(data.keys()),
        "male_counts": [data[age]["Male"] for age in data],
        "female_counts": [data[age]["Female"] for age in data],
    }

    cursor.close()
    connection.close()
    print(chart_data)

    return jsonify(chart_data)

@app.route('/get-employee')
def get_employee():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT role, gender FROM rolewise ORDER BY role")
        result = cursor.fetchall()
        connection.close()

        employees_by_role = {}
        for role, gender in result:
            if role not in employees_by_role:
                employees_by_role[role] = {'male': 0, 'female': 0, 'total': 0}
            
            if gender == 'Male':
                employees_by_role[role]['male'] += 1
            elif gender == 'Female':
                employees_by_role[role]['female'] += 1
            
            employees_by_role[role]['total'] += 1

        for role, counts in employees_by_role.items():
            male_percentage = (counts['male'] / counts['total']) * 100 if counts['total'] > 0 else 0
            female_percentage = (counts['female'] / counts['total']) * 100 if counts['total'] > 0 else 0
            counts['male_percentage'] = round(male_percentage, 2)
            counts['female_percentage'] = round(female_percentage, 2)

        return jsonify(employees_by_role)

    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------- Main Runner --------------------
if __name__ == "__main__":
    app.run(debug=True)
