FROM continuumio/anaconda3:4.4.0
MAINTAINER Nikhil Kohli

COPY ./ /usr/local/python

EXPOSE 8501

WORKDIR /usr/local/python

RUN pip install -r requirements.txt

CMD streamlit run app.py