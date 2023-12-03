FROM ubuntu:23.04

ENV DEBIAN_FRONTEND=noninteractive

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Set environment variable
ENV DISPLAY=$DISPLAY

# Define volume
VOLUME ["/tmp/.X11-unix"]

# Install Python 3 and packages
RUN apt-get update
RUN apt-get install -y python3-pyqt6
RUN apt-get install -y python3-requests
RUN apt-get install -y python3-numpy

# Create a working directory
WORKDIR /app/src/ui

# Copy the current directory contents into the container at /app
COPY . /app

# Install the requisite packages, it works without this currently.
# We'll probably want to use this in the future as we start adding in the 
# actual RL training and models that require other python packages
#RUN pip install --no-cache-dir -r requirements.txt

# Default command to run
CMD ["python3", "/app/src/ui/app.py"]