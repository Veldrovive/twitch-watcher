FROM python:3.10.1

# Set the workspace
WORKDIR /app

# Copy the files to the container
COPY constants.py /app/constants.py
COPY downloader.py /app/downloader.py
COPY entry.py /app/entry.py
COPY index.py /app/index.py
COPY memory.py /app/memory.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Run the application
CMD ["python", "index.py"]