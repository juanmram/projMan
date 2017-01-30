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

# Define default command.
CMD ["python", "run.py"]
