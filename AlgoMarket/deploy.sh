#! /bin/bash
killall gunicorn

if [ ! -z ${1} ]; then
    if [ ${1} == "daemon" ];
    then
        gunicorn --bind 0.0.0.0:8002 AlgoMarket.wsgi:application --${1}
    fi 
else
    gunicorn --bind 0.0.0.0:8002 AlgoMarket.wsgi:application
fi

