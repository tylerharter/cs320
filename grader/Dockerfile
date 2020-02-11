FROM ubuntu:18.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN pip3 install jupyter pandas numpy requests matplotlib beautifulsoup4 statistics recordclass haversine sklearn
RUN apt-get -y install zip
