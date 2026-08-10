students = []


def display_menu():
    print("\nSTUDENT MANAGEMENT SYSTEM")
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student (by ID or Name)")
    print("4. Update Student Details")
    print("5. Delete Student Record")
    print("6. Exit")


def add_student():
    print("\nAdd New Student")

    while True:
        student_id = input("Enter Student ID: ").strip()
        if not student_id:
            print("Student ID cannot be empty.")
            continue
        if any(s["ID"].lower() == student_id.lower() for s in students):
            print("A student with this ID already exists. Try again.")
        else:
            break

    name = input("Enter Name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter Name: ").strip()

    while True:
        try:
            age = int(input("Enter Age: "))
            if age <= 0:
                print("Age must be a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a whole number for age.")

    course = input("Enter Course: ").strip()

    while True:
        try:
            marks = float(input("Enter Marks (0-100): "))
            if 0 <= marks <= 100:
                break
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Invalid input! Please enter a numeric value for marks.")

    new_student = {
        "ID": student_id,
        "Name": name,
        "Age": age,
        "Course": course,
        "Marks": marks,
    }

    students.append(new_student)
    print(f"Student '{name}' (ID: {student_id}) added successfully!")


def view_all_students():
    print("\nAll Student Records")
    if not students:
        print("No student records found.")
        return

    print(
        f"{'ID':<10} | {'Name':<20} | {'Age':<5} | {'Course':<15} | {'Marks':<6}"
    )

    for s in students:
        print(
            f"{s['ID']:<10} | {s['Name']:<20} | {s['Age']:<5} | {s['Course']:<15} | {s['Marks']:<6.2f}"
        )


def search_student():
    print("\nSearch Student")
    if not students:
        print("No student records found.")
        return

    query = input("Enter Student ID or Name to search: ").strip().lower()
    matches = [
        s
        for s in students
        if query in s["ID"].lower() or query in s["Name"].lower()
    ]

    if matches:
        print(f"\nFound {len(matches)} matching record(s):")
        print(
            f"{'ID':<10} | {'Name':<20} | {'Age':<5} | {'Course':<15} | {'Marks':<6}"
        )
        for s in matches:
            print(
                f"{s['ID']:<10} | {s['Name']:<20} | {s['Age']:<5} | {s['Course']:<15} | {s['Marks']:<6.2f}"
            )
    else:
        print(f"No student found matching '{query}'.")


def update_student():
    print("\nUpdate Student")
    if not students:
        print("No student records found.")
        return

    target_id = input("Enter Student ID to update: ").strip()

    student = next(
        (s for s in students if s["ID"].lower() == target_id.lower()), None
    )

    if not student:
        print(f"Student with ID '{target_id}' not found.")
        return

    print(f"\nUpdating details for {student['Name']} (ID: {student['ID']}).")
    print("Press Enter to keep existing values unchanged.")

    new_name = input(f"New Name [{student['Name']}]: ").strip()
    if new_name:
        student["Name"] = new_name

    new_age = input(f"New Age [{student['Age']}]: ").strip()
    if new_age:
        try:
            student["Age"] = int(new_age)
        except ValueError:
            print("Invalid age entered; keeping old value.")

    new_course = input(f"New Course [{student['Course']}]: ").strip()
    if new_course:
        student["Course"] = new_course

    new_marks = input(f"New Marks [{student['Marks']}]: ").strip()
    if new_marks:
        try:
            val = float(new_marks)
            if 0 <= val <= 100:
                student["Marks"] = val
            else:
                print("Marks out of range (0-100); keeping old value.")
        except ValueError:
            print("Invalid marks entered; keeping old value.")

    print(f"Record for ID '{student['ID']}' updated successfully!")


def delete_student():
    print("\nDelete Student")
    if not students:
        print("No student records found.")
        return

    target_id = input("Enter Student ID to delete: ").strip()

    for idx, s in enumerate(students):
        if s["ID"].lower() == target_id.lower():
            confirm = (
                input(f"Are you sure you want to delete {s['Name']}? (y/n): ")
                .strip()
                .lower()
            )
            if confirm == "y":
                removed = students.pop(idx)
                print(
                    f"Student '{removed['Name']}' (ID: {removed['ID']}) deleted."
                )
            else:
                print("Action canceled.")
            return

    print(f"Student with ID '{target_id}' not found.")


def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("\nExiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()
