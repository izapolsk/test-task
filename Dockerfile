FROM fedora:30

ENV SELENIUM_VERSION 3.141.0
ENV DESTDIR=/sprintboards
ENV GIT_SSL_NO_VERIFY true

USER root

# installing essential packages
RUN dnf install -y git vim python3 python3-pip zip && dnf clean all

# chrome
ADD https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm \
    /root/google-chrome-stable_current_x86_64.rpm
RUN dnf install -y /root/google-chrome-stable_current_x86_64.rpm && \
    rm -f /root/google-chrome-stable_current_x86_64.rpm

# chromedriver
ENV DESTFILE /root/chrome-driver/chromedriver_linux64.zip
RUN CHROME_VERSION=$(rpm -q --qf "%{VERSION}\n" google-chrome-stable|sed -Ee 's/^(.*)\..*/\1/') && \
    CHROME_DRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}) && \
    mkdir -p /root/chrome-driver && \
    curl -o ${DESTFILE} https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip -d /root/chrome-driver/ ${DESTFILE} && \
    rm -f ${DESTFILE}
    ENV PATH="${PATH}:/root/chrome-driver/"


# clone tests
RUN mkdir $DESTDIR
RUN git clone https://github.com/izapolsk/test-task.git $DESTDIR
WORKDIR $DESTDIR

# install python requirements
RUN pip3 install -r requirements.txt
