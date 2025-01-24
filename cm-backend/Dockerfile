FROM python:3.10

RUN apt-get update \
  && apt-get install -y graphviz


WORKDIR /app/src

# copy & install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# copy & execute sourcecode
COPY ./cm-backend /app/src
CMD ["fastapi", "run", "concept_mapper_api.py", "--port", "8000"]