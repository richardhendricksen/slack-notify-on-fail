FROM python:3.8-slim

COPY requirements.txt /
WORKDIR /
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY LICENSE.txt README.md pipe.yml /
COPY pipe /

ENTRYPOINT ["python3", "/pipe.py"]
