# Bloodpy (Blood Bank Management System )

An app to do blood bank management (used by hospital to maintain the record of blood unit), serve donations and blood requests

Tkinter + Mysql

- [ ] Track the availability of different blood types in real-time
- [ ] management of blood donors (registration, donation history, scheduling for future donations)
- [ ] hospital can request for specific blood type and track the status of their request efficiently

- [ ] Track donor details, blood inventory and transaction record in the db


- [ ] The system should fetch all the records from the BloodBank table and displaying the same on the screen using mysql connector.

- [ ] The entries consist of blood group, the units of blood available of the particular blood group, and two tkinter buttons to perform the functionalities (donate, and request) and as per user requirement.

- [ ] The user to enter the required blood group and amount using the Tkinter entry widget and then it offers a submit button to call the request_dbase() method which checks availability and updates data correspondingly.

- [ ] Connects with the database and checks if the asked amount of blood is available or not. If not, it displays the required message. Otherwise, it completes the request and reduces the units of the particular blood group in the database, and flashes the corresponding message box.

- [ ] Two methods (donate and donate_dbase) just increase the units of blood donated by the user

## Features

- The admin login 
- Homepage display blood groups and unit with donate and request options. 
- Register Donors with their blood groups 
- Blood request button to enter the units of blood required with date 
- Donate blood button to enter blood group to donate with date 
- Blood donation history 
- Logout
