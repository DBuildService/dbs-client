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
    s={'server':'server', 'port':'port'}
    s.update(args)
    return s


def _get_specified(args, fields):
    d=vars(args)
    return dict((nameout, d[namein]) for nameout, namein in _get_copied(fields).iteritems() if d[namein] is not None)


def _print_nice(s):
    print(json.dumps(s, indent=4, sort_keys=True))


# sub-command functions
def action_new(args):
    if args.file:
        return subcommands.action_new(data=args.file.read())
    payload = _get_specified(args, {'git_url':'git_url',
                                    'git_dockerfile_path':'git_dockerfile_path',
                                    'git_commit':'git_commit',
                                    'parent_registry':'parent_registry',
                                    'target_registries':'target_registries',
                                    'repos':'repos',
                                    'tag':'tag'})
    output = subcommands.action_new(args=payload)
    _print_nice(output)
    return True


def action_move(args):
    if args.file:
        return subcommands.action_move(data=args.file.read())
    payload = _get_specified(args, {'source_registry':'source_registry',
                                    'target_registry':'target_registry',
                                    'tags':'tags',
                                    'image':'image'})
    output = subcommands.action_move(args=payload)
    _print_nice(output)
    return True


def action_invalidate(args):
    if args.file:
        return subcommands.action_invalidate(data=args.file.read())
    payload = _get_specified(args, {'target_registries':'target_registries',
                                    'image':'image'})
    output = subcommands.action_invalidate(args=payload)
    _print_nice(output)
    return True


def action_rebuild(args):
    if args.file:
        return subcommands.action_rebuild(data=args.file.read())
    payload = _get_specified(args, {'target_registries':'target_registries',
                                    'image':'image'})
    output = subcommands.action_rebuild(args=payload)
    _print_nice(output)
    return True


def action_tasks(args):
    if args.file:
        return subcommands.action_tasks(data=args.file.read())
    payload = _get_specified(args, {})
    output = subcommands.action_tasks(args=payload)
    _print_nice(output)
    return True


def action_taskstatus(args):
    if args.file:
        return subcommands.action_taskstatus(data=args.file.read())
    payload = _get_specified(args, {'task':'task'})
    output = subcommands.action_taskstatus(args=payload)
    _print_nice(output)
    return True


def action_images(args):
    if args.file:
        return subcommands.action_images(data=args.file.read())
    payload = _get_specified(args, {})
    output = subcommands.action_images(args=payload)
    _print_nice(output)
    return True


def action_imageinfo(args):
    if args.file:
        return subcommands.action_imageinfo(data=args.file.read())
    payload = _get_specified(args, {'image':'image'})
    output = subcommands.action_imageinfo(args=payload)
    _print_nice(output)
    return True


def action_imagestatus(args):
    if args.file:
        return subcommands.action_imagestatus(data=args.file.read())
    payload = _get_specified(args, {'image':'image'})
    output = subcommands.action_imagestatus(args=payload)
    _print_nice(output)
    return True


def action_imagedeps(args):
    if args.file:
        return subcommands.action_imagedeps(data=args.file.read())
    payload = _get_specified(args, {'image':'image'})
    output = subcommands.action_imagedeps(args=payload)
    _print_nice(output)
    return True


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Client for lightweight communication with DBS server.',
                                 epilog="This is an open-source project by Red Hat.")
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(CLIENT_VERSION))
    subparsers = parser.add_subparsers()

    # general args
    parser.add_argument('--server', metavar='url', default=BUILD_SERVER_URL_DEFAULT,
                   help='URL of the Build Server')
    parser.add_argument('-p', '--port', metavar='port', type=int,
                   help='Port number the Build Server runs on')
    parser.add_argument('-u', '--user', metavar='user',
                   help='Username, will be replaced by advanced authorization')
    parser.add_argument('-F', '--file', type=argparse.FileType('r'),
                   help='JSON file with specification')

    # create the parser for the "taskstatus" command
    parser_tasks = subparsers.add_parser('tasks', help='Show all tasks')
    parser_tasks.set_defaults(func=action_tasks)

    # create the parser for the "taskstatus" command
    parser_taskstatus = subparsers.add_parser('taskstatus', help='Show status of the task')
    parser_taskstatus.add_argument('-t', '--task', metavar='id', required=True,
                       help='ID of the task we want status for')
    parser_taskstatus.set_defaults(func=action_taskstatus)

    # create the parser for the "images" command
    parser_images = subparsers.add_parser('images', help='Show all images')
    parser_images.set_defaults(func=action_images)

    # create the parser for the "imageinfo" command
    parser_imageinfo = subparsers.add_parser('imageinfo', help='Show information about specified image')
    parser_imageinfo.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image we want information for')
    parser_imageinfo.set_defaults(func=action_imageinfo)

    # create the parser for the "imagestatus" command
    parser_imagestatus = subparsers.add_parser('imagestatus', help='Show status information about specified image')
    parser_imagestatus.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image we want information for')
    parser_imagestatus.set_defaults(func=action_imagestatus)

    # create the parser for the "imagedeps" command
    parser_imagedeps = subparsers.add_parser('imagedeps', help='Show deps of specified image')
    parser_imagedeps.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image we ask for dependencies')
    parser_imagedeps.set_defaults(func=action_imagedeps)

    # create the parser for the "new" command
    parser_new = subparsers.add_parser('new', help='Submit a new task')
    parser_new.add_argument('-g', '--git-url', metavar='url', required=True,
                       help='URL to git repository, excluding path')
    parser_new.add_argument('--git-dockerfile-path', metavar='path', required=False,
                       help='Path in the git repository')
    parser_new.add_argument('--git-commit', metavar='path', default='HEAD',
                       help='Commit in the git repository')
    parser_new.add_argument('-p', '--parent-registry', metavar='url',
                       help='URL to registry server where parent image is pulled from')
    parser_new.add_argument('-e', '--target-registries', metavar='url', nargs='*',
                       help='URL to registry server where built image is pushed to')
    parser_new.add_argument('-r', '--repos', metavar='url', nargs='*',
                       help='URL to Yum repository where to pull packages from '
                       + 'during build, but should not be available in the image')
    parser_new.add_argument('-t', '--tag', metavar='tag',
                       help='Tag that should be used to label built image with')
    parser_new.set_defaults(func=action_new)

    # create the parser for the "move" command
    parser_move = subparsers.add_parser('move', help='Move some image from one registry to another registry')
    parser_move.add_argument('-s', '--source-registry', metavar='url', required=True,
                       help='URL to registry server where moving image is pulled from')
    parser_move.add_argument('-e', '--target-registry', metavar='url', required=True,
                       help='URL to registry server where built image is pushed to')
    parser_move.add_argument('-t', '--tags', metavar='tag', required=True, nargs='*',
                       help='Tag that should be used to label built image with')
    parser_move.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image that should be moved')
    parser_move.set_defaults(func=action_move)

    # create the parser for the "rebuild" command
    parser_rebuild = subparsers.add_parser('rebuild', help='Rebuild already built image')
    parser_rebuild.add_argument('-e', '--target-registries', metavar='url', nargs='*',
                       help='URL to registry server where the built image should be pushed to')
    parser_rebuild.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image that should be rebuilded')
    parser_rebuild.set_defaults(func=action_rebuild)

    # create the parser for the "invalidate" command
    parser_inv = subparsers.add_parser('invalidate', help='Invalidate all images built from specified image')
    parser_inv.add_argument('-e', '--target-registries', metavar='url', nargs='*',
                       help='URL to registry server where we want to invalidate childs')
    parser_inv.add_argument('-i', '--image', metavar='id', required=True,
                       help='ID of the image whose childs should be invalidated')
    parser_inv.set_defaults(func=action_invalidate)

    # parse the args and call whatever function was selected
    args = parser.parse_args()

    return args.func(args)

if __name__ == '__main__':
    if main():
        exit(0)
    else:
        exit(1)


