 # A dockerfile must always start by importing the base image.
# We use the keyword 'FROM' to do that.
# In our example, we want import the python image.
# So we write 'python' for the image name and 'latest' for the version.
FROM python:latest

WORKDIR /

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir tensorflow numpy pandas 
RUN pip install --no-cache-dir networkx
RUN pip install --no-cache-dir pickle
RUN pip install --no-cache-dir mathplotlib

# In order to launch our python code, we must import it into our image.
# We use the keyword 'COPY' to do that.
# The first parameter 'main.py' is the name of the file on the host.
# The second parameter '/' is the path where to put the file on the image.
# Here we put the file at the image root folder.
COPY /data+
COPY artist_follower_vs_neighbours.py


# We need to define the command to launch when we are going to run the image.
# We use the keyword 'CMD' to do that.
# The following command will execute "python ./main.py".
#CMD cat /etc/alpine-release file_does_not_exist.txt > /home/output.txt 2>/home/error.txt
CMD  python /artist_follower_vs_neighbours.py
#CMD [ "python", "./send_data.py" ]
#to run this image:
# sudo docker run --mount 'type=bind,src={absolut/path/to/data_folder},dst=/data/hospital' thesis:latest
#the data file has to be named hospital_data.csv