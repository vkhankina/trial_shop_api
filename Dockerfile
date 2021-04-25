# Use the official image as a parent image.
FROM debian:buster-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN apt update && \
    apt install python3 python3-pip uwsgi-plugin-python3 default-mysql-client libmariadbclient-dev libpcre3 libpcre3-dev -y && \
    mkdir /usr/src/app && \
    useradd -d /usr/src/app --system --user-group --shell /usr/sbin/nologin  uwsgi && \
    apt clean all && \
    rm -rf /var/cache/apt


# Copy the file from your host to your current location.
COPY requirements.txt /usr/src/app

# Run the command inside your image filesystem.
# FIX: remove temp files
RUN ls -l /usr/src/app
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

# Add metadata to the image to describe which port the container is listening on at runtime.
EXPOSE 8080 9191

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . /usr/src/app

# Provide settings file to django
RUN mv /usr/src/app/prod.settings.py /usr/src/app/trial/settings.py

RUN python3 /usr/src/app/manage.py collectstatic --no-input

# Running migrations and uWSGI HTTP Router.
ENTRYPOINT ["/usr/src/app/run.sh"]