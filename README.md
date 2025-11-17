# Bus Ticket Reservation System (Python)

This project is a **terminal-based Bus Ticket Reservation System** built in Python. It allows both **Administrators** and **Customers** to manage bus seat bookings, view routes, update fares, and more. The system stores data in text files so the booking state remains persistent even after restarting the program.

---

## 🚍 Features

### **👨‍💼 Administrator Panel**
- View seat plans for all routes
- Remove or unbook seats
- View all available routes and fares
- Change fare for any route
- Change admin passkey

---

### **🧑‍💻 Customer Panel**
- View seat plans
- Book multiple seats at once
- View route and fare list
- Check total fare for selected routes
- View all seats booked under their account

---

## 📁 Data Storage
The system stores data in text files:

- `seats_routeX.txt` → Stores seat status (`1-40` or `x` for booked)
- `customer.txt` → Stores registered users and their booked seats
- `fares.txt` → Stores editable route fares
- `admin_passkey.txt` → Stores admin passcode

---

## 🛣️ Available Routes
| Index | Route |
|-------|------------------|
| 1 | Dhaka → CTG |
| 2 | CTG → Barisal |
| 3 | Dhaka → Sylhet |
| 4 | Dhaka → Dinajpur |

---

## 🎟 Seat Booking System
- Each route contains **40 seats**
- Unbooked seats show their seat number
- Booked seats appear as **`x`**
- Seat plans are displayed in a 2×2 layout per row

Example:
```
[1, 2] [3, 4]
[5, 6] [7, 8]
...
```

---

## 💰 Fare Management
Default fares:
```
Route 1: 800 BDT
Route 2: 1000 BDT
Route 3: 600 BDT
Route 4: 1200 BDT
```
Admins can modify fares, which are saved permanently in `fares.txt`.

---

## 🔐 Authentication System
### **Admin Login**
- Requires a numeric passkey (default: `1234`)

### **Customer Login**
- Usernames & passwords are stored in `customer.txt`
- Customers can register new accounts

---

## 📌 How the Program Works
1. User selects login type: **Admin**, **Customer**, or **Register**
2. Based on login, menu options appear
3. Data is loaded from text files
4. User performs operations (booking, unbooking, fare changes, etc.)
5. Changes are saved immediately to preserve state

---

## ▶️ How to Run
```
python frass8.py
```
Make sure the script is in a writable folder, as it generates and updates data files.

---

## 📦 Files Created Automatically
After first run, the program generates:
- `seats_route1.txt`
- `seats_route2.txt`
- `seats_route3.txt`
- `seats_route4.txt`
- `admin_passkey.txt`
- `fares.txt`
- `customer.txt`

---

## 🛠 Technologies Used
- Python 3
- File handling (`open`, read/write)
- Dictionary-based route and fare management
- Modular functions for seat handling

---

## 🚧 Future Improvements
- Add GUI using Tkinter or PyQt
- Add bus schedules & time slots
- Add payment calculation per booking
- Add automatic merging of customer bookings
- JSON-based storage instead of plain text

---

## 📜 License
This project is open-source and free to use.

---

## 🙌 Author
Developed by **Fardin FW**.

