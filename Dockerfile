from python:3.8

ENV PYTHONPATH="${PYTHONPATH}:/root"

WORKDIR /root/

ENTRYPOINT ['/bin/bash']