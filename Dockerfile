FROM python:3.12-slim
WORKDIR /Feedback
COPY requirements.txt requirements.txt
COPY . /Feedback
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.run"]