# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   TONeill, 06.04.2025, Created Script
# ------------------------------------------------------------------------------------------ #

# ----- Import libraries ----- #
import json

# ----- Define the data constants ----- #
MENU: str = """
---- Course Registration Program --------
  Select from the following menu:  
    1. Register a student for a course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
"""
FILE_NAME: str = "Enrollments.json"

# ----- Define the data variables ----- #
students: list = []  # a table of student data
menu_choice: str = ""  # holds the choice made by the user.


class Person:
    """
    A class representing person data.

    Properties:
    - first_name (str): The person's first name.
    - last_name (str): The person's last name.

    ChangeLog:
    - TONeill, 06.04.2025, created the class.
    """

    def __init__(self, first_name: str = "", last_name: str = ""):
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def first_name(self):
        return self.__first_name.title()  # formatting code

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":  # is character or empty string
            self.__first_name = value
        else:
            raise ValueError("The first name must only contain letters.")

    @property
    def last_name(self):
        return self.__last_name.title()  # formatting code

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":  # is character or empty string
            self.__last_name = value
        else:
            raise ValueError("The last name must only contain letters.")

    def __str__(self):
        return f'{self.first_name},{self.last_name}'


class Student(Person):
    """
    A class representing student data.

    Properties:
    - first_name (str): The student's first name, inherited from Person.
    - last_name (str): The student's last name, inherited from Person.
    - course_name (str): The student's course name.

    ChangeLog:
    - TONeill, 06.04.2025, created the class.
    """

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        super().__init__(first_name = first_name, last_name = last_name)
        self.__course_name = course_name

    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'


# Processing ----------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files

    ChangeLog:
    - RRoot, 1.1.2030, created class
    - TONeill, 06.04.2025, formatting edits
    """

    @staticmethod
    def read_data_from_file(file_name: str):
        """
        This method reads data from a JSON file, loads it into a list of dictionary rows,
        then returns the list filled with student data.

        ChangeLog:
        - RRoot, 1.1.2030, created method
        - TONeill, 06.04.2025, formatting edits

        :param file_name: string data with name of file to read from
        :return: list
        """

        try:
            # get a list of dictionary rows from the data file
            file = open(file_name, "r")
            json_students = json.load(file)

            # convert the list of dictionary rows into a list of Student objects
            student_objects = []
            for student in json_students:
                student_object: Student = Student(first_name = student["FirstName"],
                                                  last_name = student["LastName"],
                                                  course_name = student["CourseName"])
                student_objects.append(student_object)
            file.close()

        except Exception as e:
            IO.output_error_messages(message = "Error: There was a problem reading the file.", error = e)

        finally:
            if file and not file.closed:
                file.close()

        return student_objects

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        This function writes data to a JSON file with data from a list of dictionary rows

        ChangeLog:
        - RRoot, 1.1.2030, created method
        - TONeill, 06.04.2025, formatting edits

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file
        :return: None
        """

        try:
            list_of_dictionary_data: list = []

            for student in student_data:
                student_json: dict \
                    = {"FirstName": student.first_name, "LastName": student.last_name, "CourseName": student.course_name}
                list_of_dictionary_data.append(student_json)

            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file, indent = 4)
            file.close()
            IO.output_student_and_course_names(student_data = student_data)
        except Exception as e:
            message = "Error: There was a problem writing to the file.\n"
            message += "Please check that the file is not open in another program."
            IO.output_error_messages(message = message, error = e)
        finally:
            if file and not file.closed:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer methods that manage user input and output

    ChangeLog:
    - RRoot, 1.1.2030, created class
    - RRoot, 1.2.2030, added menu output and input methods
    - RRoot, 1.3.2030, added a method to display the data
    - RRoot, 1.4.2030, added a method to display custom error messages
    - TONeill, 06.04.2025, formatting edits
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        This method displays a custom error message to the user

        ChangeLog:
        - RRoot, 1.3.2030, created method

        :param message: string with message data to display
        :param error: exception object with technical message to display
        :return: None
        """
        print(message, end = "\n\n")
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep = '\n')

    @staticmethod
    def output_menu(menu: str):
        """
        This method displays the menu of choices to the user

        ChangeLog:
        - RRoot, 1.1.2030, created method
        - TONeill, 06.04.2025, formatting edits

        :return: None
        """
        print()  # adding extra space to make it look nicer.
        print(menu)
        print()  # adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """
        this method gets a menu choice from the user

        ChangeLog:
        - RRoot, 1.1.2030, created method
        - TONeill, 06.04.2025, formatting edits

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu selection: ")
            if choice not in ("1","2","3","4"):  # note these are strings
                raise Exception("Please only choose 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """
        This method displays the student and course names to the user

        ChangeLog:
        - RRoot, 1.1.2030, created method
        - TONeill, 06.04.2025, formatting edits

        :param student_data: list of dictionary rows to be displayed
        :return: None
        """

        print("-" * 50)
        for student in student_data:

            print(f'Student {student.first_name} {student.last_name} '
                  f'is enrolled in {student.course_name}')

        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """
        This method gets a student's first name, last name, and course name from the user

        ChangeLog:
        - RRoot, 1.1.2030, created function
        - TONeill, 06.04.2025, formatting edits

        :param student_data: list of dictionary rows to be filled with input data
        :return: list
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("First name must only contain letters.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("Last name must only contain letters.")
            course_name = input("Please enter the name of the course: ")

            student = Student(first_name = student_first_name, last_name = student_last_name, course_name = course_name)
            student_data.append(student)
            print()
            print(f"Student {student_first_name} {student_last_name} has successfully been registered for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message = "One of the values was the incorrect type of data.", error = e)
        except Exception as e:
            IO.output_error_messages(message = "Error: There was a problem with your entered data.", error = e)
        return student_data


# Main Body ------------------------------------------ #

# when the program starts, read the file data into a list of lists (table)
# ----- Extract the data from the file ----- #
students = FileProcessor.read_data_from_file(file_name = FILE_NAME)

# ----- Present and Process the data ----- #
while (True):

    # Present the menu of choices
    IO.output_menu(menu = MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # this will not work if it is an integer!
        students = IO.input_student_data(student_data = students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name = FILE_NAME, student_data = students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop

print("Thank you for using this program!")