# Student Management System - Main Flask Application

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
from config import Config
import os
from werkzeug.utils import secure_filename

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)
UPLOAD_FOLDER = 'static/uploads/cnic'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure session is properly configured
app.secret_key = app.config['SECRET_KEY']

app.config['PERMANENT_SESSION_LIFETIME'] = 3600  
app.config['SESSION_TYPE'] = 'filesystem'

def get_db_connection():
    """Establish database connection with error handling"""
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT']
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        flash(f"Database connection failed: {e}", 'error')
        return None

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """Execute database queries with proper error handling"""
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        if connection is None:
            return None
            
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if commit:
            connection.commit()
            return cursor.lastrowid if cursor.lastrowid else True
            
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            return True
            
    except Error as e:
        print(f"Query execution error: {e}")
        flash(f"Database error: {e}", 'error')
        if connection:
            connection.rollback()
        return None
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Routes
@app.route('/')
def index():
    """Display all students"""
    try:
        query = "SELECT * FROM students ORDER BY created_at DESC"
        students = execute_query(query, fetch_all=True)
        
        if students is None:
            students = []
            
        return render_template('index.html', students=students)
    except Exception as e:
        print(f"Index route error: {e}")
        flash(f"Error loading students: {e}", 'error')
        return render_template('index.html', students=[])
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            roll_number = request.form.get('roll_number', '').strip().upper()
            subject = request.form.get('subject', '').strip()

            cnic_front_path = None
            cnic_back_path = None

            # Upload CNIC front
            if 'cnic_front' in request.files:
                front_file = request.files['cnic_front']
                if front_file and allowed_file(front_file.filename):
                    front_filename = secure_filename(f"{roll_number}_front_{front_file.filename}")
                    front_file.save(os.path.join(app.config['UPLOAD_FOLDER'], front_filename))
                    cnic_front_path = f"uploads/cnic/{front_filename}"

            # Upload CNIC back
            if 'cnic_back' in request.files:
                back_file = request.files['cnic_back']
                if back_file and allowed_file(back_file.filename):
                    back_filename = secure_filename(f"{roll_number}_back_{back_file.filename}")
                    back_file.save(os.path.join(app.config['UPLOAD_FOLDER'], back_filename))
                    cnic_back_path = f"uploads/cnic/{back_filename}"

            if not name or not roll_number or not subject:
                flash('All fields are required!', 'error')
                return render_template('add_student.html')

            # Check duplicate roll number
            check_query = "SELECT id FROM students WHERE roll_number = %s"
            existing_student = execute_query(check_query, (roll_number,), fetch_one=True)

            if existing_student:
                flash(f'Roll number "{roll_number}" already exists!', 'error')
                return render_template('add_student.html')

            # Insert data
            insert_query = """
                INSERT INTO students (name, roll_number, subject, cnic_front, cnic_back) 
                VALUES (%s, %s, %s, %s, %s)
            """

            result = execute_query(
                insert_query,
                (name, roll_number, subject, cnic_front_path, cnic_back_path),
                commit=True
            )

            if result:
                flash(f'Student "{name}" added successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Failed to add student.', 'error')

        except Exception as e:
            print(f"Add student error: {e}")
            flash(f'Error: {e}', 'error')

    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """Edit an existing student"""
    try:
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name', '').strip()
            roll_number = request.form.get('roll_number', '').strip().upper()
            subject = request.form.get('subject', '').strip()
            
            # Validate form data
            if not name or not roll_number or not subject:
                flash('All fields are required!', 'error')
                return redirect(url_for('edit_student', id=id))
            
            # Check if roll number already exists (excluding current student)
            check_query = "SELECT id FROM students WHERE roll_number = %s AND id != %s"
            existing_student = execute_query(check_query, (roll_number, id), fetch_one=True)
            
            if existing_student:
                flash(f'Roll number "{roll_number}" already exists!', 'error')
                return redirect(url_for('edit_student', id=id))
            
            # Update student
            update_query = """
                UPDATE students 
                SET name = %s, roll_number = %s, subject = %s 
                WHERE id = %s
            """
            result = execute_query(update_query, (name, roll_number, subject, id), commit=True)
            
            if result:
                flash(f'Student "{name}" updated successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Failed to update student. Please try again.', 'error')
        
        # GET request - fetch student data
        query = "SELECT * FROM students WHERE id = %s"
        student = execute_query(query, (id,), fetch_one=True)
        
        if student is None:
            flash('Student not found!', 'error')
            return redirect(url_for('index'))
            
        return render_template('edit_student.html', student=student)
        
    except Exception as e:
        print(f"Edit student error: {e}")
        flash(f'Error editing student: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_student(id):
    """Delete a student"""
    try:
        # Validate ID
        if not id or id <= 0:
            flash('Invalid student ID!', 'error')
            return redirect(url_for('index'))
        
        # Get student info for confirmation message
        get_query = "SELECT name, roll_number FROM students WHERE id = %s"
        student = execute_query(get_query, (id,), fetch_one=True)
        
        if student is None:
            flash('Student not found!', 'error')
            return redirect(url_for('index'))
        
        # Delete student
        delete_query = "DELETE FROM students WHERE id = %s"
        result = execute_query(delete_query, (id,), commit=True)
        
        if result:
            flash(f'Student "{student["name"]}" deleted successfully!', 'success')
        else:
            flash('Failed to delete student. Please try again.', 'error')
            
    except Exception as e:
        print(f"Delete student error: {e}")
        flash(f'Error deleting student: {e}', 'error')
    
    # Ensure we have a proper redirect
    try:
        return redirect(url_for('index'))
    except Exception as redirect_error:
        print(f"Redirect error: {redirect_error}")
        # Fallback redirect if url_for fails
        return redirect('/')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    flash('Page not found!', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    flash('Internal server error!', 'error')
    return redirect(url_for('index'))

# Test database connection route
@app.route('/test-db')
def test_db_connection():
    """Test database connection (for debugging)"""
    try:
        connection = get_db_connection()
        if connection:
            connection.close()
            return "Database connection successful!"
        else:
            return "Database connection failed!"
    except Exception as e:
        return f"Database test error: {e}"

# Create tables if they don't exist
def create_tables():
    """Create database tables if they don't exist"""
    try:
        # First, create database if it doesn't exist
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DB']}"
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            port=app.config['MYSQL_PORT']
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(create_db_query)
        connection.close()
        
        # Now create the students table
        create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                roll_number VARCHAR(50) NOT NULL UNIQUE,
                subject VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        result = execute_query(create_table_query, commit=True)
        
        if result:
            print("Tables created successfully!")
        else:
            print("Failed to create tables!")
            
    except Exception as e:
        print(f"Error creating tables: {e}")

# Main execution
if __name__ == '__main__':
    # Create tables on startup
    create_tables()
    
    # Run the Flask application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
