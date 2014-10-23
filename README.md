Client Tool for Docker Build Service
====================================

This Client provides library in subcommands.py and thin wrapper around this library, that basically only parses CLI arguments and constructs a JSON request from that.


Usage
=====

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


Configuration
=============

You can cange configuration of the client (like server URL) either by specifying CLI arguments or define them in file ~/.config/dbs, which can have the following format:

    [client]
    server_url=http://localhost:8000

