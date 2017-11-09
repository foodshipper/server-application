FROM python
ENV foo /app/server
WORKDIR ${foo}
RUN python3 -m venv ../ && /bin/bash -c "source ../bin/activate"
ADD . .
RUN pip3 install --no-cache-dir -r requirements.txt && cp conf/foodship-api.ini ./foodship-api.ini
EXPOSE 8080
ENTRYPOINT circusd foodship-api.ini
