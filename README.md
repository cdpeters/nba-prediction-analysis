# **NBA Champion Analysis**

## **Overview of Project**
The NBA Champion Analysis website was the result of a four-week-long group
effort, serving as the final project of [*The Data Science and Visualization Boot Camp*](https://extendedstudies.ucsd.edu/courses-and-programs/data-science-and-visualization-part-i)
run by UC San Diego Extension (renamed to UC San Diego Division of Extended
Studies). The project was completed in April 2022, with the boot camp concluding
in May 2022. The team consisted of three students: Pascale Geday, Lauren Hess,
and myself. A visualization component and a machine learning component were
required for successful completion of the project.

At the conclusion of the project, we were able to complete a website with
Tableau visualizations and predict a champion via machine learning. We presented
the website to our boot camp class by running it locally. We had further
aspirations to eventually host the website but left this as a post boot camp
goal.

## **My Role**
My role on the original project consisted of the following areas:
- ETL pipeline - from web scraping to database loading.
- Machine learning analysis and the associated prediction page.

## **Project Revival**
At the end of October 2023, I started working to bring the website back to life
with the goal of hosting the project online. While revisiting all of the work
that we did, I was able to clean up a lot of the rough edges that were the
result of time constraints in the original timeline. Throughout the process, I
made a point of preserving the work of my teammates as much as possible because
I did not want to lose the contributions they made. The revival was completed in
April 2024. Below is a collection of some of the fixes/improvements that were
made.

### **Project environment**
- Environment reconfigured to use `conda` for environment creation and `poetry`
    for package management.
- Added development tools such as `black` for formatting, `isort` for import
    sorting, and `flake8` for various linting operations.
- Configured the app to use environment variables for the database credentials
    to mirror the hosting set up.

### **ETL Pipeline**
- Changes to the NBA stats website broke the scraping code so I rewrote the ETL
    portions that were affected.
- Modified the extract stage to allow for collection of new season data.
- Repurposed the prototype notebook to compare two tools for database
    communication that could be used in the app: `ibis-framework` and
    `Flask-SQLAlchemy`. Also experimented with ORM models to help facilitate
    database queries.
- Used `SQLAlchemy` to create the database schema and to construct the ORM
  models. The primary purpose of this work was to get more practice with
  `SQLAlchemy` and was not strictly necessary.

### **Database**
- Reduced redundant data storage by moving columns common to many tables into
    their own tables and by taking advantage of foreign key constraints.

### **Machine Learning**
- Reorganized the machine learning jupyter notebook for clarity. Added more
    explanation so that it is easier to understand our approach. Fixed errors in
    some of the analysis.
- Completely reworked the prediction page report. Added a future work section
    that lists areas of weakness in our analysis and our plans to address them
    in a second pass.

### **Python App Structure**
- Split our main app file into modules for clarity and maintainability. The
    modules cover database/csv related operations, router creation, ORM model
    creation, handling of Flask extensions, and utility functions.
- Added server side caching of the database query used in the app and allowed
    for client side caching of the different app pages.

### **HTML Structure and Styling**
- Cleaned up the HTML structure and visual styling for a consistent look across
    all pages.

### **Tableau Visualizations**
- Replaced the embedded Tableau visualizations with preview images and links to
    the Tableau Public versions (they consumed too many resources and thus would
    have added too much cost to the final hosted version of the app).
- For 3 out of 4 of the visualizations, the graphs were distorted and hard to
    use properly, so I re-hosted these on my Tableau Public profile with minor
    changes for usability. I also included links to the original versions found
    on my teammates' profiles.

### **Documentation**
- Added type annotations to all functions.
- Added numpy style docstrings to all non-trivial functions.

### **Hosting**
- Set up database and app hosting on [*railway.app*](https://railway.app/).

## **Website and Repos**
Here are links to the website and to the GitHub repositories of the current and
original versions of the project.

### **Current Version**
- Website:
  [*https://nba-champion-analysis.up.railway.app/*](https://nba-champion-analysis.up.railway.app/)
- Repo:
  [*https://github.com/cdpeters/nba-prediction-analysis*](https://github.com/cdpeters/nba-prediction-analysis)

### **Original Version**
- Website: This version is not hosted.
- Repo:
  [*https://github.com/pascalegeday/NBA_Prediction_Analysis*](https://github.com/pascalegeday/NBA_Prediction_Analysis)

## **Project Files**
The following list contains information about the files found in the different
repo folders:
- ***flowcharts/***
    - ERD diagrams and flowcharts representing the project infrastructure.
- ***notebooks/***
    - ***ETL_and_sqlalchemy/***
        - [*nba_stats_extract.ipynb*](https://github.com/cdpeters/nba-prediction-analysis/blob/main/notebooks/ETL_and_sqlalchemy/nba_stats_extract.ipynb)
          and
          [*nba_stats_transform_load.ipynb*](https://github.com/cdpeters/nba-prediction-analysis/blob/main/notebooks/ETL_and_sqlalchemy/nba_stats_transform_load.ipynb)
          contain all of the ETL pipeline code. They are split in order to
          create a buffer between the web scraping and the
          transformation/loading stages.
        - [*query_db_prototype.ipynb*](https://github.com/cdpeters/nba-prediction-analysis/blob/main/notebooks/ETL_and_sqlalchemy/query_db_prototype.ipynb)
          contains database connection and query prototyping.
    - ***html_table_customization/***
        - [*html_table_customization.ipynb*](https://github.com/cdpeters/nba-prediction-analysis/blob/main/notebooks/html_table_customization/html_table_customization.ipynb)
          contains code that allows for adding html attributes to any element in
          the table html produced by the `pandas` method `DataFrame.to_html`.
    - ***machine_learning/***
        - [*nba_stats_ml.ipynb*](https://github.com/cdpeters/nba-prediction-analysis/blob/main/notebooks/machine_learning/nba_stats_ml.ipynb)
          contains the machine learning analysis.
- ***src/***
    - [*app.py*](https://github.com/cdpeters/nba-prediction-analysis/blob/main/src/app.py)
      is the main file for running the app.
    - Supporting python files, html templates, and static content files are also
      found in this folder.
