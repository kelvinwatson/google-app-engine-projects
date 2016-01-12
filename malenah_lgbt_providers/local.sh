#!/bin/bash

#kill any outstanding port connections
echo fuser -k 8080/tcp

#backup incase above doesn't work
lsof -P | grep ':8080' | awk '{print $2}' | xargs kill -9

#connect local server
echo `python ../google_appengine/dev_appserver.py ../malenah_lgbt_providers`
