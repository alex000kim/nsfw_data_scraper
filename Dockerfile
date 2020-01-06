FROM ubuntu:18.04
RUN apt update \
 && apt upgrade -y \
 && apt install wget rsync imagemagick default-jre -y 
RUN mkdir /root/nsfw_data_scraper
WORKDIR /root/nsfw_data_scraper
COPY ./ /root/nsfw_data_scraper
COPY ./scripts/rip.properties /root/.config/ripme/rip.properties
ENTRYPOINT ["/bin/bash"]