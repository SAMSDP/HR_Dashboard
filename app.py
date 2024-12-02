from flask import Flask, render_template, request, redirect, jsonify
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
@app.route('/attendance')
def attendance():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch the last 10 employees who logged in
    query_last_logged_in = """
        SELECT emp_id, name, domain, login_time
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
        permission_requests=permission_requests
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

# -------------------- Main Runner --------------------
if __name__ == "__main__":
    app.run(debug=True)
