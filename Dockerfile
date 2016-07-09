FROM centos:7
MAINTAINER Giles Thomas <giles@lemonman.org.uk>

RUN yum -y update && \
    yum clean all

COPY pixelserv.py /usr/local/bin/pixelserv
RUN  chmod 755 /usr/local/bin/pixelserv

RUN useradd -ms /bin/bash pixelserv
USER pixelserv

EXPOSE 8000

CMD ["pixelserv"]

