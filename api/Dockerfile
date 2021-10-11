# Use an official Python runtime as a parent image
FROM python:3.9

# Adding backend directory to make absolute filepaths consistent across services
WORKDIR /todo-challenge/api

# Install Python dependencies
COPY requirements.txt /todo-challenge/api
RUN pip3 install --upgrade pip -r requirements.txt

# Add the rest of the code
COPY . /todo-challenge/api

# Make port 8000 available for the app
EXPOSE 8000

# Use 0.0.0.0 for the host within the Docker container,
# otherwise the browser won't be able to find it
CMD python3 manage.py runserver 0.0.0.0:8000