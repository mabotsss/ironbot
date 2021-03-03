FROM nandoscrz/ironbots:7.0
RUN apk add aria2
RUN git clone https://github.com/mabotsss/ironbot /root/ironbot
WORKDIR /root/ironbot/
RUN pip3 install -r resources/requirements.txt
CMD ["python3", "main.py"]
