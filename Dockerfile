FROM nandoscrz/ironbots:7.0
RUN apk update && apk upgrade && pip install --upgrade pip
RUN git clone https://github.com/mabotsss/ironbot /root/ironbot
WORKDIR /root/ironbot/
RUN pip3 install -r resources/requirements.txt
CMD ["python3", "main.py"]
