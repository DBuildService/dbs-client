Client Tool for Docker Build Service
====================================

This Client provides library in subcommands.py and thin wrapper around this
library, that basically only parses CLI arguments and constructs a JSON
request from that.


Usage
-----

    usage: dbs-client.py [-h] [--version] [--server url] [-p port] [-u user]
                         [-F FILE]

                         {tasks,taskstatus,images,imageinfo,imagedeps,new,move,rebuild,invalidate}
                         ...

    Client for lightweight communication with DBS server.

    positional arguments:
      {tasks,taskstatus,images,imageinfo,imagedeps,new,move,rebuild,invalidate}
        tasks               Show all tasks
        taskstatus          Show status of the task
        images              Show all images
        imageinfo           Show information about specified image
        imagestatus         Show status information about specified image
        imagedeps           Show deps of specified image
        new                 Submit a new task
        move                Move some image from one registry to another registry
        rebuild             Rebuild already built image
        invalidate          Invalidate all images built from specified image

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --server url          URL of the Build Server
      -p port, --port port  Port number the Build Server runs on
      -u user, --user user  Username, will be replaced by advanced authorization
      -F FILE, --file FILE  JSON file with specification

    This is an open-source project by Red Hat.


Example of usage
----------------

Submit a new task:

    python dbs-client.py -p 8000 new \
                         -g https://github.com/TomasTomecek/docker-hello-world.git \
                         --git-dockerfile-path=Dockerfile

Get info about a task:

    python dbs-client.py -p 8000 taskstatus -t 123465

Get info about all images:

    python dbs-client.py images


How to test the whole DBS on one machine
----------------------------------------

Get sources of all components:

    mkdir dbs ; cd dbs
    for c in dock dbs-client dbs-worker dbs-server ; do
        git clone https://github.com/DBuildService/$c.git
    done

We need three processes, so we will use three terminals.

Install all dependencies as documented in README of particular components.

Prepare building docker image as described at https://github.com/DBuildService/dock.

On terminal-celery, run:

    cd dbs-worker
    PYTHONPATH=../dock/ celery -A dbs_worker.docker_tasks worker -l INFO

On terminal-server, run:

    cd dbs-server
    head -c 500 /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1 >secret_key
    rm -f data/db.sqlite3
    ./manage.py syncdb --noinput
    ./manage.py runserver

On terminal-client, run:

    cd dbs-client
    python dbs-client.py -p 8000 new \
                         -g https://github.com/TomasTomecek/docker-hello-world.git \
                         --git-dockerfile-path=Dockerfile
    python dbs-client.py -p 8000 tasks


Configuration
-------------

You can cange configuration of the client (like server URL) either
by specifying CLI arguments or define them in file ~/.config/dbs,
which can have the following format:

    [client]
    server_url=http://localhost:8000

