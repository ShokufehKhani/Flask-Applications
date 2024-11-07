
# **Student Portal Web Application**

This is a basic student portal web application built using Flask. The application allows students to view their profile, see a list of courses, and view details about each course. Teachers can add new courses and manage student enrollments.

## **Features**

-  **Student Login**: Students can log in with their email and password to view their profile and courses.
- **Personal Info Page**: Students can update their personal information.
-  **Course Registration**: Students can register for courses, with dynamic course columns created for each student.
- **Forms and Data Handling**: Students can update their personal details via a form on the profile page.
- **Student Course Page**: Students can view the courses they are registered for.
- **Teacher Login**: Teachers can log in with their email and password to manage their courses and view their profile.
- **Teacher Profile**: Teachers can log in to manage their courses.
- **Teacher Course Management**: Teachers can view and manage the courses they are teaching.


## **File Structure**
  ``bash
  /student_portal
    /data
        students_data.xlsx
        teachers_data.xlsx
        courses_data.xlsx
    /templates
        index.html
        student_login.html
        course_details.html
        student_register_course.html
        teacher_profile.html
        teacher_courses.html
        add_course.html
        personal_info.html
        student_profile.html
        teacher_login.html
        update_personal_info.html
    /static
        /css
            style.css
    app.py
    requirements.txt
    README.md


## **Setup Instructions**

### **Prerequisites**

1. **Python 3.x** with the following packages:
   - Python 3.8+
   - Flask
   - Jinja2
   - numpy
   - pandas
You can install the required packages using:

  ``bash
  pip install -r requirements.txt

### **Running the application**

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:ShokufehKhani/Flask-Applications.git
  cd student-portal

3. **Prepare Data:** Place your `students_data.xlsx`, `teachers_data.xlsx`, and `courses_data.xlsx` files in the `data/` folder of your project directory.

2. **Run the Flask application**:
  ```bash
  python app.py

3. Open your browser and go to http://localhost:5000 to view the app.






