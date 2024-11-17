import requests

#making a change for pr

SERVER_PORT = 5000
SERVER_URL = "http://18.207.203.105:" + str(SERVER_PORT)
STUDENT_API = "students"

def accessServer():
    ip_address = input("Please enter your host address: ")
    port_num = input("Please enter the port: ")
    return ip_address, port_num
        
def getStudentList(ip, port):
    response = requests.get(f"http://{ip}:{port}/{STUDENT_API}")
    if response.status_code == 200:
        students_list = response.json()
        for student in students_list["students"]:
            print(f'1. Name: {student["name"]}')
            print(f'2. Age: {student["age"]}')
            print(f'3. ID: {student["id"]}')
            print(10 * "-")
    else:
        print("Error bad request")
        
def getStudentInfo(ip, port):
    student_id = input("Please enter student id: ")
    response = requests.get(f"http://{ip}:{port}/{STUDENT_API}/{student_id}")
    if response.status_code == 200:  
        student_by_id = response.json()  
        print(f'1. Name: {student_by_id["name"]}')
        print(f'2. Age: {student_by_id["age"]}')
        print(f'3. ID: {student_by_id["id"]}')
        print(10 * "-")
    else:
        print(f"Error fetching student with id {student_id}")

def saveNewStudent(ip, port):
    new_name = input("Please enter student name: ")
    new_age = input("Please enter student age: ")
    student_data = {
        "name": new_name,
        "age": new_age
    }
    response = requests.post(f"http://{ip}:{port}/{STUDENT_API}", json=student_data)
    if response.status_code == 201:  
        print("New student added successfully.")
    else:
        print("Error adding student.")
    
def changeStudentName(ip, port):
    #put does not work as the server expects name and age keys together
    # Error updating student: 400 - {"error":"Bad Request, data must include 'name' and 'age'"}
    student_id = input("Please enter student id: ")
    new_student_name = input("Please enter new student name: ")
    response = requests.get(f"http://{ip}:{port}/{STUDENT_API}/{student_id}")
    update_name= response.json()
    update_name["name"] = new_student_name
    response = requests.put(f"http://{ip}:{port}/{STUDENT_API}/{student_id}", json=update_name)
    if response.status_code == 200:
        print("Student name updated successfully.")
    else:
        print(f"Error updating student: {response.status_code} - {response.text}")

        
def changeStudentAge(ip, port):
    student_id = input("Please enter student id: ")
    new_student_age = input("Please enter student age: ")
    response = requests.get(f"http://{ip}:{port}/{STUDENT_API}/{student_id}")
    update_age = response.json()
    update_age["age"] = new_student_age
    response = requests.put(f"http://{ip}:{port}/{STUDENT_API}/{student_id}", json=update_age)
    if response.status_code == 200:
        print("Student name updated successfully.")
    else:
        print(f"Error updating student: {response.status_code} - {response.text}")
        
def deleteStudent(ip, port):
    student_id = input("Please enter student id to erase: ")
    response = requests.delete(f"http://{ip}:{port}/{STUDENT_API}/{student_id}")
    if response.status_code == 200:
        print("Student name deleted successfully.")
    else:
        print("Error deleting student:")
        
def serverOptions(ip_address, port_num):
    ip, port = ip_address, port_num
    options = [
        "Get student list",
        "Get specific student information",
        "Save a new student",
        "Change student name",
        "Change student age",
        "Delete student",
        "Exit"
    ]
    options_func_call = {"1": getStudentList,
               "2": getStudentInfo,
               "3": saveNewStudent,
               "4": changeStudentName,
               "5": changeStudentAge,
               "6": deleteStudent,
               "Exit": ""
               }
    for index, options in enumerate(options, 1):
        print(f"{index}. {options}")
    selected_option = input("Please select a menu option (1-7): ")
    if selected_option == "7":
        return False
    if selected_option in options_func_call.keys():
        options_func_call[selected_option](ip, port)  
        return True
    else:
        print("Invalid option, please select again.")
        return True
    
def main():
    ip_aws, port_aws = accessServer() 
    flag = True
    while flag:
       flag = serverOptions(ip_aws, port_aws)

if __name__ == "__main__":
    main()