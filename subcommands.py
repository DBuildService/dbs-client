#-*- coding: UTF-8 -*-

"""
Functions to call the DBS Restful API and handling the output.
"""

import ConfigParser
import requests
import json
import os

import dbs_exceptions
from dbs_defaults import *



def get_api_url(server=None, port=None):
    """ Retrieve the user information from the config file. """
    config = ConfigParser.ConfigParser()
    config.read(
        os.path.join(os.path.expanduser("~"), ".config", CONFIG_FILE_NAME)
    )

    if config.has_section("client"):
        # Default BUILD_SERVER_URL_DEFAULT or configured server_url:
        if not server and config.has_option("client", "server_url"):
            server = config.get("client", "server_url")

        # Default BUILD_SERVER_URL_DEFAULT or configured server_url:
        if not port and config.has_option("client", "port"):
            port = config.get("client", "port")

    if not server:
        server = BUILD_SERVER_URL_DEFAULT

    if not port:
        port = BUILD_SERVER_PORT_DEFAULT

    if server[0:4] != 'http':
        server = "http://{0}".format(server)

    port_suf = ''
    if port != 80:
        port_suf = ":{0}".format(port)

    return "{0}{1}/v{2}".format(server, port_suf, DBS_API_VERSION)


def get_user():
    """ Retrieve the user information from the config file. """
    return {"username":"fakeusername", "token":"faketoken"}
    config = ConfigParser.ConfigParser()
    if not config.read(
            os.path.join(os.path.expanduser("~"), ".config", CONFIG_FILE_NAME)):
        raise dbs_exceptions.CoprCliNoConfException(
            "No configuration file '~/.config/{0}' found. "
            "See man {0}-cli for more information".format(CONFIG_FILE_NAME))
    try:
        username = config.get("client", "username", None)
        token = config.get("client", "token", None)
    except ConfigParser.Error as err:
        raise dbs_exceptions.CoprCliConfigException(
            "Bad configuration file: {0}".format(err))
    return {"username": username, "token": token}


def _get_data(req):
    """ Wrapper around response from server

    checks data and raises a DBSRequestException with nice error message.
    Otherwise return json object.
    """
    if req.status_code == 404:
        raise dbs_exceptions.DBSCliRequestException("We got 404...\n")
    try:
        output = json.loads(req.text)
    except ValueError:
        raise dbs_exceptions.DBSCliUnknownResponseException(
                    "Unknown response from the server.")
    if req.status_code != 200:
        raise dbs_exceptions.DBSCliRequestException(output["error"])

    if output is None:
        raise dbs_exceptions.DBSCliUnknownResponseException(
                    "No response from the server.")
    return output


def _default_post(url, data=None, args=None, user=None):
    server=None
    port=None
    if args:
       if 'server' in args:
           server=args.pop('server')
       if 'port' in args:
           port=args.pop('port')

    server_api_url = get_api_url(server, port)
    URL = url.format(server_api_url)

    if not user:
        user = get_user()

    if not data:
        data=json.dumps(args)

    # debugging output
    print ("Posting data: {0}".format({'url':URL,'data':data}))

    try:
        req = requests.post(URL,
        #TODO:                    auth=(user["username"], user["token"]),
                            data=data)
    except requests.exceptions.ConnectionError:
        raise dbs_exceptions.DBSCliRequestException("Could not connect to server {0}.".format(URL))
    #except:
    #    raise dbs_exceptions.DBSCliRequestException("Error when sending POST request to {0}.".format(URL))

    output = _get_data(req)
    if output is not None:
        # TODO: should not we use some wrapper around message like [retcode=1, message=...]?
        # then it would be:
        # print(output["message"])
        print(output)


def _default_get(url, data=None, args=None, user=None):
    server=None
    port=None
    if args:
       if 'server' in args:
           server=args.pop('server')
       if 'port' in args:
           port=args.pop('port')

    server_api_url = get_api_url(server, port)
    URL = url.format(server_api_url)

    if not user:
        user = get_user()

    # debugging output
    print ("Getting data: {0}".format({'url':URL,'data':data}))

    try:
        req = requests.get(URL)
    #TODO:                       ,auth=(user["username"], user["token"]))
    except requests.exceptions.ConnectionError:
        raise dbs_exceptions.DBSCliRequestException("Could not connect to server {0}.".format(URL))
    #except:
    #    raise dbs_exceptions.DBSCliRequestException("Error when sending GET request to {0}.".format(URL))

    output = _get_data(req)
    if output is not None:
        # TODO: should not we use some wrapper around message like [retcode=1, message=...]?
        # then it would be:
        # print(output["message"])
        print(output)


def action_new(data=None, args=None, user=None):
    """ Submit a new build. Specify either data or args. """
    return _default_post('{0}/image/new', data, args, user)


def action_move(data=None, args=None, user=None):
    """ Move image from one registry to another. Specify either data or args. """
    image=args.pop('image')
    return _default_post('{{0}}/image/move/{0}'.format(image), data, args, user)


def action_rebuild(data=None, args=None, user=None):
    """ Rebuild already built image. Specify either data or args. """
    image=args.pop('image')
    return _default_post('{{0}}/image/rebuild/{0}'.format(image), data, args, user)


def action_invalidate(data=None, args=None, user=None):
    """ Invalidate all deps of image specified by ID. Specify either data or args. """
    image=args.pop('image')
    return _default_post('{{0}}/image/invalidatechilds/{0}'.format(image), data, args, user)


def action_tasks(data=None, args=None, user=None):
    """ Show all tasks. """
    return _default_get('{0}/tasks', data, args, user)


def action_taskstatus(data=None, args=None, user=None):
    """ Show tasks status. """
    task=args.pop('task')
    return _default_get('{{0}}/taskstatus/{0}'.format(task), data, args, user)


def action_images(data=None, args=None, user=None):
    """ Show all images """
    return _default_get('{0}/images', data, args, user)


def action_imageinfo(data=None, args=None, user=None):
    """ Show image info """
    image=args.pop('image')
    return _default_get('{{0}}/image/{0}/info'.format(image), data, args, user)


def action_imagestatus(data=None, args=None, user=None):
    """ Show image info """
    image=args.pop('image')
    return _default_get('{{0}}/image/{0}/status'.format(image), data, args, user)


def action_imagedeps(data=None, args=None, user=None):
    """ Show image deps """
    image=args.pop('image')
    return _default_get('{{0}}/image/{0}/deps'.format(image), data, args, user)

