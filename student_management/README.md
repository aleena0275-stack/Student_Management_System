# Student Management System

A complete web-based Student Management System built with Flask, MySQL, and Bootstrap 5.

## Features

- **View All Students**: Display all students in a responsive table with pagination
- **Add Student**: Add new students with validation
- **Edit Student**: Update existing student information
- **Delete Student**: Remove students with confirmation dialogs
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Real-time Statistics**: View total students, subjects, and system status
- **Error Handling**: Comprehensive error handling and user-friendly messages
- **Database Validation**: Prevents duplicate roll numbers and ensures data integrity

## Tech Stack

- **Backend**: Python 3 + Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: MySQL (via XAMPP)
- **ORM**: mysql-connector-python
- **Tools**: XAMPP (Apache + MySQL), pip

## Prerequisites

1. **Python 3.7+** installed on your system
2. **XAMPP** installed with MySQL running on localhost:3306
3. **pip** (Python package manager)

## Installation & Setup

### 1. Clone/Download the Project

```bash
# Navigate to your project directory
cd "e:\school management system\student_management"
```

### 2. Set Up the Database

#### Option A: Using phpMyAdmin (Recommended)
1. Start XAMPP and start Apache and MySQL services
2. Open phpMyAdmin (http://localhost/phpmyadmin)
3. Click on "Import" tab
4. Choose the `database.sql` file from the project directory
5. Click "Go" to execute the SQL script

#### Option B: Manual Setup
1. Open phpMyAdmin
2. Create a new database named `student_db`
3. Execute the following SQL:

```sql
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(50) NOT NULL UNIQUE,
    subject VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Start the Flask application
python app.py
```

The application will be available at: **http://localhost:5000**

## Project Structure

```
student_management/
├── app.py                 # Main Flask application
├── config.py              # Database configuration
├── requirements.txt       # Python dependencies
├── database.sql          # Database setup script
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Homepage - view all students
│   ├── add_student.html  # Add student form
│   └── edit_student.html # Edit student form
└── static/               # Static files
    └── css/
        └── style.css     # Custom CSS styles
```

## Usage

### 1. View Students
- Visit the homepage to see all students
- Statistics cards show total students, subjects, and system status

### 2. Add Student
- Click "Add New Student" button
- Fill in the form with student details
- Roll number must be unique
- Click "Add Student" to save

### 3. Edit Student
- Click the edit icon (pencil) next to any student
- Modify the required fields
- Click "Update Student" to save changes

### 4. Delete Student
- Click the delete icon (trash) next to any student
- Confirm the deletion in the modal dialog
- Click "Delete" to remove the student permanently

## Database Configuration

The database configuration is in `config.py`:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'student_db'
MYSQL_PORT = 3306
MYSQL_CURSORCLASS = 'DictCursor'
```

### To Change Database Settings:
1. Open `config.py`
2. Modify the values as needed
3. Restart the application

## Features in Detail

### Validation
- All form fields are required
- Roll numbers must be unique
- Roll numbers contain only letters and numbers
- Student names limited to 100 characters

### Error Handling
- Database connection errors
- Duplicate roll number detection
- Form validation with user-friendly messages
- 404 and 500 error handling

### Security
- SQL injection prevention using parameterized queries
- Input validation and sanitization
- Secure session management

### Responsive Design
- Mobile-friendly interface
- Bootstrap 5 responsive grid system
- Touch-friendly buttons and forms

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure XAMPP MySQL service is running
   - Check database credentials in `config.py`
   - Verify database `student_db` exists

2. **Import Error**
   - Install requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Port 5000 Already in Use**
   - Stop other applications using port 5000
   - Or modify the port in `app.py`:

```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

4. **Permission Issues**
   - Run command prompt as administrator
   - Check file permissions

### Debug Mode
The application runs in debug mode by default. To disable:

```python
# In config.py
DEBUG = False
```

## API Endpoints

- `GET /` - View all students
- `GET /add` - Show add student form
- `POST /add` - Process add student form
- `GET /edit/<id>` - Show edit student form
- `POST /edit/<id>` - Process edit student form
- `GET /delete/<id>` - Delete a student
- `GET /test-db` - Test database connection (debugging)

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify your setup matches the requirements
3. Check the console for error messages
4. Ensure XAMPP services are running

---

**Happy Coding! 🎓**
