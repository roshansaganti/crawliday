FROM python:3.12-alpine

# Install Doppler CLI
RUN wget -q -t3 'https://packages.doppler.com/public/cli/rsa.8004D9FF50437357.key' -O /etc/apk/keys/cli@doppler-8004D9FF50437357.rsa.pub && \
  echo 'https://packages.doppler.com/public/cli/alpine/any-version/main' | tee -a /etc/apk/repositories && \
  apk add doppler

# Copy directory
COPY . /app

# Change directory
WORKDIR /app

# Set up environment
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Execute
# RUN python crawl.py halloween

# Keep container running indefinitely
ENTRYPOINT ["tail", "-f", "/dev/null"]