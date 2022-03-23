FROM alpine:3.15.1

VOLUME [ "/root/test" ]

RUN apk upgrade
RUN apk --update --no-cache add \
    python3 \
    python3-dev \
    py-pip

RUN pip install robotframework

WORKDIR /root

RUN mkdir runKeywordAsync

COPY runKeywordAsync/ /root/runKeywordAsync/

COPY setup.py /root/

RUN pip install -e .

ENTRYPOINT [ "robot", "-d", "test", "test/acceptance.robot" ]




