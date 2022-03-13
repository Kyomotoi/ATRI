FROM python:3.8

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"

COPY ./ /app/

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

CMD python3 *.py