FROM python:3.12-alpine

# Copy directory
COPY . /app

# Change directory
WORKDIR /app

# Set up environment
RUN pip install -r requirements.txt

# Execute
# RUN python crawl.py halloween

# Keep container running indefinitely
ENTRYPOINT ["tail", "-f", "/dev/null"]