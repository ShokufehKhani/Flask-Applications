
# **Student Portal Web Application**

This is a basic student portal web application built using Flask. The application allows students to view their profile, see a list of courses, and view details about each course. Teachers can add new courses and manage student enrollments.

## **Features**

-  **Home Page**: The home page (`/`) displays navigation links to "Home", "Profile", and "Courses."
-  **Profile Page**: Students can view their profile (`/profile`), including personal details (name, email, major), which are dynamically passed from the server.
- **Courses Page**: A page (`/courses`) that lists all available courses with their names, descriptions, and the teacher's name.
- **Course Details Page**: A dynamic page (`/courses/<course_id>`) that displays detailed information about a specific course based on the course_id.
- **Add Courses (Teacher Role)**: Teachers can add new courses through a form on the `/add_course` page.
- **Forms and Data Handling**: Students can update their personal details via a form on the profile page.

## **File Structure**
  ``bash
  /student-portal
      /static
          /css
              personal_info.css  # Styles for the pages
      /templates
          index.html           # Home page
          profile.html         # Profile page
          courses.html         # List of courses page
          course_detail.html   # Individual course details page
      app.py                    # Main Flask app logic


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


2. **Run the Flask application**:
  ```bash
  python app.py

3. Open your browser and go to http://localhost:5000 to view the app.






