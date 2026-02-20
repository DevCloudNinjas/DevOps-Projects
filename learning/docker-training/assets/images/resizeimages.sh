#!/bin/bash

docker run -v $(pwd):/imgs dpokidov/imagemagick /imgs/kubernetes_fullsize.png -resize 200x200 /imgs/kubernetes.png
docker run -v $(pwd):/imgs dpokidov/imagemagick /imgs/mesos_fullsize.png -resize 200x200 /imgs/mesos.png
docker run -v $(pwd):/imgs dpokidov/imagemagick /imgs/swarm_fullsize.png -resize 200x200 /imgs/swarm.png