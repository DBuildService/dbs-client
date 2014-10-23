#!/usr/bin/env python
import argparse
import json
import requests

import subcommands
from dbs_defaults import *

"""
Client for lightweight communication with DBS server.
"""

def _get_copied(args):
    s=['server', 'port', 'user']
    s.extend(args)
    return s


def _get_specified(args, fields):
    d=vars(args)
    return dict((key, d[key]) for key in _get_copied(fields))


# sub-command functions
def action_new(args):
    if args.file:
        return subcommands.action_new(data=args.file.read())
    payload = _get_specified(args, ['git', 'git_path', 'git_commit', 'parent', 'target', 'repo', 'tag'])
    return subcommands.action_new(args=payload)


def action_move(args):
    if args.file:
        return subcommands.action_move(data=args.file.read())
    payload = _get_specified(args, ['source', 'target', 'tag', 'image'])
    return subcommands.action_move(args=payload)


def action_invalidate(args):
    if args.file:
        return subcommands.action_invalidate(data=args.file.read())
    payload = _get_specified(args, ['target', 'image'])
    return subcommands.action_invalidate(args=payload)


def action_rebuild(args):
    if args.file:
        return subcommands.action_rebuild(data=args.file.read())
    payload = _get_specified(args, ['target', 'image'])
    return subcommands.action_rebuild(args=payload)


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Client for lightweight communication with DBS server.',
                                 epilog="This is an open-source project by Red Hat.")
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(CLIENT_VERSION))
    subparsers = parser.add_subparsers()

    # general args
    parser.add_argument('--server', metavar='url', default=BUILD_SERVER_URL_DEFAULT,
                   help='URL of the Build Server')
    parser.add_argument('-p', '--port', metavar='port', default=BUILD_SERVER_PORT_DEFAULT, type=int,
                   help='Port number the Build Server runs on')
    parser.add_argument('-u', '--user', metavar='user',
                   help='Username, will be replaced by advanced authorization')
    parser.add_argument('-F', '--file', type=argparse.FileType('r'),
                   help='JSON file with specification')

    # create the parser for the "taskstatus" command
    parser_tasks = subparsers.add_parser('tasks', help='Show all tasks')

    # create the parser for the "taskstatus" command
    parser_taskstatus = subparsers.add_parser('taskstatus', help='Show status of the task')
    parser_taskstatus.add_argument('-t', '--task', metavar='id', required=True,
                       help='ID of the task we want status for')

    # create the parser for the "images" command
    parser_images = subparsers.add_parser('images', help='Show all images')

    # create the parser for the "imageinfo" command
    parser_imageinfo = subparsers.add_parser('imageinfo', help='Show information about specified image')
    parser_imageinfo.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image we want information for')

    # create the parser for the "imagedeps" command
    parser_imagedeps = subparsers.add_parser('imagedeps', help='Show deps of specified image')
    parser_imagedeps.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image we ask for dependencies')

    # create the parser for the "new" command
    parser_new = subparsers.add_parser('new', help='Submit a new task')
    parser_new.add_argument('-g', '--git', metavar='url', required=True,
                       help='URL to git repository, excluding path')
    parser_new.add_argument('--git-path', metavar='path', required=True,
                       help='Path in the git repository')
    parser_new.add_argument('--git-commit', metavar='path', default='HEAD',
                       help='Commit in the git repository')
    parser_new.add_argument('-p', '--parent', metavar='url',
                       help='URL to registry server where parent image is pulled from')
    parser_new.add_argument('-e', '--target', metavar='url',
                       help='URL to registry server where built image is pushed to')
    parser_new.add_argument('-r', '--repo', metavar='url', nargs='*',
                       help='URL to Yum repository where to pull packages from '
                       + 'during build, but should not be available in the image')
    parser_new.add_argument('-t', '--tag', metavar='tag', nargs='*',
                       help='Tag that should be used to label built image with')
    parser_new.set_defaults(func=action_new)

    # create the parser for the "move" command
    parser_move = subparsers.add_parser('move', help='Move some image from one registry to another registry')
    parser_move.add_argument('-s', '--source', metavar='url', required=True,
                       help='URL to registry server where moving image is pulled from')
    parser_move.add_argument('-e', '--target', metavar='url', required=True,
                       help='URL to registry server where built image is pushed to')
    parser_move.add_argument('-t', '--tag', metavar='tag', nargs='*',
                       help='Tag that should be used to label built image with')
    parser_move.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image that should be moved')
    parser_move.set_defaults(func=action_move)

    # create the parser for the "rebuild" command
    parser_rebuild = subparsers.add_parser('rebuild', help='Rebuild already built image')
    parser_rebuild.add_argument('-e', '--target', metavar='url',
                       help='URL to registry server where the built image should be pushed to')
    parser_rebuild.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image that should be rebuilded')
    parser_rebuild.set_defaults(func=action_rebuild)

    # create the parser for the "invalidate" command
    parser_inv = subparsers.add_parser('invalidate', help='Invalidate all images built from specified image')
    parser_inv.add_argument('-e', '--target', metavar='url',
                       help='URL to registry server where we want to invalidate childs')
    parser_inv.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image whose childs should be invalidated')
    parser_inv.set_defaults(func=action_invalidate)

    # parse the args and call whatever function was selected
    args = parser.parse_args()

    return args.func(args)

if __name__ == '__main__':
    exit(main())


