# Procfile for Azure Web App
# Tells Azure how to start the Django application

web: gunicorn questionnaire_project.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
