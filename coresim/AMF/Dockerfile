FROM ubuntu:18.04

MAINTAINER Praveen <velugubantla.praveen@ltts.com>

RUN apt-get update &&  apt-get install -y apt-utils && apt-get install -y openjdk-8-jre && apt-get install -y openjdk-8-jdk  && apt-get install -y python3 && apt-get install -y python3-pip && pip3 install lxml && pip3 install sockets && apt -y install net-tools && apt-get install -y openssh-server && apt-get install -y maven && apt-get install -y git

COPY . /

RUN cp -r code pom.xml Main.java root

RUN ./sftp_config.sh

RUN ./ves_agent.sh

WORKDIR /root/code

CMD ["tail", "-f", "/dev/null"]

#CMD ["python3","AMF.py","AMF"]
