# wingspan-bird-brain
Reinforcement learning model for wingspan game


## Running it all in Docker

Just run it if you're on Linux, otherwise use WSL if on Windows.

If you're using WSL on Windows follow these instructions to set up WSL: https://docs.docker.com/desktop/wsl/

Note: Start by running `wsl --install` to install the Ubuntu distro for WSL.

```
cd /path/to/wherever/you/cloned/me
```

```
sudo docker build -t wingspan-birdbrain-pyqt .
```

```
sudo docker run --rm -it   -v /run/user/1000/gdm/Xauthority:/root/.Xauthority -v /tmp/.X11-unix:/tmp/.X11-unix   -e DISPLAY=$DISPLAY   wingspan-birdbrain-pyqt
```


