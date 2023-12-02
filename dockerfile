# Use an official Python runtime as a parent image
FROM python:3.11.3

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP __init__.py

# Run the Flask app when the container launches
CMD ["flask", "run", "--host=192.168.68.131"]