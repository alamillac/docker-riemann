# riemann-dash
#
# VERSION               1.0

FROM     ruby:2
MAINTAINER Andres F. Lamilla, "alamilla@gmail.com"

RUN gem install riemann-dash thin

ADD src/config.rb /usr/local/etc/config.rb

EXPOSE 4567

CMD ["riemann-dash", "/usr/local/etc/config.rb"]
