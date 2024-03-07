FROM ubuntu:23.04

ENV DEBIAN_FRONTEND=noninteractive

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Set environment variable
ENV DISPLAY=$DISPLAY

# Define volume
VOLUME ["/tmp/.X11-unix"]

# Install Python 3 and packages

RUN apt-get update && apt-get install -y python3 python3-pip python3.11-venv

# Create a working directory
WORKDIR /app/src/ui

# Copy the current directory contents into the container at /app
COPY . /app

# Install the requisite packages, it works without this currently.
# We'll probably want to use this in the future as we start adding in the 
# actual RL training and models that require other python packages

RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install -r /app/requirements.txt

ENV PATH="/app/venv/bin:$PATH"

RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 ffmpeg libgl1 libegl1 libxcb-cursor0
RUN apt-get update && apt-get install -y --reinstall qt6-base-dev

# Default command to run
CMD ["/app/venv/bin/python3", "/app/src/ui/app.py"]
