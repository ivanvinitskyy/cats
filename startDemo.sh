#!/bin/bash

cd "$(dirname "$0")"
sudo vagrant up --provision
for i in {0..19}; do curl localhost:9999; echo ''; done > ./rr-result
cat ./rr-result | awk 'BEGIN{error=0} {current = $NF;getline; if($NF == current) error=1} END{if(error)print "Not all requests were served in RR mode"; else print "All requests were served in RR mode"}'
