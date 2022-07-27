FROM python:latest

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirement.txt /code/
RUN pip install -r requirement.txt

# Copy project
COPY . /code/

