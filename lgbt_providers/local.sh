#!/bin/bash

#kill any outstanding port connections
echo fuser -k 8080/tcp
#connect local server
echo `python ../google_appengine/dev_appserver.py ../lgbt_providers`
