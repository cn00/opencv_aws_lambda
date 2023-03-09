FROM amazonlinux

# FROM lambci/lambda:build-python3.7

RUN yum install -y zip python3 python3-pip libzbar-dev libgl-dev libglib2.0-bin

COPY pip.conf /root/.pip/pip.conf

# Install Python packages
RUN mkdir /packages
ADD requirements.txt /packages/requirements.txt
RUN mkdir -p /packages/opencv-python-3.7/python/lib/python3.7/site-packages
RUN pip3 install -r /packages/requirements.txt -t /packages/opencv-python-3.7/python/lib/python3.7/site-packages

# Create zip files for Lambda Layer deployment
WORKDIR /packages/opencv-python-3.7/
RUN mkdir python/lib/python3.7/site-packages/pyzbar.libs; \
    # zip -r9 /packages/cv2-python37.zip .;
# WORKDIR /packages/
# RUN rm -rf /packages/opencv-python-3.7/
