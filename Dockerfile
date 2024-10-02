FROM python

WORKDIR /usr/src/orion

COPY req.txt ./

RUN pip install -r req.txt