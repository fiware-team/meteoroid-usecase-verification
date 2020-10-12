curl http://192.168.28.10:31026/v2/entities/test1/attrs/temp/value -s -S \
    --header 'Content-Type: text/plain' \
    -H 'Fiware-Service: iotpj' \
    -X PUT -d $1
