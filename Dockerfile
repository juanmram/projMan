# Pull base image.
FROM centos:latest

# Build commands
RUN yum install -y python-setuptools mysql-connector-python mysql-devel gcc python-devel git
RUN easy_install pip
RUN mkdir /opt/projMan
WORKDIR /opt/projMan
ADD requirements.txt /opt/projMan/
RUN pip install -r requirements.txt
ADD . /opt/projMan
ENV FLASK_APP run.py

# Define default command.
#CMD ["flask", "run", "--host=0.0.0.0"]
