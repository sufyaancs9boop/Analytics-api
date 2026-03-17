# 1. Create the venv
RUN python -m venv /opt/venv

# 2. Set environment variables so the system uses the venv automatically
# This replaces the need for "source activate"
ENV PATH="/opt/venv/bin:$PATH"

# 3. Copy your requirements from your project folder into the container
COPY requirements.txt .

# 4. Install them (it will automatically go into /opt/venv because of the PATH above)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Installing OS dependencies, of the linux machine(vm) or server it will run on
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

#Create the mini Vm's code directory
RUN mkdir -p /code

#Set the working directory in the container to /code
WORKDIR /code   

# Copy the requirements.txt file to the container
COPY requirements.txt /code/requirements.txt

#Copy the project code into the container's working directory
COPY ./src/code

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt|

# make the bash script executable
COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the FastAPI project via the runtime script
# when the container starts
CMD ["/opt/run.sh"]