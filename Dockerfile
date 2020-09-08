FROM python:3.8.5-slim
COPY app /app
WORKDIR /app/
RUN pip install --no-cache-dir -r requirement.txt
EXPOSE 5000
CMD [ "python", "app.py" ]
