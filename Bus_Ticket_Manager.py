import os

route = {
    1: "Dhaka-CTG",
    2: "CTG-Barisal",
    3: "Dhaka-Sylhet",
    4: "Dhaka-Dinajpur"
}


def seat_filename(route_id):
    return f"seats_route{route_id}.txt"

def load_seats(val):
    fname = seat_filename(val)

    if os.path.exists(fname):
            try:
                with open(fname, "r") as f:
                    content = f.read().strip()
                    if not content:
                        raise ValueError
                    parts = content.split(",")
                    return [p if p =='x' else int(p) for p in parts]
            except Exception:
                print("Error in the seat plan, Loading seat plan again")
            
    return list(range(1,41))


def saveseats(arr,id):
    fname = seat_filename(id)
    with open(fname, "w") as f:
        f.write(",".join(str(x) for x in arr))

def seatPlan(arr):
        for i in range(0, 40, 2):
            print(f"[{arr[i]}, {arr[i+1]}]", end=" ")
            if((i+2)%4 == 0):
                print()
        print()


def positionfree(seatNo, arr):
    return arr[seatNo-1] != 'x'


def book(seatNo, arr, id):
    while True:
        if not (1 <= seatNo <= len(arr)):
            print("Invalid seat number.")
        elif positionfree(seatNo, arr):
            arr[seatNo - 1] = 'x'
            saveseats(arr,id)
            return
        else:
            print("Seat taken, choose a different seat!")

            try:
                seatNo = int(input("Enter seat: ").strip())
            except ValueError:
                print("Please enter a valid integer.")


def remove(seatNo, arr, id):
    while True:
        if not (1 <= seatNo <= len(arr)):
            print("Invalid seat number.")
            continue
        elif positionfree(seatNo, arr):
            arr[seatNo - 1] = 'x'
            saveseats(arr,id)
            return
        else:
            return



def unbook(seatNo, arr, id):
    if arr[seatNo-1] == 'x':
        arr[seatNo-1] = seatNo
        saveseats(arr, id)
        print(f"Seat {seatNo} freed")

        if os.path.exists("customer.txt"):
            lines = []
            with open("customer.txt", "r") as f:
                for line in f:
                    if "Username:" not in line:
                        lines.append(line)
                        continue
                    name , rid_str, seats_str = line.strip().split(",", 2)
                    rid = int(rid_str.split(":")[1].strip())
                    if rid != id:
                        lines.append(line)
                        continue
                    seats_list = seats_str.split(":")[1].strip().strip("[]")
                    booked_seats = [int(s) for s in seats_list.replace(","," ").split() if s.isdigit()]
                    if seatNo in booked_seats:
                        booked_seats.remove(seatNo)
                    if booked_seats:
                        new_line = f"{name}, {rid_str}, Seat: {booked_seats}\n"
                        lines.append(new_line)
            
            with open("customer.txt","w") as f:
                f.writelines(lines)

    else:
        print(f"Seat {seatNo} is already free")




def myfare(username, routes):
    fare_total = 0
    last_line = None
    if os.path.exists("customer.txt"):
        with open("customer.txt", "r") as f:
            for route in routes:
                for line in f:
                    if "Username:" not in line: 
                        continue
                    name, rid, seats = line.strip().split(",", 2)
                    rid = int(rid.split(":")[1].strip())
                    name = name.split(":")[1].strip()
                    if name == username and rid == route:
                        last_line = line
        
        
        
                if last_line:
                    name, rid, seats = last_line.strip().split(",", 2)
                    name = name.split(":")[1].strip()
                    rid = int(rid.split(":")[1].strip())
                    seats = seats.split(":")[1].strip().strip("[]")
                    seat_numbers = [s.strip() for s in seats.replace(",", " ").split() if s.strip().isdigit()]
                    seat_count = len(seat_numbers)
                    cost = load_fare(rid)
                    fare_total += cost * seat_count
                    print(f"\nFare on route {route}: {seat_count}*{cost} = {fare_total} BDT")

        print("\nTotal Fare: ",fare_total,"BDT")
    return fare_total



def myseats(username,routes):
    last_line = None
    if os.path.exists("customer.txt"):
        for route in routes:
            with open("customer.txt", "r") as f:
                last_line = None
                for line in f:
                    if "Username:" not in line: 
                        continue
                    name, rid, seats = line.strip().split(",", 2)
                    rid = int(rid.split(":")[1].strip())
                    name = name.split(":")[1].strip()
                    if name == username and rid == route:
                        last_line = line        
        
                if last_line:
                    name, rid, seats = last_line.strip().split(",", 2)
                    name = name.split(":")[1].strip()
                    rid = int(rid.split(":")[1].strip())
                    seats = seats.split(":")[1].strip().strip("[]")
                    seat_numbers = [s.strip() for s in seats.replace(",", " ").split() if s.strip().isdigit()]
                    print(f"Seats in route {route}: are {seat_numbers}")



def seat_per_customer(rid, new_seats, username):
    lines = []
    updated = False

    if os.path.exists("customer.txt"):
        with open("customer.txt", "r") as f:
            for line in f:
                if "Username:" in line:
                    name_part, rid_part, seat_part = line.strip().split(",", 2)

                    name = name_part.split(":")[1].strip()
                    route_id = int(rid_part.split(":")[1].strip())

                    if name == username and route_id == rid:
                        old_seats_str = seat_part.split(":")[1].strip().strip("[]")
                        old_seats = [int(s) for s in old_seats_str.replace(",", " ").split() if s.isdigit()]

                        merged = sorted(set(old_seats + new_seats))

                        new_line = f"Username: {username}, Route: {rid}, Seat: {merged}\n"
                        lines.append(new_line)
                        updated = True
                        continue

                lines.append(line)

    if not updated:
        lines.append(f"Username: {username}, Route: {rid}, Seat: {new_seats}\n")

    with open("customer.txt", "w") as f:
        f.writelines(lines)



def fare(id):
    routename = route.get(id)
    if not routename:
        raise ValueError("Invalid Route")
    print(f"Route: {routename}")
    print(f"Fare: {load_fare(id)}")



def showroute():
    for key,value in route.items():
        print(f"{key}: {value}")


FARES = "fares.txt"


def showfare():
    fare = load_all_fares()
    print(f"Dhaka-CTG: {fare[0]}\nCTG-Barisal: {fare[1]}\nDhaka-Sylhet: {fare[2]}\nDhaka-Dinajpur: {fare[3]}\n")


def load_fare(id):
    if os.path.exists(FARES):
        with open(FARES, "r") as f:
            line = f.read().strip()
            if line:
               fare_list = [int(x) for x in line.split(",")]
               if 1 <= id <= len(fare_list):
                    return fare_list[id - 1] 
    return fares[id]


def load_all_fares():
    if os.path.exists(FARES):
        with open(FARES, "r") as f:
            line = f.read().strip()
            if line:
                return [int(x) for x in line.split(",")]
    return [fares[1], fares[2], fares[3], fares[4]]



def save_fare(fare_list):
    with open(FARES, "w") as f:
        f.write(",".join(str(x) for x in fare_list))


fares = {
    1: 800,
    2: 1000,
    3: 600,
    4: 1200
}



def change_fare():
    showroute()
    try:
        rid = int(input("\nSelect route to change fare (1-4): ").strip())
        if 1 <= rid <= 4:
            new_fare = int(input(f"Enter new fare for {route[rid]}: ").strip())
            fare_list = load_all_fares()
            fare_list[rid - 1] = new_fare
            save_fare(fare_list)
            print(f"Fare updated for {route[rid]} to {new_fare}")
        else:
            print("Invalid route index.")
    except ValueError:
        print("Invalid input.")



def load_customers():
    customer = {}
    if os.path.exists("customer.txt"):
        with open("customer.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) == 2:
                    username, password = parts
                    customer[username.strip()] = password.strip()
    return customer




def register_customer():
    customers = load_customers()
    username = str(input("\n\tEnter Username: ").strip())
    for username in customers:
        print("Username already taken, Choose a different username")
        return
    password = str(input("\tCreate a password: "))
    with open("customer.txt", "a") as f:
        f.write(f"{username},{password}\n")
        print("\nRegistration succesful!\n")
    


def customer_login():
    global current_username
    customers = load_customers()
    if os.path.exists("customer.txt"):
        for i in range(3):
            username = str(input("\n\tEnter username: ").strip())
            password = str(input("\tEnter password: ").strip())
            if username in customers and customers[username] == password:
                current_username = username
                return True
            else:
                print("\nWrong username or password!\nTry again")
                print(f"{2-i} more attempts left")

        print("Log in failed 3 times!\n")
    return False



PASSKEY_FILE = "admin_passkey.txt"

def load_passkey():
    if os.path.exists(PASSKEY_FILE):
        with open(PASSKEY_FILE, "r") as f:
            return int(f.read().strip())
    return 1234 #default

def save_passkey(newkey):
    with open(PASSKEY_FILE, "w") as f:
        f.write(str(newkey))




def main1():
    print("\n\t----------Welcome Admin----------\n")
    arr1 = load_seats(1)
    arr2 = load_seats(2)
    arr3 = load_seats(3)
    arr4 = load_seats(4)

    seats = {
    1: arr1,
    2: arr2,
    3: arr3,
    4: arr4,
  }

    while True:
        print("\n\t\t--- Services ---\n")
        print("\t\t1. Show seat plan")
        print("\t\t2. Change seat plan")
        print("\t\t3. Show route & fare")
        print("\t\t4. Change route fares")
        print("\t\t5. Change passkey")
        print("\t\t6. Exit")

        choice = int(input("\nSelect an option: ").strip())
        print()
    
        if choice == 1:
            showroute()
            while True:
                try:
                    val = int(input("\nEnter Route index (1-4): ").strip())
                    print()
                    if 1 <= val <= 4:
                        break
                    else:
                        print("\nRoute must be between 1 and 4.")
                except ValueError:
                    print("\nEnter a valid index.")
            
            container = seats.get(val)
            print()
            seatPlan(container)

            print("\n")


        elif choice == 2:
            showroute()
            while True:
                try:
                    val = int(input("\nEnter Route index (1-4): ").strip())
                    print()
                    if 1 <= val <= 4:
                        break
                    else:
                        print("\nRoute must be between 1 and 4.")
                except ValueError:
                    print("Enter a valid index.")

            container = seats.get(val)
            seatPlan(container)
            print("1. Remove Seat\n2. Unbook Seat\n")
            select = int(input("\nSelect option to perform changes: ").strip())
            if select == 1:
                while True:
                    try:
                        seatNo = input("\nSelect your seats to remove: ").strip()
                        seatnumbers = [int(s.strip()) for s in seatNo.split(",")]
                        invalid_seats = [s for s in seatnumbers if not (1 <= s <= len(container))]
                        if invalid_seats:
                            print("Invalid seat numbers.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input")

                container = seats.get(val)
                for seat in seatnumbers:
                    remove(seat, container,val)
                print("Seat(s) removed!")
                print("\n")
            if select == 2:
                while True:
                    try:
                        seatNo = input("Select your seats to unbook: ").strip()
                        seatnumbers = [int(s.strip()) for s in seatNo.split(",")]
                        invalid_seats = [s for s in seatnumbers if not (1 <= s <= len(container))]
                        if invalid_seats:
                            print("Invalid seat numbers.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input")

                container = seats.get(val)
                for seat in seatnumbers:
                    unbook(seat, container,val)
                print("Seat(s) unbooked!")
                print("\n")


        elif choice == 3:
            showroute()
            print("\n")
            showfare()

        elif choice == 4:
            print(load_all_fares())
            print()
            change_fare()
        
        elif choice == 5:
            for i in range(3):
                val = int(input("\nEnter current passkey: "))
                key = load_passkey()
                if val == key:
                    newkey = int(input("\nEnter new Passkey: ").strip())
                    save_passkey(newkey)
                    key = newkey
                    print("Passkey updated successfully!")
                    return
                else:
                    print("Wrong Passkey. Try again\n")
                    print(f"{2-i} more attempts left")


        elif choice == 6:
            print("Changes completed.\nExiting......")
            break
        else:
            print("Invalid option. Select again")
            continue





def main2():
    print(f"\n\t----------Welcome, {current_username}!----------\n")
    arr1 = load_seats(1)
    arr2 = load_seats(2)
    arr3 = load_seats(3)
    arr4 = load_seats(4)

    seats = {
    1: arr1,
    2: arr2,
    3: arr3,
    4: arr4,
  }

    while True:
        print("\t\t--- Services ---\n")
        print("\t\t1. Show seat plan")
        print("\t\t2. Book a seat")
        print("\t\t3. Show route & fare")
        print("\t\t4. Show my total fare")
        print("\t\t5. Show my seats")
        print("\t\t6. Exit")

        choice = int(input("\nSelect an option: ").strip())
        print()
        
        if choice == 1:
            showroute()
            while True:
                try:
                    val = int(input("\nEnter Route index (1-4): ").strip())
                    print()
                    if 1 <= val <= 4:
                        break
                    else:
                        print("\nRoute must be between 1 and 4.")
                except ValueError:
                    print("Enter a valid index.")
            
            container = seats.get(val)
            print()
            seatPlan(container)

            print("\n")


        elif choice == 2:
            showroute()
            while True:
                try:
                    val = int(input("\nEnter Route index (1-4): ").strip())
                    print()
                    if 1 <= val <= 4:
                        break
                    else:
                        print("\nRoute must be between 1 and 4.")
                except ValueError:
                    print("Enter a valid index.")

            container = seats.get(val)
            seatPlan(container)
            while True:
                try:
                    seatNo = input("\nSelect your desired seats to reserve: ").strip()
                    seatnumbers = [int(s.strip()) for s in seatNo.split(",")]
                    invalid_seats = [s for s in seatnumbers if not (1 <= s <= len(container))]
                    if invalid_seats:
                        print("Invalid seat numbers.")
                        continue
                    break
                except ValueError:
                    print("Invalid input")

            container = seats.get(val)
            for seat in seatnumbers:
                book(seat, container, val)

            seat_per_customer(val, seatnumbers, current_username)
            print("Seat(s) Booked!")
            print("\n")

        elif choice == 3:
            showroute()
            print("\n")
            showfare()

        elif choice == 4:
            showroute()

            val = input("\nEnter Route index: ")
            print()
            val_list = [int(s) for s in val.replace(","," ").split() if s.isdigit()]
            myfare(current_username, val_list)
            print()
            print()
        
        elif choice == 5:
            routes = [1,2,3,4]
            myseats(current_username,routes)
        elif choice == 6:
            print("Reserving seat completed.\nExiting......")
            break
        else:
            print("Invalid option. Select again")
            continue

 


print("\n\n\t-------------------------------------------------")
print("\t\tWelcome to GREEN TRANSPORT AGENCY")
print("\t-------------------------------------------------\n\n")

while True:
	try:
		log = int(input("\tSelect login option: \n\n\t1. Administrator\n\t2. Customer\n\t3. Register new account\n\nChoose option: ").strip())
	except ValueError:
		print("Please enter a valid integer option.\n")
		continue

	if log == 1:
		while True:
			try:
				passkey = int(input("\n\tEnter Passkey to log in: ").strip())
				key = load_passkey()
				if passkey == key:
					print("\n\tLogin successful!\n")
					main1()
					break
				else:
					print("Wrong passkey. Try again.")
			except ValueError:
				print("\nEnter a valid integer passkey.")
			continue

	elif log == 2:
		while True:
			login_success = customer_login()
			if login_success:
				main2()
				break
			else:
				print("\nNo account found or login failed. Please register first.")
				register_customer()

	elif log == 3:
		register_customer()

	else:
		print("Invalid option. Please enter 1, 2 or 3.\n")

