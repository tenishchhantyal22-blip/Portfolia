#--------------------------------------------------------------------------
# VOLUNTERS FEATURES (Including details like contact information and availability)          
#--------------------------------------------------------------------------

def log_volunteer_hours():
    name = input("Enter volunteer's name: ").strip().upper()
    event = input("Enter events/activities volunteered for: ").strip()
    hours = float(input("Enter number of hours volunteered: ").strip())
    date = input("Enter date of volunteer work (YYYY-MM-DD): ").strip()

    if not date:
        date = datetime.now().strftime("%Y-%m-%d") # Use the current date if no date is provided
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO volunteers (name, event, hours, date)
    VALUES (?, ?, ?, ?)
    """, (name, event, hours, date))

    conn.commit()
    conn.close()
    print(f"\nVolunteer '{name}' has been logged successfully for {hours} hours on {date}. \n")
    check_and_issue_certificate(name, hours, date)

def check_and_issue_certificate(name, hours, date):
    """
    Auto-generate a simple text certificate for volunteers who have successfully completed a milestone of 20, 50, or 100 hours of volunteer work.
     """
     conn = get_connection()
     cur = conn.cursor()
     cur.execute(" SELECT SUM(hours) FROM volunteers WHERE name = ?", (name,))
     total_hours = cur.fetchone()[0] or 0
     conn.close()

     milestones = [20, 50, 1000]
     for milestone in milestones:
        if total_hours >= milestone:
            filename = f"certificate_{name.replace(' ', '_')}_{milestone}_hours.txt"
            # only issue if not already generated (Simply check)
            try:
                with open(filename, "X") as f:
                    f.write(
                                 f"CERTIFICATE OF RECOGBITION\n\n"
                        f"This certifies that {name} has successfully contributed {total_hours:.1f} volunteer "
                        f"hours, Crossing the {milestone} hours milestone\n\n"
                        f"We wish him to have a wonderful life ahead"
                        f"Issued by: Junior Red Cross Society"
                        f"Date: {datetime.now().strftime('%Y-%m-%d')}"
                    )
                print(f"🏆 Milestone Reached: Certificate generated: {filename}")
            except FileExistsError:
                pass # already issued for this milestone

def view_volunteer_report():
    conn = get_connection()
    cur = conn_cursor()
    cur.excecute(
        "SELECT name, SUM(hours as total hours, COUNT(*) as  events)"
        "FROM volunteers GROUP BY name ORDER BY total_hours DESC"
    )
    results = cur.fetchall(c)
    conn.close()

    if not results:
        print("\nNo volunteer records, yes. \n")
        return
    print(f"\n {'Name':<20} {'Total hours':<15.1f} {event}")
    print("_" * 50)
    for name, total_hours, events in results:
        print(f"{name:<20} {total_hours:<15.1f} {event}")
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
                print("Goodbyr!")
                break
            else:
                print("\n Invalid choice, please try again.\n")
            
if __name__ == "_main_":
main()
