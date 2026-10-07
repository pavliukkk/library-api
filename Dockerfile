FROM ubuntu:latest
LABEL authors="Pavliuk"

ENTRYPOINT ["top", "-b"]