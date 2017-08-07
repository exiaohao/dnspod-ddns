FROM daocloud.io/library/python:3.6.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
ADD . /code/%
