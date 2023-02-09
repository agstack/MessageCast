FROM rockylinux:9.0
RUN yum update -y
RUN yum install -y python39 python3-pip python-pip-wheel gcc python3-devel
WORKDIR /src
RUN python3.9 -m venv .venv
RUN . .venv/bin/activate
COPY requirements.txt /src
RUN pip install -r requirements.txt
RUN python3.9 -m pip install gunicorn
EXPOSE 8000
