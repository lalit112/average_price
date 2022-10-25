FROM python:3.8
# Python docker images: https://github.com/docker-library/docs/tree/master/python/

# Create a working directory
WORKDIR /app

# Copy requirements file to current directory
COPY requirements.txt .

# Copy contents of project to current directory
COPY . /app

# Create and activate Virtual environment
#RUN python3 -m venv venv
#RUN source venv/bin/activate

# Install python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Run the application file
CMD ["python", "./run.py"]