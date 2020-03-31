# test-task

This repo contains an implementation of test task.
It has the following structure:
- lib/views - widgetastic views covering login/board/card pages and modals
- lib/widgets - widgetastic widgets
- tests - tests itself
- utils - utilities needed for testing like set up logging and etc

There many ways to run existing smoke tests. 
The smoothest one is to use pre-built docker container or build it from scratch.
The way with pre-built container: 

```shell script
docker pull docker.io/ez999/test-task:latest
docker run -it --shm-size=512m docker.io/ez999/test-task:latest
``` 
