#!/bin/bash

cd "$(dirname "$0")"
sudo vagrant up --provision
for i in {1..9}; do curl localhost:9999; echo ''; done
