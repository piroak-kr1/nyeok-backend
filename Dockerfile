FROM python:3.12.1-alpine

# Set the working directory
WORKDIR /APP

# Copy the directory contents of app into the container at /app
COPY ./app/. /APP

# Install packages specified in requirements.txt
# RUN pip install --root-user-action=ignore -r requirements.txt
# TODO: use poetry instead

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["fastapi", "dev", "--port", "8000", "--host", "0.0.0.0"]
