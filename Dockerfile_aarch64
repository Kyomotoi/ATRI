FROM flyingjoe/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"

COPY ./ /app/

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade --quiet -i https://pypi.tuna.tsinghua.edu.cn/simple/ pip \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends wget \
	&& wget -q  https://github.com/PINTO0309/Tensorflow-bin/releases/download/v2.8.0/tensorflow-2.8.0-cp39-none-linux_aarch64.whl \
	&& pip install *.whl --no-cache-dir --upgrade --quiet -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
	&& pip install --no-cache-dir --upgrade -r requirements.txt --quiet -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf *.whl

VOLUME /app/accounts /app/data

CMD python3 main.py