# data science notebook
#ARG BASE_CONTAINER=ucsdets/datahub-base-notebook:2020.2-stable
ARG BASE_CONTAINER=ubuntu:18.04
FROM $BASE_CONTAINER

LABEL maintainer="Najeem Kanishka"

USER root
COPY /requirements-docker.txt /

# install python and related dependencies
RUN apt update -y
RUN apt upgrade -y

RUN apt install -y git vim
RUN apt install -y wget curl
RUN apt install -y language-pack-en
RUN apt install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4
RUN apt install -y python3 python3-pip python3-scipy
RUN apt install -y mysql-client mysql-server libmysqlclient-dev

# these files need to be installed separately of requirements
RUN pip3 install --no-cache-dir Cython
RUN pip3 install --no-cache-dir html5lib
RUN pip3 install --no-cache-dir -U scikit-learn

# finally, install from requirements
RUN pip3 install --no-cache-dir -r /requirements-docker.txt

### The following lines are sourced from: https://nander.cc/using-selenium-within-a-docker-container

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome
RUN apt-get -y update
# Magic happens
RUN apt-get install -y google-chrome-stable
# Installing Unzip
RUN apt-get install -yqq unzip
# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` \
    curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE \
    `/chromedriver_linux64.zip
# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# Set display port as an environment variable
ENV DISPLAY=:99

### End citation

CMD ["/bin/bash"]
