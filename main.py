import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tkinter import *
from tkinter import messagebox, ttk
import os

# -----------------------------
# ✅ Database Connection Details
# -----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "asad.",
    "database": "Student_database"
}

SCHEMA_FILE = "schema.sql"

# -----------------------------
# ✅ Step 1: Auto-create Database and Tables
# -----------------------------


def setup_database():
    # Create database if not exists
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.database = DB_CONFIG["database"]
        cursor.close()
        conn.close()
        print(f"✅ Database '{DB_CONFIG['database']}' is ready.")
    except mysql.connector.Error as err:
        print(f"❌ Database setup error: {err}")
        return

    # Create tables and insert data from schema.sql
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        schema_path = os.path.join(os.path.dirname(__file__), SCHEMA_FILE)
        if not os.path.exists(schema_path):
            print(f"⚠️ schema.sql not found at: {schema_path}")
            return

        with open(schema_path, "r", encoding="utf-8") as f:
            sql_commands = f.read().split(";")

        created_tables = 0
        inserted_rows = 0
        for cmd in sql_commands:
            cmd = cmd.strip()
            if not cmd or cmd.lower().startswith(("create database", "use ")):
                continue
            try:
                cursor.execute(cmd)
                if cmd.lower().startswith("create table"):
                    created_tables += 1
                elif cmd.lower().startswith("insert into"):
                    inserted_rows += cursor.rowcount
            except mysql.connector.Error as err:
                if err.errno in (1050, 1062):  # table exists / duplicate entry
                    pass
                else:
                    print(f"⚠️ SQL Warning: {err}")

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Tables verified/created: {created_tables}")
        print(f"✅ Data inserted: {inserted_rows} rows")

    except mysql.connector.Error as err:
        print(f"❌ Table or data setup failed: {err}")


# Run database setup before GUI starts
setup_database()

# -----------------------------
# ✅ Student Performance Analyzer
# -----------------------------


def show_performance_chart():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, subject, marks FROM records")
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No Data", "No student records found.")
        return

    students = {}
    for row in data:
        student_name, subject, marks = row
        if student_name not in students:
            students[student_name] = []
        students[student_name].append(marks)

    names = list(students.keys())
    marks_array = np.array(list(students.values()))
    avg_marks = np.mean(marks_array, axis=1)

    def calculate_grade(avg):
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    grades = [calculate_grade(mark) for mark in avg_marks]

    print("\n--- Student Performance Report ---")
    for name, avg, grade in zip(names, avg_marks, grades):
        print(f"{name:<15} | Average: {avg:.2f} | Grade: {grade}")
    print("-----------------------------------\n")

    grade_colors = {
        "A+": "#00b050",
        "A": "#92d050",
        "B": "#ffc000",
        "C": "#f79646",
        "D": "#ff5050",
        "F": "#c00000"
    }

    colors = [grade_colors[g] for g in grades]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(names, avg_marks, color=colors,
                  edgecolor='black', linewidth=1)

    ax.set_title("Average Marks and Grades of Students",
                 fontsize=15, weight='bold', pad=15)
    ax.set_xlabel("Student Names", fontsize=12, labelpad=10)
    ax.set_ylabel("Average Marks", fontsize=12)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=0, ha='center', fontsize=10)

    for bar, grade, avg in zip(bars, grades, avg_marks):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"{grade} ({avg:.1f})", ha='center', va='bottom', fontsize=10, weight='bold')

    legend_patches = [mpatches.Patch(
        color=color, label=f'Grade {grade}') for grade, color in grade_colors.items()]
    ax.legend(handles=legend_patches, title="Grade Legend",
              loc="upper right", frameon=True)

    plt.tight_layout()
    plt.show()

# -----------------------------
# ✅ Payment Viewer (GUI)
# -----------------------------


def fetch_payments():
    student_name = entry_name.get().strip()
    if not student_name:
        messagebox.showwarning("Input Error", "Please enter a student's name.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        SELECT r.student_name, p.payment_month, p.amount, p.payment_method, p.status
        FROM payments p
        JOIN records r ON r.student_id = p.student_id
        WHERE r.student_name = %s
        ORDER BY p.payment_id DESC
        """
        cursor.execute(query, (student_name,))
        data = cursor.fetchall()
        conn.close()

        for row in tree.get_children():
            tree.delete(row)

        if not data:
            messagebox.showinfo(
                "No Record", f"No payments found for '{student_name}'.")
            return

        for row in data:
            tree.insert("", END, values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


# -----------------------------
# ✅ Tkinter GUI Setup
# -----------------------------
root = Tk()
root.title("🎓 Student Management System")
root.geometry("750x520")
root.resizable(False, False)
root.configure(bg="#f4f4f4")

title = Label(root, text="Student Billing & Performance", font=(
    "Segoe UI", 18, "bold"), bg="#f4f4f4", fg="#333")
title.pack(pady=10)

frame = Frame(root, bg="#f4f4f4")
frame.pack(pady=5)

Label(frame, text="Enter Student Name:", font=("Segoe UI", 12),
      bg="#f4f4f4").grid(row=0, column=0, padx=5)
entry_name = Entry(frame, font=("Segoe UI", 12), width=25)
entry_name.grid(row=0, column=1, padx=5)

btn_search = Button(frame, text="Show Bill", font=(
    "Segoe UI", 11, "bold"), bg="#0078D7", fg="white", command=fetch_payments)
btn_search.grid(row=0, column=2, padx=8)

btn_chart = Button(frame, text="Show Performance Chart", font=(
    "Segoe UI", 11, "bold"), bg="#28A745", fg="white", command=show_performance_chart)
btn_chart.grid(row=0, column=3, padx=8)

table_frame = Frame(root, bg="#f4f4f4")
table_frame.pack(pady=15)

columns = ("Student Name", "Date", "Amount", "Method", "Status")

tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
tree.pack()

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER, width=150)

scrollbar = Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

root.mainloop()
