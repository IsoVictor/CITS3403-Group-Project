# CITS3403-Group-Project
Group Project for Agile Web Development 

# Study Forums App

Welcome to the Study Forum App! This Flask application helps users organize and manage their study sessions effectively, allowing students to create study groups and post questions which can then be joined or answered by other students. 

# Group Information

| UWA ID       | Name              | GitHub Username         |
|--------------|-------------------|-------------------------|
| 23380426     | Victor Iso        | IsoVictor               |
| 23358213     | Rohnan Klifunis   | RohnanK/Rohnan Klifunis |
| 23374296     | Jason Nguyen      | Jasonnguyxn             |
| 23043141     | Nguyen Le Cam Anh | ann250902               |

## Launch Guide

To launch this Flask application, follow these steps:

### 1. Set up your environment:

- **Ensure Python is installed on your system.**

  Make sure you have Python installed on your system. You can download and install Python from the official website: [Python.org](https://www.python.org/).

- **Optionally, activate a virtual environment to best manage dependencies:**
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  
### 2. Install dependencies
- **Install all required packages from the requirements.txt file:**
  ```bash
  pip install -r requirements.txt

### 3. Set environment variables
- **Specify the environment and debug mode:**
  ```bash
  export FLASK_APP=run.py      # On Windows use `set FLASK_APP=run.py`
  export SECRET_KEY=secret_key_i_gave_you

### 4. Initialise Database with Test data
- **Optional but you can import test data in the shell**
  ```bash
  flask db upgrade
  flask shell
  >>> import app.test_data

### 5. Run the application
- **Start the Flask server:**
  ```bash
  flask run

## Test Guide
### 1. Unit Tests
- **To run the unit tests for our code:**
  ```bash
  python -m unittest Tests/unit.py

### 2. Selenium Tests
- **To run the selinium tests for our code:**
  ```bash
  python -m unittest Tests/selenium.py
