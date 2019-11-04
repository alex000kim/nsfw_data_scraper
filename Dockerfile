FROM ubuntu:18.04
RUN apt update \
 && apt upgrade -y \
 && apt install wget rsync imagemagick default-jre -y 
ENTRYPOINT ["/bin/bash"]