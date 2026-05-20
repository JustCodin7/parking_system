import json
import datetime

while True:
    print("<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>")
    print("  Welcome To KZN Smart Mall Parking System")
    print("<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    print("========================================")

    choice = input("Enter choice: ")

    if choice == "1":
        print("--- Login ---")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        try:
            file = open("users.json", "r")
            users = json.load(file)
            file.close()
        except:
            users = []
            print("No users registered yet.")
        found = False
        for user in users:
            if user["username"] == username and user["password"] == password:
                found = True
                logged_in_user = user
                print("Login successful! Welcome", user["name"])

                # CUSTOMER MENU
                if logged_in_user["role"] == "Customer":
                    while True:
                        print("--- Customer Menu ---")
                        print("1. Select Mall & Park Vehicle")
                        print("2. Exit Vehicle")
                        print("3. View My Parking History")
                        print("4. View My Payments")
                        print("5. Update Profile")
                        print("6. Check Current Parking Status")
                        print("7. Logout")
                        customer_choice = input("Enter choice: ")

                        if customer_choice == "1":
                            print("--- Select A Mall ---")
                            print("1. Gateway Theatre (Umhlanga) - R15 flat rate - 250 spaces")
                            print("2. Pavilion (Westville)       - R10 per hour  - 180 spaces")
                            print("3. La Lucia Mall (La Lucia)   - R12 per hour, capped at R60 - 150 spaces")
                            mall_choice = input("Enter your mall choice: ")

                            if mall_choice == "1":
                                selected_mall = "Gateway"
                                print("You have selected Gateway Theatre of Shopping")
                            elif mall_choice == "2":
                                selected_mall = "Pavilion"
                                print("You have selected Pavilion Shopping Centre")
                            elif mall_choice == "3":
                                selected_mall = "La Lucia"
                                print("You have selected La Lucia Mall")
                            else:
                                selected_mall = None
                                print("Invalid mall selection. Please try again.")

                            if selected_mall != None:
                                if selected_mall == "Gateway":
                                    total_capacity = 250
                                elif selected_mall == "Pavilion":
                                    total_capacity = 180
                                elif selected_mall == "La Lucia":
                                    total_capacity = 150

                                try:
                                    file = open("parking.json", "r")
                                    parking_list = json.load(file)
                                    file.close()
                                except:
                                    parking_list = []

                                currently_parked = 0
                                for record in parking_list:
                                    if record["mall"] == selected_mall and record["exit_time"] == None:
                                        currently_parked = currently_parked + 1

                                if currently_parked >= total_capacity:
                                    print("Sorry!", selected_mall, "is full. No spaces available.")
                                else:
                                    plate = input("Enter your vehicle number plate: ")
                                    entry_time = datetime.datetime.now()
                                    entry_time_str = entry_time.strftime("%Y-%m-%d %H:%M:%S")

                                    parking_record = {
                                        "username": logged_in_user["username"],
                                        "mall": selected_mall,
                                        "plate": plate,
                                        "entry_time": entry_time_str,
                                        "exit_time": None,
                                        "fee": None,
                                        "paid": False
                                    }

                                    try:
                                        file = open("parking.json", "r")
                                        parking_list = json.load(file)
                                        file.close()
                                    except:
                                        parking_list = []

                                    parking_list.append(parking_record)
                                    file = open("parking.json", "w")
                                    json.dump(parking_list, file)
                                    file.close()
                                    print("Vehicle", plate, "has entered", selected_mall, "at", entry_time_str)
                                    print("Spaces remaining:", total_capacity - currently_parked - 1)

                        elif customer_choice == "2":
                            print("--- Vehicle Exit ---")
                            plate = input("Enter your vehicle number plate: ")

                            try:
                                file = open("parking.json", "r")
                                parking_list = json.load(file)
                                file.close()
                            except:
                                parking_list = []
                                print("No parking records found.")

                            found_record = None
                            for record in parking_list:
                                if record["plate"] == plate and record["exit_time"] == None:
                                    found_record = record

                            if found_record == None:
                                print("No active parking found for", plate)
                            else:
                                exit_time = datetime.datetime.now()
                                exit_time_str = exit_time.strftime("%Y-%m-%d %H:%M:%S")

                                entry_time = datetime.datetime.strptime(found_record["entry_time"], "%Y-%m-%d %H:%M:%S")
                                duration = exit_time - entry_time
                                total_minutes = duration.seconds // 60
                                total_hours = total_minutes // 60
                                leftover_minutes = total_minutes % 60
                                if leftover_minutes > 0:
                                    total_hours = total_hours + 1

                                if found_record["mall"] == "Gateway":
                                    fee = 15
                                    print("Pricing: Flat Rate")
                                elif found_record["mall"] == "Pavilion":
                                    fee = total_hours * 10
                                    print("Pricing: Hourly Rate")
                                elif found_record["mall"] == "La Lucia":
                                    fee = total_hours * 12
                                    if fee > 60:
                                        fee = 60
                                    print("Pricing: Hourly Rate with Daily Cap")

                                print("Vehicle:", plate)
                                print("Mall:", found_record["mall"])
                                print("Entry Time:", found_record["entry_time"])
                                print("Exit Time:", exit_time_str)
                                print("Duration:", total_minutes, "minutes")
                                print("Amount Due: R", fee)
                                pay = input("Confirm payment? (yes/no): ")

                                if pay == "yes":
                                    found_record["exit_time"] = exit_time_str
                                    found_record["fee"] = fee
                                    found_record["paid"] = True
                                    print("Payment of R", fee, "confirmed! Thank you!")

                                    payment_record = {
                                        "username": logged_in_user["username"],
                                        "mall": found_record["mall"],
                                        "plate": plate,
                                        "fee": fee,
                                        "date": exit_time_str
                                    }
                                    try:
                                        file = open("payments.json", "r")
                                        payments_list = json.load(file)
                                        file.close()
                                    except:
                                        payments_list = []
                                    payments_list.append(payment_record)
                                    file = open("payments.json", "w")
                                    json.dump(payments_list, file)
                                    file.close()
                                else:
                                    print("Payment cancelled. Please pay before leaving.")

                                file = open("parking.json", "w")
                                json.dump(parking_list, file)
                                file.close()

                        elif customer_choice == "3":
                            print("--- My Parking History ---")
                            try:
                                file = open("parking.json", "r")
                                parking_list = json.load(file)
                                file.close()
                            except:
                                parking_list = []

                            my_records = []
                            for record in parking_list:
                                if record["username"] == logged_in_user["username"]:
                                    my_records.append(record)

                            if len(my_records) == 0:
                                print("No parking history found.")
                            else:
                                for record in my_records:
                                    print("========================================")
                                    print("Mall:", record["mall"])
                                    print("Plate:", record["plate"])
                                    print("Entry Time:", record["entry_time"])
                                    print("Exit Time:", record["exit_time"])
                                    print("Fee: R", record["fee"])
                                    print("Paid:", record["paid"])

                        # NEW - View My Payments
                        elif customer_choice == "4":
                            print("--- My Payment History ---")
                            try:
                                file = open("payments.json", "r")
                                payments_list = json.load(file)
                                file.close()
                            except:
                                payments_list = []

                            my_payments = []
                            for payment in payments_list:
                                if payment["username"] == logged_in_user["username"]:
                                    my_payments.append(payment)

                            if len(my_payments) == 0:
                                print("No payments found.")
                            else:
                                for payment in my_payments:
                                    print("========================================")
                                    print("Mall:", payment["mall"])
                                    print("Plate:", payment["plate"])
                                    print("Amount Paid: R", payment["fee"])
                                    print("Date:", payment["date"])

                        elif customer_choice == "5":
                            print("--- Update Profile ---")
                            print("1. Change Name")
                            print("2. Change Surname")
                            print("3. Change Password")
                            update_choice = input("Enter choice: ")

                            if update_choice == "1":
                                new_name = input("Enter new name: ")
                                logged_in_user["name"] = new_name
                            elif update_choice == "2":
                                new_surname = input("Enter new surname: ")
                                logged_in_user["surname"] = new_surname
                            elif update_choice == "3":
                                new_password = input("Enter new password: ")
                                confirm_new = input("Confirm new password: ")
                                if new_password != confirm_new:
                                    print("Passwords do not match. Update cancelled.")
                                else:
                                    logged_in_user["password"] = new_password
                            else:
                                print("Invalid choice.")

                            try:
                                file = open("users.json", "r")
                                users = json.load(file)
                                file.close()
                            except:
                                users = []

                            for i in range(len(users)):
                                if users[i]["username"] == logged_in_user["username"]:
                                    users[i] = logged_in_user

                            file = open("users.json", "w")
                            json.dump(users, file)
                            file.close()
                            print("Profile updated successfully!")

                        elif customer_choice == "6":
                            print("--- Current Parking Status ---")
                            try:
                                file = open("parking.json", "r")
                                parking_list = json.load(file)
                                file.close()
                            except:
                                parking_list = []

                            active = False
                            for record in parking_list:
                                if record["username"] == logged_in_user["username"] and record["exit_time"] == None:
                                    active = True
                                    print("You currently have a vehicle parked!")
                                    print("Mall:", record["mall"])
                                    print("Plate:", record["plate"])
                                    print("Entry Time:", record["entry_time"])

                            if active == False:
                                print("You have no vehicle currently parked.")

                        elif customer_choice == "7":
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please try again.")

                # ADMIN MENU
                elif logged_in_user["role"] == "Admin":
                    while True:
                        print("--- Admin Menu:", logged_in_user["mall"], "---")
                        print("1. View Parked Vehicles")
                        print("2. Monitor Capacity")
                        print("3. View Daily Activity")
                        print("4. Logout")
                        admin_choice = input("Enter choice: ")

                        if admin_choice == "1":
                            print("--- Vehicles Currently Parked At", logged_in_user["mall"], "---")
                            try:
                                file = open("parking.json", "r")
                                parking_list = json.load(file)
                                file.close()
                            except:
                                parking_list = []

                            count = 0
                            for record in parking_list:
                                if record["mall"] == logged_in_user["mall"] and record["exit_time"] == None:
                                    count = count + 1
                                    print("========================================")
                                    print("Plate:", record["plate"])
                                    print("Entry Time:", record["entry_time"])
                                    print("Username:", record["username"])

                            if count == 0:
                                print("No vehicles currently parked.")
                            else:
                                print("========================================")
                                print("Total vehicles parked:", count)

                        elif admin_choice == "2":
                            print("--- Capacity Monitor:", logged_in_user["mall"], "---")
                            try:
                                file = open("parking.json", "r")
                                parking_list = json.load(file)
                                file.close()
                            except:
                                parking_list = []

                            if logged_in_user["mall"] == "Gateway":
                                total_capacity = 250
                            elif logged_in_user["mall"] == "Pavilion":
                                total_capacity = 180
                            elif logged_in_user["mall"] == "La Lucia":
                                total_capacity = 150

                            currently_parked = 0
                            for record in parking_list:
                                if record["mall"] == logged_in_user["mall"] and record["exit_time"] == None:
                                    currently_parked = currently_parked + 1

                            spaces_left = total_capacity - currently_parked
                            print("Total Capacity:", total_capacity)
                            print("Currently Parked:", currently_parked)
                            print("Spaces Available:", spaces_left)

                        elif admin_choice == "3":
                            print("--- Daily Activity:", logged_in_user["mall"], "---")
                            today = datetime.datetime.now().strftime("%Y-%m-%d")
                            try:
                                file = open("parking.json", "r")
                                parking_list = json.load(file)
                                file.close()
                            except:
                                parking_list = []

                            daily_count = 0
                            daily_revenue = 0
                            for record in parking_list:
                                if record["mall"] == logged_in_user["mall"] and record["entry_time"].startswith(today):
                                    daily_count = daily_count + 1
                                    if record["fee"] != None:
                                        daily_revenue = daily_revenue + record["fee"]
                                    print("========================================")
                                    print("Plate:", record["plate"])
                                    print("Entry Time:", record["entry_time"])
                                    print("Exit Time:", record["exit_time"])
                                    print("Fee: R", record["fee"])
                                    print("Paid:", record["paid"])

                            if daily_count == 0:
                                print("No activity today.")
                            else:
                                print("========================================")
                                print("Total vehicles today:", daily_count)
                                print("Total revenue today: R", daily_revenue)

                        elif admin_choice == "4":
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please try again.")

                # OWNER MENU
                elif logged_in_user["role"] == "Owner":
                    while True:
                        print("--- Owner Menu ---")
                        print("1. View All Malls Report")
                        print("2. Compare Malls")
                        print("3. Logout")
                        owner_choice = input("Enter choice: ")

                        if owner_choice == "1":
                            print("--- All Malls Report ---")
                            try:
                                file = open("parking.json", "r")
                                parking_list = json.load(file)
                                file.close()
                            except:
                                parking_list = []

                            for mall_name in ["Gateway", "Pavilion", "La Lucia"]:
                                total_vehicles = 0
                                total_revenue = 0
                                total_duration = 0
                                completed = 0

                                for record in parking_list:
                                    if record["mall"] == mall_name:
                                        total_vehicles = total_vehicles + 1
                                        if record["fee"] != None:
                                            total_revenue = total_revenue + record["fee"]
                                        if record["exit_time"] != None and record["entry_time"] != None:
                                            entry = datetime.datetime.strptime(record["entry_time"], "%Y-%m-%d %H:%M:%S")
                                            exit = datetime.datetime.strptime(record["exit_time"], "%Y-%m-%d %H:%M:%S")
                                            duration = exit - entry
                                            total_duration = total_duration + duration.seconds // 60
                                            completed = completed + 1

                                if completed > 0:
                                    average_duration = total_duration // completed
                                else:
                                    average_duration = 0

                                print("========================================")
                                print("Mall:", mall_name)
                                print("Total Vehicles:", total_vehicles)
                                print("Total Revenue: R", total_revenue)
                                print("Average Parking Duration:", average_duration, "minutes")

                        elif owner_choice == "2":
                            print("--- Mall Comparison ---")
                            try:
                                file = open("parking.json", "r")
                                parking_list = json.load(file)
                                file.close()
                            except:
                                parking_list = []

                            print("==================================================")
                            print("Mall           | Vehicles | Revenue | Avg Duration")
                            print("==================================================")

                            for mall_name in ["Gateway", "Pavilion", "La Lucia"]:
                                total_vehicles = 0
                                total_revenue = 0
                                total_duration = 0
                                completed = 0

                                for record in parking_list:
                                    if record["mall"] == mall_name:
                                        total_vehicles = total_vehicles + 1
                                        if record["fee"] != None:
                                            total_revenue = total_revenue + record["fee"]
                                        if record["exit_time"] != None and record["entry_time"] != None:
                                            entry = datetime.datetime.strptime(record["entry_time"], "%Y-%m-%d %H:%M:%S")
                                            exit = datetime.datetime.strptime(record["exit_time"], "%Y-%m-%d %H:%M:%S")
                                            duration = exit - entry
                                            total_duration = total_duration + duration.seconds // 60
                                            completed = completed + 1

                                if completed > 0:
                                    average_duration = total_duration // completed
                                else:
                                    average_duration = 0

                                print(mall_name, "        |", total_vehicles, "        | R", total_revenue, "   |", average_duration, "mins")

                        elif owner_choice == "3":
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please try again.")

        if found == False:
            print("Invalid username or password.")

    elif choice == "2":
        print("--- Register ---")
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")

        if password != confirm_password:
            print("Passwords do not match. Registration cancelled.")
        else:
            print("Select Your Role:")
            print("1. Customer")
            print("2. Admin")
            print("3. Owner")
            role_choice = input("Enter your role choice: ")

            if role_choice == "1":
                role = "Customer"
                admin_mall = None
            elif role_choice == "2":
                role = "Admin"
                print("Select your mall:")
                print("1. Gateway Theatre")
                print("2. Pavilion")
                print("3. La Lucia Mall")
                mall_choice = input("Enter mall choice: ")
                if mall_choice == "1":
                    admin_mall = "Gateway"
                elif mall_choice == "2":
                    admin_mall = "Pavilion"
                elif mall_choice == "3":
                    admin_mall = "La Lucia"
                else:
                    admin_mall = None
                    print("Invalid mall selection.")
            elif role_choice == "3":
                role = "Owner"
                admin_mall = None
            else:
                role = None
                admin_mall = None
                print("Invalid role. Registration cancelled.")

            if role != None:
                try:
                    file = open("users.json", "r")
                    users = json.load(file)
                    file.close()
                except:
                    users = []

                username_taken = False
                for user in users:
                    if user["username"] == username:
                        username_taken = True
                        print("Username already taken. Please try again.")

                if username_taken == False:
                    new_user = {
                        "name": name,
                        "surname": surname,
                        "username": username,
                        "password": password,
                        "role": role,
                        "mall": admin_mall
                    }
                    users.append(new_user)
                    file = open("users.json", "w")
                    json.dump(users, file)
                    file.close()
                    print("Registration successful! Welcome", name)

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")