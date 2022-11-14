FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /smarty
COPY requirements.txt /smarty/
RUN pip3 install -r requirements.txt
COPY . /smarty/