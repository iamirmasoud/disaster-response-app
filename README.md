# Disaster Response Pipeline Project

### Project Description:

In this project, I built ETL and machine learning pipelines that is capable to curate the class of the messages. The pipeline is eventually built into a flask application. The project include a web app where an emergency worker can input a new message and get classification results in several categories (Multi-Label Classification). The landing page of the webapp also includes four visualizations of the training dataset built with plotly.

### File Descriptions:
The project contains the following files,

* ETL Pipeline Preparation.ipynb: Notebook experiment for the ETL pipelines
* ML Pipeline Preparation.ipynb: Notebook experiment for the machine learning pipelines
* data/process_data.py: The ETL pipeline used to process data in preparation for model building.
* models/train_classifier.py: The Machine Learning pipeline used to fit, tune, evaluate, and export the model to a Python pickle (pickle is not uploaded to the repo due to size constraints on github).
* app: flask application folder. run.py starts the python server for the web app and prepare visualizations.


## Usage:

1. Run the following commands in the project's root directory to set up your database and model.

* To run ETL pipeline that cleans data and stores in sql database:
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
* To run ML pipeline that trains classifier and saves the model:
        `python models/train_classifier.py data/DisasterResponse.db models/classifier_me.pkl`

2. Run the following command in the app's directory to run your web app:
    `python run.py`

3. Go to http://127.0.0.1:3001/ to check out the API.

![Webapp Screenshot](https://github.com/amirmasoudsfd/disaster-response-app/raw/master/disasterapp_screenshot.png)
