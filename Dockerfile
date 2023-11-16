# Use the base image
FROM jozo/pyqt5

# Create a user if it does not already exist, call it "qtuser"
RUN id -u qtuser &>/dev/null || useradd -ms /bin/bash qtuser
USER qtuser

# Set environment variable
ENV DISPLAY=$DISPLAY

# Define volume
VOLUME ["/tmp/.X11-unix"]

# Default command to run
CMD ["python3", "/tmp/hello.py"]