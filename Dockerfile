FROM python:3.9.19-slim-bookworm
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "web.py" ]