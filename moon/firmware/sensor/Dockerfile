FROM python:3.9-slim-bullseye

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY firmware.py /firmware.py

CMD sh -c "python /firmware.py"
