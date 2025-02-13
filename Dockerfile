FROM python:3.12-slim
WORKDIR /Feedback
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /Feedback
EXPOSE 5000
CMD ["python", "app.py"]