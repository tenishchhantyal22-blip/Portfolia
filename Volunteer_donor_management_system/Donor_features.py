# Including features/details about donors, donations, campaigns, and volunteers. 

def add_donor():
    """ add details about donor if he/she is new in database """
    name = input("Enter donr's name: ").strip().upper()
    blood_type = input("Enter donor's blood type (e.g A+, B+ O+, A-): ").strip().upper()
    phone = input("Enter donor's phone number: ").strip()
    location = input("Enter donor's location: ").strip()
    last_donation_date = input("Enter donor's last date of donation (YYYY-MM-DD) and leave blank if never donated: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO donors (name, blood_type, phone, location, last_donation_date)
    VALUES (?, ?, ?, ?, ?),
    (name, blood_type, phone, location, last_donation_date or none),
    """)
    conn.commit()
    conn.close()
    print(f"\nDonor '{name}' has been added successfully to the database. \n")

def search_donor():
    """ searching for a donor in the database by blood type and location """
    blood_type = input("Enter donor's blood type (e.g A+, B+, O-, A-): ").strip().upper()
    location = input("Enter donor's location ane leave blank if you want to search by blood type only: ").strip()
    query = "SELECT id, name, blood_type, phone, location, last_donation_date FROM donors WHERE 1=1"
    params = []

    if blood_type:
        query += "AND blood_type = ?"
        params.append(blood_type)

    if location:
        query += "AND location LIKE ?"
        params.append(f"%{location}%")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    con.close()

    if not results:
        print("\nNo donors found matching to those details and criteria \n")
        return

    print(f"\n{'ID': <5} {'Name': <20} ('Group': <10} {'Phone': <15} {'Location': <20} {'Last Donation Date': <15} {'Eligible now to donate blood?'}")

    print("_" * 100)
    for row in results:
        donor_id, name, blood_type, phone, location, last_donation_date = row
        eligible = is_eligible_to_donate(last_donation_date)
        print(f"{donor_id: <5} {name: <20} {blood_type: <10} {phone: <15} {location: <20} {last_donation_date: <15} {'Yes' if eligible else 'No'}")
    print()
 
