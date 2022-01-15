FROM python:3.10.1

# Set the workspace
WORKDIR /app

# Copy the files to the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Run the application
CMD ["python", "index.py"]