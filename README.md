# NurseEase
NurseEase is an application that was built by students of TH Deggendorf. The aim of the application was to enhance patient care and reducing the workload of nurses by providing real time vital signs updates and emergency alerts.

This application is built with FastAPI and Plotly to automate the reading of vital signs and visualize them in a graph in real-time. The app generates random vital sign data with Faker library for demonstration purposes and saves patient information as FHIR resources ensuring interoperability in healthcare. 

## Technologies
### Frontend
- HTML5, CSS3 And JavaScript
- jQuery and AJAX

### Backend
- Python 
- FASTAPI
- PostgreSQL

## Features
- Automatic vital signs reading
- Graph of current vital signs and the overall trend
- Real-time graph visualization using Plotly and AJAX calls
- FHIR Resources are used to ensure interoperability
- Authentication and Email verification

## Installation
### Method 1:
1. Clone the repository:
<pre>
git clone https://github.com/Aswath1999/NurseEase.git
</pre>
2. Activate virtual environment and install the required dependencies
<pre>
pip install -r requirements.txt
</pre>
3. Save the necessary environment variables. The app requires DATABASE_URL, MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER and SECRET_KEY to function properly. 

4. Run the application 
<pre>
uvicorn main:app --reload
</pre>

### Method 2: Docker installation
1. After cloning the repository and setting the environment variables, you can run the application with the command
<pre>
docker compose up
</pre>

## App Demo:
You can checkout the app demo at https://nurseease.onrender.com. You can use the username: Nurseease2023 and password: Nurseease2023@ to login or you can create a new account using your email address.

## Collobarators 
- Adwitiya https://github.com/Aboruahcode

## Licensing 
MIT