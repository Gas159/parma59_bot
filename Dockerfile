FROM ubuntu:latest
LABEL authors="gas"

ENTRYPOINT ["top", "-b"]