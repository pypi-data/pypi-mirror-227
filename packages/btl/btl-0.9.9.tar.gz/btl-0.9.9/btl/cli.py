#!/usr/bin/python
import os
import sys
import argparse
from btl import ToolDB, Tool, Library, serializers
from btl.shape import Shape

try:
    import FreeCAD
except ImportError:
    sys.stderr.write('error: FreeCAD not found. Make sure to include it in your PYTHONPATH')
    sys.exit(1)

def select_library(libraries):
    # No need to choose if there's just one.
    if len(libraries) == 1:
        return libraries[0]

    # Print the list of libraries including a number.
    libraries = list(enumerate(sorted(libraries, key=lambda l: l.label), start=1))
    default = None
    for n, lib in libraries:
        if lib.label == 'Default':
            default = n
        print('{}) {}{}'.format(n, lib.label, '*' if lib.label == 'Default' else ''))

    # Let the user choose.
    while True:
        try:
            selection = int(input('Please select the library number [{}]'.format(default)) or 1)
        except ValueError:
            continue
        return libraries[selection-1][1]

def get_libraries(db, name):
    if args.library == 'all':
        return db.get_libraries()
    try:
        return [db.get_library_by_id(name)]
    except KeyError:
        return []

def create_tool(shape_name):
    try:
        shape = Shape(shape_name)
    except OSError:
        sys.stderr.write('Shape "{}" not found. Supported built-in shapes: {}'.format(
            shape_name,
            Shape.builtin
        ))
        sys.exit(1)

    # Reading the shape file requires the FreeCAD Python module to be installed.
    try:
        properties = shape.get_properties()
    except ImportError:
        sys.stderr.write('error: FreeCAD Python module not found.' \
                       + ' Make sure it is installed and in your PYTHONPATH')
        sys.exit(1)

    # Ask for mandatory base parameters.
    label = input('Please enter a tool name (label): ')
    tool = Tool(label, shape)

    # Ask for tool-specific parameters as extracted from the shape file.
    print('Please enter the tool parameters (enter accepts default).')
    for group, propname, value, unit, enum in properties:
        enum_msg = 'Allowed values: ' + ', '.join(enum) if enum else ''
        msg = '{}/{} Unit is {}. {} [{}]: '.format(group, propname, unit, enum_msg, value)
        while True:
            val = input(msg) or value
            if enum and val not in enum:
                continue
            break
        tool.set_param(propname, val)

    return tool

parser = argparse.ArgumentParser(
    prog=__file__,
    description='CLI tool to manage a tool library'
)

# Common arguments
parser.add_argument('-f', '--format',
                    help='the type (format) of the library',
                    choices=sorted(serializers.serializers.keys()),
                    default='freecad')
parser.add_argument('name',
                    help='the DB name. In case of a file based DB, this is the path to the DB')
subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')

# "ls" command arguments
lsparser = subparsers.add_parser('ls', help='list objects')
lsparser.add_argument('objects',
                      help='which DB object to work with',
                      nargs='*',
                      choices=['all', 'libraries', 'tools'])

# "show" command arguments
lsparser = subparsers.add_parser('show', help='list objects with details')
lsparser.add_argument('-b', '--builtin', action='store_true', help='also show built-in shapes')
lsparser.add_argument('-s', '--summarize', action='store_true', help='summarize tool parameters')
lsparser.add_argument('objects',
                      help='which DB object to work with',
                      nargs='*',
                      choices=['all', 'libraries', 'tools'])

# "export" command arguments
exportparser = subparsers.add_parser('export', help='export tools and libraries in a defined format')
exportparser.add_argument('-f', '--format',
                          dest='output_format',
                          help='target format',
                          choices=sorted(serializers.serializers.keys()),
                          required=True)
exportparser.add_argument('output',
                          help='the output DB name. In case of a file based DB, this is the path to the DB')

# "create" command arguments
createparser = subparsers.add_parser('create', help='create tools or libraries')
createsubparsers = createparser.add_subparsers(dest='object', metavar='OBJECT')

createtoolparser = createsubparsers.add_parser('tool', help='create a new tool')
createtoolparser.add_argument('shape', help='the type of tool. may be built-in shape, or a filename')

createlibraryparser = createsubparsers.add_parser('library', help='create a new library')
createlibraryparser.add_argument('name', help='the name of the library')

# "remove" command arguments
removeparser = subparsers.add_parser('remove', help='remove tools or libraries')
removesubparsers = removeparser.add_subparsers(dest='object', metavar='OBJECT')

removetoolparser = removesubparsers.add_parser('tool', help='remove the tool from the given library')
removetoolparser.add_argument('library', help='the library id, or "all"')
removetoolparser.add_argument('tool', help='the tool id, or "all"')

removelibraryparser = removesubparsers.add_parser('library', help='remove the library')
removelibraryparser.add_argument('library', help='the library id, or "all"')

def run():
    args = parser.parse_args()

    serializer_cls = serializers.serializers[args.format]
    serializer = serializer_cls(args.name)
    db = ToolDB()
    db.deserialize(serializer)

    if args.command == 'ls':
        if 'all' in args.objects or 'libraries' in args.objects:
            for lib in db.libraries.values():
                print(lib)
        if 'all' in args.objects or 'tools' in args.objects:
            for tool in db.tools.values():
               print(tool)

    elif args.command == 'show':
        if 'all' in args.objects:
            db.dump(summarize=args.summarize, builtin=args.builtin)
        if 'libraries' in args.objects:
            for library in db.get_libraries():
                library.dump(summarize=args.summarize)
        if 'tools' in args.objects:
            for tool in db.get_tools():
                tool.dump(summarize=args.summarize)

    elif args.command == 'export':
        print("Exporting as {}".format(args.output_format))
        output_serializer_cls = serializers.serializers[args.output_format]
        output_serializer = output_serializer_cls(args.output)
        db.serialize(output_serializer)

    elif args.command == 'create':
        if args.object == 'tool':
            library = select_library(db.get_libraries())
            print('Tool will be added to library "{}".'.format(library.label))

            tool = create_tool(args.shape)
            db.add_tool(tool, library=library)
            library.serialize(serializer)
            print("Tool id is {}.".format(tool.id))
        elif args.object == 'library':
            library = Library(createlibraryparser.name)
            library.serialize(serializer)
        else:
            parser.error('requested unsupported object: {}'.format(args.object))
            db.serialize(serializer)

    elif args.command == 'remove':
        if args.object == 'tool':
            try:
                tool = db.get_tool_by_id(args.tool)
            except KeyError:
                removetoolparser.error('Tool with ID {} not found.'.format(args.tool))
            try:
                libraries = get_libraries(db, args.library)
            except KeyError:
                removetoolparser.error('Library with ID {} not found.'.format(args.library))
            for library in libraries:
                print('Removing tool {} from library "{}".'.format(tool.id, library.label))
                library.remove_tool(tool)
            if args.library == 'all':
                print('Removing tool from DB.')
                db.remove_tool(tool)
            elif args.object == 'library':
                for library in get_libraries(db, args.library):
                    print('Removing library "{}".'.format(library.label))
                    db.remove_library(library)
        else:
            parser.error('requested unsupported object: {}'.format(args.object))
            db.dump()
            db.serialize(serializer)

    else:
        print("no command given, nothing to do")

if __name__ == '__main__':
    run()
