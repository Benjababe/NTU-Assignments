FROM ubuntu/apache2:2.4-20.04_beta

# Install necessary tools
RUN apt update
RUN apt upgrade -y
RUN apt install gcc make -y

# Enable CGI extension for apache
RUN ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load

# Copy and extract bash source
COPY bash-4.3.tar.gz /tmp/bash-4.3.tar.gz
RUN tar -xf /tmp/bash-4.3.tar.gz -C /tmp/

# Build vulnerable bash and replace the default bash
WORKDIR /tmp/bash-4.3
RUN ./configure --bindir=/tmp/bash-4.3
RUN make && \
    mv /bin/bash /bin/bash_bak && \
    cp ./bash /bin/bash
WORKDIR /
RUN rm -rf /tmp/bash-4.3*

# Setup CGI scripts
WORKDIR /usr/lib/cgi-bin
COPY cgi-bin .
RUN chmod +x setup.sh && ./setup.sh

# Expose apache port
EXPOSE 80