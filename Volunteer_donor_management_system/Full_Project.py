import sqlite3
from datetime import datetime, timedelta

DB_NAME = "red_cross.db"

# database setup

def get_connection():
    """ open (and if needed create) the database and return a connection object """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def setup_database():
    """ create the donors and volunteers tables if they don't exist yet.  """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            phone TEXT,
            location TEXT,
            last_donation_date TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS volunteers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            event TEXT NOT NULL,
            hours TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()

# Including features/details about donors, donations, campaigns, and volunteers.

def add_donor():
    """ add details about donor if he/she is new in database """
    name = input("Enter donr's name: ").strip()
    blood_group = input("Enter donor's blood group (e.g A+, B+ O+, A-): ").strip().upper()
    phone = input("Enter donor's phone number: ").strip()
    location = input("Enter donor's location: ").strip()
    last_donation_date = input("Enter donor's last date of donation (YYYY-MM-DD) and leave blank if never donated: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO donors (name, blood_group, phone, location, last_donation_date)"
        "VALUES (?, ?, ?, ?, ?)",
        (name, blood_group, phone, location, last_donation_date or None)
    )
    conn.commit()
    conn.close()
    print(f"\nDonor '{name}' has been added successfully to the database. \n")

def search_donors():
    """ searching for a donor in the database by blood type and location """
    blood_group = input("Search by blood group (leave blank to skip): ").strip()
    location = input("Search by location (leave blank to skip): ").strip()

    query = "SELECT id, name, blood_group, phone, location, last_donation_date FROM donors WHERE 1=1"
    params = []

    if blood_group:
        query += " AND blood_group = ?"
        params.append(blood_group)
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()

    if not results:
        print("\nNo matching donors found.\n")
        return

    print(f"\n{'ID':<5}{'Name':<20}{'Group':<10}{'Phone':<15}{'Location':<20}{'Last Donation Date':<15} {'Eligible Now?'}")
    print("_" * 100)
    for row in results:
        donor_id, name, group, phone, loc, last_date = row
        eligible = is_eligible_to_donate(last_date)
        print(f"{donor_id:<5}{name:<20}{group:<10}{phone:<15}{loc:<15}{str(last_date):<15}{'Yes' if eligible else 'No'}")
    print()

def is_eligible_to_donate(last_donation_date):
    """
    Check if a donor is eligible to donate blood based on the last donation date.
    A donor is eligible if they have never donated before or if it has been at least 90 days since their last donation.
    """
    if not last_donation_date:
        return True

    try:
        last_donation = datetime.strptime(last_donation_date, "%Y-%m-%d")
    except ValueError:
        return True     # Invalid date format, not eligible to donate blood
    return datetime.now() - last_donation >= timedelta(days = 90)

#--------------------------------------------------------------------------
# VOLUNTERS FEATURES (Including details like contact information and availability)
#--------------------------------------------------------------------------

def log_volunteer_hours():
    name = input("Enter volunteer's name: ").strip()
    event = input("Enter events/activities volunteered for: ").strip()
    hours = float(input("Enter number of hours volunteered: ").strip())
    date = input("Enter date of volunteer work (YYYY-MM-DD): ").strip()

    if not date:
        date = datetime.now().strftime("%Y-%m-%d") # Use the current date if no date is provided

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO volunteers (name, event, hours, date) VALUES (?, ?, ?, ?)",
        (name, event, hours, date),
    )

    conn.commit()
    conn.close()
    print(f"\nVolunteer '{name}' has been logged successfully for '{hours}' hours. \n")
    check_and_issue_certificate(name)

def check_and_issue_certificate(name):
    """ Auto-generate a simple text certificate for volunteers who have successfully completed a milestone of 20, 50, or 100 hours of volunteer work."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(hours) FROM volunteers WHERE name = ?", (name,))
    total_hours = cur.fetchone()[0] or 0
    conn.close()

    milestones = [20, 50, 100]
    for milestone in milestones:
        if total_hours >= milestone:
            filename = f"certificate_{name.replace(' ', '_')}_{milestone}_hours.txt"
            # only issue if not already generated (Simply check)
            try:
                with open(filename, "x") as f:
                    f.write(
                        f"CERTIFICATE OF RECOGNITION\n\n"
                        f"This certifies that {name} has successfully contributed {total_hours:.1f} volunteer "
                        f"hours, Crossing the {milestone} hours milestone\n\n"
                        f"We wish him to have a wonderful life ahead\n"
                        f"Issued by: Junior Red Cross Society\n"
                        f"Date: {datetime.now().strftime('%Y-%m-%d')}"
                    )
                print(f"🏆 Milestone Reached: Certificate generated: {filename}")
            except FileExistsError:
                pass # already issued for this milestone

def view_volunteer_report():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT name, SUM(hours) as total_hours, COUNT(*) as events "
        "FROM volunteers GROUP BY name ORDER BY total_hours DESC"
    )
    results = cur.fetchall()
    conn.close()

    if not results:
        print("\nNo volunteer records yet. \n")
        return

    print(f"\n{'Name':<20}{'Total hours':<15}{'Events Logged'}")
    print("_" * 50)
    for name, total_hours, events in results:
        print(f"{name:<20}{total_hours:<15.1f}{events}")
    print()

#-------------------------------------------
# MAIN MENU
#-------------------------------------------
def main():
    setup_database()
    menu = """
    ==================================
    RED CROSS VOLUNTEER & DONOR SYSTEM
    ==================================
    1. Add a blood donor
    2. Search donors (by blood group/location)
    3. Log volunteer hours
    4. View volunteer report
    5. Exit
    """
    while True:
            print(menu)
            choice = input("Choos an option (1-5;)").strip()

            if choice == "1":
                add_donor()
            elif choice == "2":
                search_donors()
            elif choice == "3":
                log_volunteer_hours()
            elif choice == "4":
                view_volunteer_report()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("\n Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()
