# Pull base image.
FROM centos:latest

# Build commands
RUN yum install -y python-setuptools mysql-connector-python mysql-devel gcc python-devel git
RUN easy_install pip
RUN mkdir /opt/projMan
WORKDIR /opt/projMan
ADD . /opt/projMan
RUN pip install -r requirements.txt
ENV DATABASE_URL 'mysql://root:jonNBZ91@mysql/projman_db'

# Define default command.
CMD ["python", "run.py"]
