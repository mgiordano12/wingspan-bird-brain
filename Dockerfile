FROM ubuntu:23.04

ENV DEBIAN_FRONTEND=noninteractive

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Set environment variable
ENV DISPLAY=$DISPLAY

# Define volume
VOLUME ["/tmp/.X11-unix"]

# Install Python 3, PyQt6
RUN apt-get update && apt-get install -y python3-pyqt6
RUN apt-get update && apt-get install -y adduser libxcb1 libxcb-render0 libxcb-shm0 libxcb-xinerama0 qtcreator x11-apps
RUN ldd /usr/lib/x86_64-linux-gnu/qt6/plugins/platforms/libqxcb.so
RUN dpkg -S /usr/lib/x86_64-linux-gnu/libxcb-xinerama.so.0 

# Add user
RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# Create a working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the requisite packages, it works without this currently.
# We'll probably want to use this in the future as we start adding in the 
# actual RL training and models that require other python packages
#RUN pip install --no-cache-dir -r requirements.txt

# Default command to run
CMD ["python3", "/app/src/ui/app.py"]