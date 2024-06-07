# Capstone_project_trestle_academy
## Data Ingestion project
### Project Title:
"Real-Time Weather Data Ingestion and Processing Pipeline"

### Project Overview:
The goal of this project is to develop a data ingestion pipeline that fetches real-time weather data from a public API, and stores it in a database for further analysis and visualization.

### Scope and Objectives:
Data Source:  public weather API (OpenWeatherMap API).<br>
Tools and Technologies: Python, Airflow, PostgreSQL, Docker, Pandas.<br>
Objectives:
Fetch real-time weather data at regular intervals.
Store the data in a PostgreSQL database.
Set up a monitoring and error handling system to ensure data quality and pipeline reliability.

### Project Implementation:
Data Source:
Sign up for an API key from OpenWeatherMap.
Identify the endpoints and parameters needed to fetch the weather data.
Data Ingestion:<br>
1.the jupyter notebook 'Python_script' test the API to fetch data from the openweathermap.
2. The docker-compose file creates a container for the project using airflow and postgres image
3. The weather_data_injection_retrieval python code runs on airflow to collect weather data from London every one hour and form 7/6/2024<br>

Data Storage:<br>
The data is then stored in postgres database by creating a connection in airflow
Monitoring and Logging:<br>
Airflow alerts and email alert for pipeline failures are added to the weather_data_injection_retrieval python code.
