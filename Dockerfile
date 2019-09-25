FROM centos/python-36-centos7

COPY . /tmp/kfp
RUN pip install -r /tmp/kfp/requirements.txt

ENTRYPOINT ["python", "/tmp/kfp/runner.py"]
