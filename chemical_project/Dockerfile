# 1. Use Python 3.10
FROM python:3.12-slim

# 2. Set up the computer
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# 3. Install Dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the Project Code
COPY . /app/

# 5. Run Migrations and Collect Static Files (Setup)
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# 6. Start the Server (Using Gunicorn for Production)
# Render automatically assigns a PORT, Gunicorn will use it.


# 6. Create Admin User (if missing) and Start Server
CMD python manage.py createsuperuser --noinput || true && gunicorn chemical_project.wsgi:application --bind 0.0.0.0:$PORT