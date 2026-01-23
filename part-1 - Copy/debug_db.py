
import sqlite3

try:
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check tables first
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables found:", [t['name'] for t in tables])
    
    if 'students' in [t['name'] for t in tables]:
        print("\n--- Content of 'students' table ---")
        rows = cursor.execute('SELECT * FROM students').fetchall()
        if not rows:
            print("Table is empty.")
        else:
            # Print header
            print(f"{'id':<5} {'name':<15} {'email':<25} {'course':<10}")
            print("-" * 60)
            for row in rows:
                print(f"{row['id']:<5} {row['name']:<15} {row['email']:<25} {row['course']:<10}")
    else:
        print("Table 'students' does not exist.")

    conn.close()

except Exception as e:
    print(f"Error: {e}")
