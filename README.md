# Library Management System

### Table of Content
- Overview
- Software Dependencies
- Data flow diagram
- Installation
- Setup the program
- Demo 
  

## Overview
The library management system software makes the library a smart one by organizing the books systematically by author, title and subject. This enables users to search for books quickly and effortlessly.This a simple Library Management System with  APIs to manage users, books, book details, and borrowed books. Leveraging the FastAPI framework, the system offers a scalable and efficient solution, allowing users to create and retrieve information about library resources, track book details, and manage borrowing transactions. The application is equipped with Swagger documentation for easy API exploration, making it accessible for both developers and end-users.

### Software Dependencies
- Python
- Postgresql
- FastAPI
- SQLAlchemy

### Data Flow Diagram
![alt text](<Screenshot from 2024-02-02 21-26-13.png>)

### Installation
1. Clone the repository 
```
git clone https://github.com/Ashoktripathi13/Library_management_system.git
```
2. Create a virtual environment.
```
python3 -m venv venv
```
3. Activate the Virtual environment.
for linux:
```
source  venv/bin/activate
```
4. Install the required dependencies.

```
pip install -r requirements.txt
```

### Setup the program 

1. configure the database(Here the postgresql is used ):
   - open the `database.py` file and adjust the databse connection settings as needed.
```
driver://username:password@host:port/database_name
```

2. Run  `main.py`  file using:

`uvicorn main:app --reload`


3.  Visit the Swagger documentation:
Open your browser and navigate to `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)` to view the Swagger documentation.

### Demo 

![alt text](<Screenshot from 2024-02-02 19-02-24.png>)

![alt text](<Screenshot from 2024-02-02 19-25-09.png>)



