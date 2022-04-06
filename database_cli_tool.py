import os
import sys
import platform
import termcolor
import mysql.connector as connector

os.system("color")
COLOR = termcolor.colored
os_platform = platform.platform().lower()
if "windows" in os_platform:
    clear_command = "cls"
else:
    clear_command = "clear"

def create_connection():
    connection = connector.connect(
        host="localhost", user="root",
        passwd="root", db="university"
    )

    return connection

def get_results(query):
    connetion = create_connection()
    cursor = connetion.cursor()
    cursor.execute(query)
    columns = cursor.column_names
    results = cursor.fetchall()
    connetion.close()

    return columns, results

def execute_query(query):
    connetion = create_connection()
    cursor = connetion.cursor()
    cursor.execute(query)
    connetion.commit()
    connetion.close()

def print_header(header):
    print(COLOR("*" * 50, "blue"))
    print(COLOR(f"\t\t{header}\t\t", "blue"))
    print(COLOR("*" * 50, "blue"))

def print_menu():
    header = "UNIVERSITY DATABASE"
    print_header(header)
    print(COLOR("\n\t1. Display Data\n\
        2. Insert Data\n\
        3. Modify Budget\n\
        4. Delete Department\n\
        0. Exit\n\
        ", "green"
    ))

def go_to_main_menu():
    input(COLOR("\nPress Enter to go to main menu...", "magenta"))
    os.system(clear_command)
    main()

def print_table(columns, results):
    format_row = "{:>20}" * (len(columns))
    print(COLOR(format_row.format(*columns), "green"))
    for row in results:
        print(format_row.format(*row))

def display_data():
    os.system(clear_command)
    print_header("DISPLAY DATA")
    user_input = input(COLOR("Enter the table name you want to display data: ", "yellow"))
    query = f"select * from {user_input}"
    try:
        columns, results = get_results(query)
        print_table(columns, results)
    except Exception as e:
        print(COLOR(f"\nERROR: {e}", "red"))
    go_to_main_menu()

def insert_data():
    os.system(clear_command)
    print_header("INSERT DATA")
    table_name = input(COLOR("Enter the table name you want to insert data: ", "yellow"))
    query = f"SHOW columns FROM {table_name}"
    try:
        _, results = get_results(query)
    except Exception as e:
        print(COLOR(f"\nERROR: {e}", "red"))
        go_to_main_menu()

    cloumn_names = [i[0] for i in results]
    print(COLOR("\nEnter the values for each column one by one, after entering the value press enter...\n", "magenta"))
    data_dict = {}
    for column in cloumn_names:
        user_input = input(COLOR(f"{column}: ", "cyan"))
        data_dict[column] = user_input

    query = f"insert into {table_name} values {tuple(data_dict.values())}"
    try:
        execute_query(query)
        print(COLOR("\nRecord inserted successfully...", "green"))
    except Exception as e:
        print(COLOR(f"\nERROR: {e}", "red"))
    go_to_main_menu()

def modify_budget():
    os.system(clear_command)
    print_header("MODIFY BUDGET")
    dept_name = input(COLOR("Enter the department name you want to update: ", "yellow"))
    query = f"select * from department where dept_name = '{dept_name}'"
    try:
        columns, results = get_results(query)
        if not results:
            print(COLOR(f"\nGiven department name: {dept_name} is not there in database", "red"))
            go_to_main_menu()
    except Exception as e:
        print(COLOR(f"\nERROR: {e}", "red"))
        go_to_main_menu()
    print("Results from the database...")
    print_table(columns, results)        
    user_input = input(COLOR("\nEnter the budget value you want to update: ", "yellow"))
    if user_input.isdigit() or user_input.isdecimal():
        query = f"update department set budget = {user_input} where dept_name = '{dept_name}'"
        try:
            execute_query(query)
            print(COLOR("\n Record updated successfully...", "green"))
        except Exception as e:
            print(COLOR(f"\nERROR: {e}", "red"))
    else:
        print(COLOR("\nERROR: Budget value should be in either integer or decimal", "red"))
    go_to_main_menu()

def delete_department():
    os.system(clear_command)
    print_header("DELETE DEPARTMENT")
    dept_name = input(COLOR("Enter the department name you want to delete: ", "yellow"))
    query = f"select * from department where dept_name = '{dept_name}'"
    try:
        columns, results = get_results(query)
        if not results:
            print(COLOR("\nERROR: Invalid department name entered", "red"))
            go_to_main_menu()
        print("Results from the database...")
        print_table(columns, results)
    except Exception as e:
        print(COLOR(f"\nERROR: {e}", "red"))
        go_to_main_menu()
    user_input = input("\nAre you sure (Y/N): ")
    if user_input.lower() not in ["yes", "no", "y", "n"]:
        print(COLOR("\nERROR: Invalid input given", "red"))
        go_to_main_menu()

    if user_input.lower() in ["yes", "y"]:
        query = f"delete from department where dept_name = '{dept_name}'"
        try:
            execute_query(query)
            print(COLOR("\nRecord deleted successfully...", "green"))
        except Exception as e:
            print(COLOR(f"\nERROR: {e}", "red"))

    go_to_main_menu()

def exit():
    print("\nTHANK YOU...")
    sys.exit()

def main():
    menu_options = {
        "1": display_data, "2": insert_data,
        "3": modify_budget, "4": delete_department,
        "0": exit
    }
    print_menu()
    user_input = input(COLOR("Select and option to perform: ", "yellow"))

    if user_input not in menu_options or not user_input:
        print("\nInvalid option selected, please select from the available options")
        sys.exit(1)


    menu_options[user_input]()

if __name__ == "__main__":
    main()