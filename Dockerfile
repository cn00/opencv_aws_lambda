FROM lambci/lambda:build-python3.9

COPY pip.conf /root/.pip/pip.conf

# Install Python packages
RUN mkdir /packages
ADD requirements.txt /packages/requirements.txt
RUN mkdir -p /packages/opencv-python-3.8/python/lib/python3.9/site-packages
RUN pip3.9 install -r /packages/requirements.txt -t /packages/opencv-python-3.9/python/lib/python3.9/site-packages

# Create zip files for Lambda Layer deployment
WORKDIR /packages/opencv-python-3.9/
RUN zip -r9 /packages/cv2-python39.zip .;\
    cp /packages/cv2-python39.zip /out
# WORKDIR /packages/
# RUN rm -rf /packages/opencv-python-3.9/
