# **Fitness Slack Bot**

Web server for slack bot that posts fitness challenges daily on the slack channel. Bot is created as to be deployed onto AWS server using github workflows. 

## Configurations
- Hosted using: AWS Elastic beanstalk
- Database used : Postgres
- Daily reminders sent using : Cron jobs
- CI/CD pipeline using : Github workflows

## Project setup
- Create virtual environment

    ```python -m venv env```

- Activate the virtual environment

    ```source env/bin/activate```

- Install dependencies

    ```python -m pip install -r requirements.txt```

- Run the server

    ```python application.py```
