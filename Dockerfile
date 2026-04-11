# first we choose the immage
# this is a basic debian img
#___________________________________________
# <><><><><><><><><><><><><><><><><><><><><>
#___________________________________________
# how to run the container :D
# Turn on docker desktop
#
# $"systemctl --user enable docker-desktop"
# $"systemctl --user start docker-desktop"
#
# $"docker build -t chessbot . "
# $"docker run -it chessbot "
#
#___________________________________________
# <><><><><><><><><><><><><><><><><><><><><>
#___________________________________________


FROM python:3.12-slim 

# creats a pseudo working dir in our container
WORKDIR /app

# installs bash incase img doesnt have it
RUN apt-get update && apt-get install -y bash

# moves requirments.txt to correct dir so we can run pip install after
COPY requirements.txt /app/

# installs dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# move src to its own folder 
COPY src/ ./src/

# moves tests to its own folder aswell
COPY tests/ ./tests/

# depends on the img for what you use here, not all imgs have bash
CMD ["bash"]
