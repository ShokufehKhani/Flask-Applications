from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = '30eeffdf734677c4010d5e1f30308a69'  

# Load data from Excel files
students_df = pd.read_excel('data/students_data.xlsx')
teachers_df = pd.read_excel('data/teachers_data.xlsx')
courses_df = pd.read_excel('data/courses_data.xlsx')

# Ensure passwords are treated as strings
students_df['password'] = students_df['password'].astype(str)
teachers_df['password'] = teachers_df['password'].astype(str)

@app.route('/')
def index():
    return render_template('index.html')

# Student Login
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        password = str(password)
        students_df['email'] = students_df['email'].str.lower()
        
        student = students_df[(students_df['email'] == email) & (students_df['password'] == password)]

        if not student.empty:
            session['student_email'] = email
            return redirect(url_for('student_profile'))
        else:
            return "Login failed, please check your credentials"
    
    return render_template('student_login.html')

# Course Details
@app.route('/course_details/<int:course_id>')
def course_details(course_id):
    course = courses_df[courses_df['id'] == course_id]

    if course.empty:
        return "Course not found."

    course = course.iloc[0]  

    return render_template('course_details.html', course=course)



@app.route('/student_register_course', methods=['GET', 'POST'])
def student_register_course():
    if 'student_email' in session:
        student_index = students_df[students_df['email'] == session['student_email']].index[0]
        student = students_df.loc[student_index]

        if request.method == 'POST':
            course_id_str = request.form.get('id')  
            if not course_id_str:
                return "No course selected."

            try:
                course_id = int(course_id_str)
            except ValueError:
                return "Invalid course ID."

            if course_id not in courses_df['id'].values:
                return "Course does not exist."

            # Check course capacity
            course_index = courses_df[courses_df['id'] == course_id].index[0]
            if courses_df.at[course_index, 'capacity'] <= 0:
                return "Course is full, cannot register."

            # Dynamically add new course columns as needed
            course_columns = [col for col in students_df.columns if col.startswith('course')]
            next_course_column = f'course {len(course_columns) + 1}'

            # Add the new course column if it doesn't exist
            if next_course_column not in students_df.columns:
                students_df[next_course_column] = None

            # Register the course
            students_df.at[student_index, next_course_column] = course_id

            # Subtract 1 from the course capacity
            courses_df.at[course_index, 'capacity'] -= 1

            # Save the updated DataFrame back to Excel
            students_df.to_excel('data/students_data.xlsx', index=False)
            courses_df.to_excel('data/courses_data.xlsx', index=False)

            return redirect(url_for('student_courses'))  # Redirect to student_courses

        # Filter out courses the student is already registered for
        registered_courses_ids = [
            student[f'course {i}'] for i in range(1, len(students_df.columns) + 1) 
            if f'course {i}' in students_df.columns and not pd.isna(student[f'course {i}'])
        ]
        available_courses = courses_df[~courses_df['id'].isin(registered_courses_ids)]

        return render_template('student_register_course.html', student=student, courses=available_courses)
    else:
        return redirect(url_for('student_login'))


# Teacher Profile
@app.route('/teacher_profile')
def teacher_profile():
    if 'teacher_email' in session:
        teacher = teachers_df[teachers_df['email'] == session['teacher_email']].iloc[0]
        return render_template('teacher_profile.html', teacher=teacher)
    else:
        return redirect(url_for('teacher_login'))

# View and Manage Courses as a Teacher
@app.route('/teacher_courses', methods=['GET', 'POST'])
def teacher_courses():
    if 'teacher_email' in session:
        teacher = teachers_df[teachers_df['email'] == session['teacher_email']].iloc[0]
        teacher_courses = courses_df[courses_df['teacher'] == teacher['name']]
        return render_template('teacher_courses.html', courses=teacher_courses)
    else:
        return redirect(url_for('teacher_login'))
    
@app.template_filter('limit_words')
def limit_words(text, num_words=1000):
    words = text.split()
    return ' '.join(words[:num_words]) + ('...' if len(words) > num_words else '')



# Add a New Course as a Teacher
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    global courses_df  
    if 'teacher_email' in session:
        if request.method == 'POST':
            course_id = request.form['id']  
            name = request.form['name']
            major = request.form['major']
            description = request.form['description']
            time = request.form['time']
            capacity = int(request.form['capacity'])
            teacher = teachers_df[teachers_df['email'] == session['teacher_email']].iloc[0]['name']

            # Ensure that the course ID is used correctly
            new_course = pd.DataFrame([[course_id, name, major, teacher, description, time, capacity, ""]],
                                      columns=courses_df.columns)
            courses_df = pd.concat([courses_df, new_course], ignore_index=True)
            courses_df.to_excel('data/courses_data.xlsx', index=False)  

            return redirect(url_for('teacher_courses'))
        return render_template('add_course.html')
    else:
        return redirect(url_for('teacher_login'))

# Personal Info Page
@app.route('/personal_info')
def personal_info():
    if 'student_email' in session:
        student = students_df[students_df['email'] == session['student_email']].iloc[0]
        return render_template('personal_info.html', student=student)
    else:
        return redirect(url_for('student_login'))

# Student Profile
@app.route('/student_profile')
def student_profile():
    if 'student_email' in session:
        student = students_df[students_df['email'] == session['student_email']].iloc[0]
        return render_template('student_profile.html', student=student)
    else:
        return redirect(url_for('student_login'))

# Teacher Login
@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # Convert to string 
        password = str(password)

        # Fetch the teacher based on the email and password
        teacher = teachers_df[(teachers_df['email'] == email) & (teachers_df['password'] == password)]

        if not teacher.empty:
            session['teacher_email'] = email
            return redirect(url_for('teacher_profile'))
        else:
            return "Login failed, please check your credentials"

    return render_template('teacher_login.html')


# View Courses
@app.route('/student_courses')
def student_courses():
    if 'student_email' in session:
        student = students_df[students_df['email'] == session['student_email']].iloc[0]

        course_columns = [col for col in students_df.columns if col.startswith('course')]
        registered_course_ids = [student[col] for col in course_columns if not pd.isna(student[col])]
        
        # Ensure registered_courses is a DataFrame
        registered_courses = courses_df[courses_df['id'].isin(registered_course_ids)]

        return render_template('student_courses.html', courses=registered_courses)
    else:
        return redirect(url_for('student_login'))

    
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('student_email', None)  
    return redirect(url_for('index'))  

    
    
@app.route('/update_personal_info', methods=['GET', 'POST'])
def update_personal_info():
    if 'student_email' in session:
        email = session['student_email']
        
        if request.method == 'POST':
            # Get form data
            new_name = request.form.get('name')
            new_password = request.form.get('password')
            new_phone = request.form.get('phone')
            new_email = request.form.get('email')

            # Update student information in DataFrame
            student_index = students_df[students_df['email'] == email].index[0]
            if new_name:
                students_df.at[student_index, 'name'] = new_name
            if new_password:
                students_df.at[student_index, 'password'] = new_password
            if new_phone:
                students_df.at[student_index, 'phone'] = new_phone

            # Save changes to Excel file
            students_df.to_excel('data/students_data.xlsx', index=False)

            return redirect(url_for('personal_info'))
        
        # For GET request, render the form with empty values
        return render_template('update_personal_info.html', student={})
    else:
        return redirect(url_for('student_login'))

    
if __name__ == '__main__':
    app.run(debug=True)