FROM nestybox/jenkins-syscont:latest

# Install docker-compose
RUN curl -L https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-linux-aarch64 -o /usr/local/bin/docker-compose \ 
&& chmod +x /usr/local/bin/docker-compose