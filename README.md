# To-Do List Application

## Project Overview
This project is a To-Do List app that allows users to create, edit, and manage tasks, with an integrated weather check feature. 
For each task, users can retrieve weather information for a specific location, making it easier to plan tasks according to current weather conditions.

## Features

-app.py - Backend Flask server handling task CRUD operations and weather data retrieval from WeatherAPI.
-/templates - HTML templates for rendering frontend content.
-/static - Static assets, such as CSS files.
-/src - Contains React components for the frontend:
-TaskForm.js: Allows task creation and editing.
-TaskList.js: Displays all tasks and options to edit, delete, complete, or view weather for each task.
-WeatherPage.js: Shows weather information for a selected task location.
-tasks.db - SQLite database for storing tasks (will be auto-generated).
-package.json - Lists frontend dependencies for the React app.
-requirements.txt - Lists backend dependencies for the Flask server.

## Tech Stack
-Frontend: React, Axios, Bootstrap
-Backend: Python (Flask, Flask-CORS, Flask-SQLAlchemy)
-Database: SQLite
-API Integration: WeatherAPI for fetching real-time weather data


### API:
- The API being used for weather data in this project is the WeatherAPI (https://www.weatherapi.com/). 
This external service provides current weather information based on latitude and longitude coordinates.

### Other Technologies:
- **JWT (JSON Web Token)**: For user authentication.
- **Mongoose**: For MongoDB object modeling.
- **Axios**: For handling HTTP requests, especially for fetching external API data.

## Installation
To run this project locally, follow these steps:

### Prerequisites
-Prerequisites
-Python 3.x
-Node.js and npm
-Internet connection to fetch weather data

### Steps:
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Jeremias686/To_Do_List.git
Hello world, How are you doing 
2. Backend Setup
-Navigate to the project directory.
-Install required backend dependencies
-pip install -r requirements.txt
-Ensure the WeatherAPI key is correctly 
set in app.py under API_KEY.
2.In the project root or src folder (where package.json is located), 
install the frontend dependencies: npm install
### Runing the Application 
1.Start the Backend Server
-Run the backend server by executing: python app.py
-This will initialize tasks.db if it doesn't already exist
2.Start the Frontend Server
-In the frontend directory, run: npm start
-This will start the React app on the defualt port:(http://localhost:3000)
3.Usage
-Open the application in your browser and start adding tasks.
-For each task, you can:
-Mark it as complete/incomplete.
-Edit or delete the task.
-Check the weather for the task’s location.
Note: Make sure to enter latitude and longitude in WeatherPage.js 
for each task’s location to get accurate weather data.
