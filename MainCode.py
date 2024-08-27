#                                  BEP09 BOOTCAMP MANAGEMENT SYSTEM
# 0. NITIALIZATION OF DATA STORAGE AND IMPORTING USEFUL MODULES
# 1. EMAIL, DOB VALIDATION AND UNIQUE ID GENERATOR 
# 2. STUDENT REGISTRATION FUNCTION
# 3. DATA ENCRYPTION FUNCTION
# 4. FEE VALIDATION FUNCTION
# 5. COURSE ENROLLMENT FUNCTION
# 6. VIEW STUDENT INFORMATION FUNCTION
# 7. SCORING STUDENTS COURSES FUNCTION
# 8. VIEWING SCORED RESULTS FUNCTION
# 9. GENERATE STUDENT PROGRESS REPORT
# 10. MAIN MENU FUNCTION

#-----------------------------------------------------------------------------------------------------------------------------------------------------

#INITIALIZATION OF DATA STORAGE AND IMPORTING USEFUL MODULES

roles = ["Administrator", "Instructor", "Student", "Parent"]

# Initialize lists to store student, course, and result information
students = []  
courses = []   
results = {}

# Display available courses and prompt for selection
available_courses = ["Python Basics", "Data Science", "Web Development", "Machine Learning"]

import re  # Import the regular expressions module
import uuid  # Import the uuid module to generate unique identifiers
from datetime import datetime

#----------------------------------------------------------------------------------------------------------------------------------------------------

# EMAIL, DOB VALIDATION AND UNIQUE ID GENERATOR

# Define a function to validate email format using regex
def is_valid_email(email):
    try:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, email) is not None:
            return True
        else:
            print("Invalid email format.")
            return False
    except Exception as e:
        print(f"An error occurred during email validation: {str(e)}")
        return False
    

# Use Python's datetime module to validate the DOB
def is_valid_date_of_birth(dob):
    try:
        # Attempt to parse the date string to a datetime object
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        
        # Check if the date is in the future
        if birth_date > datetime.now():
            print("Invalid date of birth: Date cannot be in the future.")
            return False
        
        # Check if the date is too far in the past (e.g., more than 120 years ago)
        if birth_date < datetime.now().replace(year=datetime.now().year - 120):
            print("Invalid date of birth: Date is too far in the past.")
            return False
        
        return True
    except ValueError:
        print("Invalid date format: Please enter the date in the format YYYY-MM-DD.")
        return False


# Generate a UUID (Unique random numbers) and Concatenate with student last name
def generate_student_id(last_name):
    unique_id = str(uuid.uuid4())[:4]  # Generate a UUID and take the first 8 characters
    student_id = f"{last_name}-{unique_id}"  # Concatenate last name with unique ID
    return student_id

#----------------------------------------------------------------------------------------------------------------------------------------------------
# STUDENT REGISTRATION FUNCTION

# Define the student registration function
def register_student():
    try:
        role = "Student"
        first_name = input("Enter your first name: ").strip().title()
        last_name = input("Enter your last name: ").strip().title()
        email = input("Enter your email address: ").strip().lower()
        date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ").strip()

        if not first_name or not last_name or not email or not date_of_birth:
            print("Registration failed: Missing required information")
            return
        
        if not is_valid_email(email):
            print("Registration failed: Invalid email format")
            return

        if not is_valid_date_of_birth(date_of_birth):
            print("Registration failed: Invalid date of birth.")
            return

        print("\nAvailable Courses:")
        for i, course in enumerate(available_courses, 1):
            print(f"{i}. {course}")

        selected_courses = input("\nEnter the courses you want to enroll in, separated by commas: ").strip().split(",")
        selected_courses = [course.strip().title() for course in selected_courses]  # Normalize course names

        student_id = generate_student_id(last_name)
        
        for course in selected_courses:
            if course not in available_courses:
                print(f"Registration failed: {course} is not a valid course")
                return

        student = {
            "studentID": student_id,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "dateOfBirth": date_of_birth,
            "selectedCourses": selected_courses,
            "feesPaid": False
        }

        encrypted_student = encrypt_data(student)
        students.append(encrypted_student)

        print(f"\nRegistration successful. Student ID: {student_id}")

    except Exception as e:
        print(f"An error occurred during registration: {str(e)}")

#-----------------------------------------------------------------------------------------------------------------------------------------------------

# DATA ENCRYPTION FUNCTION

from cryptography.fernet import Fernet

# Generate and store the encryption key (do this only once, and store the key securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Save the key securely in a file (you should ideally store this key securely)
with open("secret.key", "wb") as key_file:
    key_file.write(key)

# Load the key from a file (whenever you need to use the key)
def load_key():
    return open("secret.key", "rb").read()

# Encrypt the student data as bytes using Fernet symmetric encryption
def encrypt_data(data):
    try:
        data_str = str(data).encode('utf-8')
        encrypted_data = cipher_suite.encrypt(data_str)
        return encrypted_data
    except Exception as e:
        print(f"An error occurred during encryption: {str(e)}")
        return None

def decrypt_data(encrypted_data):
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        data_str = decrypted_data.decode('utf-8')
        data_dict = eval(data_str)
        return data_dict
    except Exception as e:
        print(f"An error occurred during decryption: {str(e)}")
        return None

#-----------------------------------------------------------------------------------------------------------------------------------------------------
# FEE VALIDATION FUNCTION

# Define the fee validation function. Only students who have paid can be enrolled for courses.
def validate_fee_payment(student_id, role):
    student_id = student_id.strip()
    role = role.strip().title()
    
    if role != "Administrator":
        print("Access Denied: Only Administrators can validate fee payments")
        return
    
    # Search for the student in the students list
    for i, encrypted_student in enumerate(students):
        student = decrypt_data(encrypted_student)  # Decrypt student data
        if student["studentID"] == student_id:
            student["feesPaid"] = True
            
            # Encrypt the updated student data and store it back in the list
            students[i] = encrypt_data(student)
            
            print(f"Fees validated for student {student['firstName']} {student['lastName']}.")
            return
    
    # If the student is not found
    print("Validation failed: Student not found")

#-----------------------------------------------------------------------------------------------------------------------------------------------------
# COURSE ENROLLMENT FUNCTION

# Define the course enrollment function
def enroll_student_in_course(student_id, selected_courses, role):
    student_id = student_id.strip()
    role = role.strip().title()
    
    # Ensure that only administrators can enroll students in courses
    if role != "Administrator":
        print("Access Denied: Only Administrators can enroll students in courses")
        return
    
    selected_courses = [course.strip().title() for course in selected_courses]  # Normalize course names
    
    # Search for the student in the students list
    for encrypted_student in students:
        student = decrypt_data(encrypted_student)  # Decrypt student data
        if student["studentID"] == student_id:
            if student["feesPaid"]:
                for course in selected_courses:
                    if course not in available_courses:
                        print(f"Enrollment failed: {course} is not a valid course")
                        return
                
                student["selectedCourses"] = selected_courses
                encrypted_student = encrypt_data(student)  # Re-encrypt updated data
                print(f"Student {student['firstName']} {student['lastName']} has been enrolled in: {', '.join(selected_courses)}.")
            else:
                print(f"Enrollment failed: Fees have not been paid for student {student['firstName']} {student['lastName']}.")
            return
    
    # If the student is not found
    print("Enrollment failed: Student not found")

#----------------------------------------------------------------------------------------------------------------------------------------------------
# VIEW STUDENT INFORMATION FUNCTION

# Define the function to view student information
def view_student_information(student_id, role):
    student_id = student_id.strip()
    role = role.strip().title()
    
    # Search for the student in the students list
    for encrypted_student in students:
        student = decrypt_data(encrypted_student)  # Decrypt student data
        if student["studentID"] == student_id:
            # Display relevant information based on the role
            if role == "Administrator" or role == "Instructor":
                # Administrators and Instructors can view all student information
                print(f"Student ID: {student['studentID']}")
                print(f"Name: {student['firstName']} {student['lastName']}")
                print(f"Email: {student['email']}")
                print(f"Date of Birth: {student['dateOfBirth']}")
                print(f"Selected Courses: {', '.join(student['selectedCourses'])}")
                print(f"Fees Paid: {'Yes' if student['feesPaid'] else 'No'}")
            
            elif role == "Student":
                # Students can view their own information
                print(f"Student ID: {student['studentID']}")
                print(f"Name: {student['firstName']} {student['lastName']}")
                print(f"Email: {student['email']}")
                print(f"Date of Birth: {student['dateOfBirth']}")
                print(f"Selected Courses: {', '.join(student['selectedCourses'])}")
            
            elif role == "Parent":
                # Parents can view basic information and the selected courses of their child
                print(f"Name: {student['firstName']} {student['lastName']}")
                print(f"Selected Courses: {', '.join(student['selectedCourses'])}")
                print(f"Fees Paid: {'Yes' if student['feesPaid'] else 'No'}")
            
            else:
                print("Access Denied: Invalid role")
            return
    
    # If the student is not found
    print("Information not found: Student not found")

#------------------------------------------------------------------------------------------------------------------------------------------------------
# SCORING STUDENTS COURSES FUNCTION

# Define the function to score (grade) a student
def score_student(student_id, course_name, score, role):
    student_id = student_id.strip()
    course_name = course_name.strip().title()
    role = role.strip().title()
    
    # Ensure that only instructors or administrators can assign scores
    if role not in ["Instructor", "Administrator"]:
        print("Access Denied: Only Instructors or Administrators can assign scores")
        return
    
    # Search for the student in the students list
    for encrypted_student in students:
        student = decrypt_data(encrypted_student)  # Decrypt student data
        if student["studentID"] == student_id:  # Ensure student is enrolled in course being scored
            if course_name in student["selectedCourses"]:  # Check if student is enrolled in the course
                if student_id not in results:
                    results[student_id] = {}  # Initialize the student's results if not present
                results[student_id][course_name] = score
                print(f"Score {score} assigned to {student['firstName']} {student['lastName']} for {course_name}.")
            else:
                print(f"Scoring failed: Student not enrolled in course {course_name}.")
            return
    
    # If the student is not found
    print("Scoring failed: Student not found")


#------------------------------------------------------------------------------------------------------------------------------------------------------
# VIEWING SCORED RESULTS FUNCTION

# Define the function to view a student's results
def view_student_results(student_id, role):
    student_id = student_id.strip()
    role = role.strip().title()
    
    # Search for the student in the students list
    for encrypted_student in students:
        student = decrypt_data(encrypted_student)  # Decrypt student data
        if student["studentID"] == student_id:
            # Check if the student has any results
            if student_id in results:
                print(f"Results for {student['firstName']} {student['lastName']}:")
                for course_name, score in results[student_id].items():
                    print(f"{course_name}: {score}")
            else:
                print(f"No results available for {student['firstName']} {student['lastName']}.")
            return
    
    # If the student is not found
    print("Results not found: Student not found")

#-------------------------------------------------------------------------------------------------------------------------------------------------------

# GENERATE STUDENT PROGRESS REPORT

def generate_progress_report():
    student_id = input("Enter the student ID: ").strip()
    role = input("Enter your role (Administrator/Instructor/Student): ").strip().title()
    
    # Check if the role has permission to view progress reports
    if role not in ["Administrator", "Instructor", "Student"]:
        print("Access Denied: Only Administrators, Instructors, or Students can generate progress reports.")
        return
    
    # Search for the student in the students list
    for encrypted_student in students:
        student = decrypt_data(encrypted_student)  # Decrypt student data
        if student["studentID"] == student_id:
            # Print basic student information
            print(f"Progress Report for {student['firstName']} {student['lastName']}:")
            print(f"Student ID: {student['studentID']}")
            print(f"Email: {student['email']}")
            print(f"Date of Birth: {student['dateOfBirth']}")
            print(f"Selected Courses: {', '.join(student['selectedCourses'])}")
            print(f"Fees Paid: {'Yes' if student['feesPaid'] else 'No'}")
            
            # Print scores for each course
            if student_id in results:
                print("\nCourse Scores:")
                total_score = 0
                count = 0
                for course_name, score in results[student_id].items():
                    try:
                        numeric_score = float(score)  # Convert score to float
                        total_score += numeric_score
                        count += 1
                        print(f"{course_name}: {numeric_score}")
                    except ValueError:
                        print(f"{course_name}: Invalid score data")
                
                # Calculate and print average score
                if count > 0:
                    average_score = total_score / count
                    print(f"\nAverage Score: {average_score:.2f}")
                else:
                    print("\nAverage Score: No valid scores available")
            else:
                print("\nNo scores available.")
            
            return
    
    # If the student is not found
    print("Progress Report: Student not found")


#-------------------------------------------------------------------------------------------------------------------------------------------------------

# MAIN MENU FUNCTION:

def main_menu():
    while True:
        print("\n--- BEP09 Bootcamp Management System ---")
        print("1. Register Student")
        print("2. Validate Fee Payment (Admin only)")
        print("3. Enroll Student in Course (Admin only)")
        print("4. View Student Information")
        print("5. Score Student Course (Instructor/Admin only)")
        print("6. View Student Results")
        print("7. Generate Student Progress Report")
        print("8. Exit")
        
        choice = input("Select an option (1/2/3/4/5/6/7/8): ")
        
        if choice == "1":
            register_student()
        elif choice == "2":
            admin_actions(validate_fee_payment)
        elif choice == "3":
            admin_actions(enroll_student_in_course)
        elif choice == "4":
            view_info()
        elif choice == "5":
            admin_actions(score_student)
        elif choice == "6":
            view_results()
        elif choice == "7":
            generate_progress_report()   
        elif choice == "8":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Helper function for admin actions
def admin_actions(action_function):
    role = input("Enter your role (Administrator/Instructor/Student/Parent): ").strip().title()
    
    # List of roles that are allowed
    valid_roles = ["Administrator", "Instructor"]
    
    # Ensure that only valid roles can proceed
    if role not in valid_roles:
        print("Access Denied: This action is restricted to Administrators/Instructors.")
        return
    
    # Prompt for additional input based on the action function
    student_id = input("Enter the student ID: ").strip()
    
    if action_function == validate_fee_payment:
        action_function(student_id, role)
    elif action_function == enroll_student_in_course:
        courses = input("Enter courses to enroll in (comma-separated): ").split(",")
        courses = [course.strip() for course in courses]
        action_function(student_id, courses, role)
    elif action_function == score_student:
        course_name = input("Enter the course name: ").strip().title()
        score = input("Enter the score: ").strip()
        action_function(student_id, course_name, score, role)


# View student information based on role
def view_info():
    role = input("Enter your role (Administrator/Instructor/Student/Parent): ")
    student_id = input("Enter the student ID: ")
    view_student_information(student_id, role)

# View student results
def view_results():
    role = input("Enter your role (Administrator/Instructor/Student/Parent): ")
    student_id = input("Enter the student ID: ")
    view_student_results(student_id, role)

# Start the main menu
if __name__ == "__main__":
    main_menu()


#--------------------------------------------------------------------------------------------------------------------------------------------------------




