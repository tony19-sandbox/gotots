#!/bin/python
########################################################################
#  gotots 0.1.0
#
#  usage: go_to_ts.py [-h] [-d OUTDIR] input [input ...]
#
#  Converts Go structs into TypeScript classes
#
#  positional arguments:
#    input                 path to input file (Go)
#
#  optional arguments:
#    -h, --help            show this help message and exit
#    -d OUTDIR, --outdir OUTDIR
#                          path to output directory
#
########################################################################

import argparse
import os
import re
import random

_verbose = False


def _args():
    """
    Parses command-line arguments
    :return: the args
    """
    parser = argparse.ArgumentParser(description='Converts Go structs into TypeScript classes')
    parser.add_argument('-d', '--outdir',
                        help='path to output directory')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='print debug info while parsing')
    parser.add_argument('input',
                        nargs='+',
                        help='path to input file (Go)')
    return parser.parse_args()


def _xprint(args):
    if _verbose:
        print args


class TypeScriptClassWriter(object):

    def _go_type_to_ts_type(self, gotype):
        """
        Converts the name of a Go type into an equivalent TypeScript type name
        :param gotype: the Go type to convert
        :return: the corresponding TypeScript type (the original input)
        """
        if gotype in ['int32', 'uint32', 'int', 'uint']:
            return 'number'
        elif gotype.startswith('[]'):
            return gotype[2:] + '[]'
        elif gotype.startswith('*'):
            return gotype[1:]
        else:
            return gotype


    def _to_dash_name(self, filename):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', filename)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


    def write_class(self, outdir, info):
        """
        Writes TypeScript class based on given info
        :param outdir: path to output directory
        :param info: Go class info
        """
        path = os.path.join(outdir, self._to_dash_name(info['classname']) + '.ts')

        outputlines = [
            'import { JsonMember, JsonObject } from \'type-json\'',
            '\n',
            '@JsonObject',
            'export class %s {' % info['classname'],
            '\n',
        ]
        with open(path, 'w') as output:
            output.write('\n'.join(outputlines))
            for f in info['fields']:
                name = f['name']
                name = name[0].lower() + name[1:]
                type = self._go_type_to_ts_type(f['type'])
                optional = f['optional'] and ' // optional' or ''

                lines = [
                    '  @JsonMember({name: \'%s\'})' % f['json'],
                    '  public %s: %s;%s' % (name, type, optional),
                    '\n'
                ]
                output.write('\n'.join(lines))

            output.write('}\n')


    def write_enum(self, outdir, enum):
        path = os.path.join(outdir, self._to_dash_name(enum['type']) + '.ts')
        with open(path, 'w') as output:
            output.write('export enum %s {\n' % enum['type'])
            for f in enum['enum']:
                output.write('  %s,\n' % f)
            output.write('}\n')


class GoFileParser(object):

    def __init__(self):
        self.re_class = re.compile(r'type (?P<class>[^\s]+) struct')
        self.re_field = re.compile(r'(?P<field>[^\s]+)\s+(?P<type>[^\s]+)\s+`json:"(?P<json>[^," ]+)(?P<optional>,omitempty)?"`')
        self.re_enum_open = re.compile(r'^\s*const \(\s*')
        self.re_enum_item = re.compile(r'\s*(?P<enum>[^\s]+)\s+(?P<type>[^\s=]+)?(\s+=.*)?$')
        self.re_enum_close = re.compile(r'\s*\)\s*$')


    def parse(self, path):
        """
        Parses Go class info
        :param path: path to input file
        :return: a list of class info
        """
        with open(path, 'r') as input:
            classlist = []
            enumlist = []
            info = {}
            enum = {}
            in_enum = False

            for line in input:
                m = self.re_class.search(line)
                if m:
                    classname = m.group('class')
                    _xprint('new class: ' + classname)
                    info = {
                        'classname': classname,
                        'fields': []
                    }
                    classlist.append(info)

                m = self.re_field.search(line)
                if m:
                    field = {}
                    field['name'] = m.group('field')
                    field['type'] = m.group('type')
                    field['json'] = m.group('json')
                    field['optional'] = m.group('optional')
                    info['fields'].append(field)
                    _xprint('new field: %s' % field)

                m = self.re_enum_open.search(line)
                if m:
                    in_enum = True
                    enum = {}
                    enum['enum'] = []
                    _xprint('open enum')

                elif in_enum:
                    m = self.re_enum_close.search(line)
                    if m:
                        _xprint('closing enum: %s' % in_enum)
                        in_enum = False
                        enumlist.append(enum)
                        enum = {}

                    else:
                        m = self.re_enum_item.search(line)
                        if m:
                            if 'type' not in enum:
                                enum['type'] = m.group('type') or ('anon-' + random.randint())
                                _xprint('enum type: %s' % enum['type'])

                            enum['enum'].append(m.group('enum'))
                            in_enum = enum['type']
                            _xprint('enum: %s' % m.group('enum'))

        return classlist, enumlist


def _main():
    args = _args()
    global _verbose
    _verbose = args.verbose

    reader = GoFileParser()
    writer = TypeScriptClassWriter()

    for input in args.input:
        classlist, enumlist = reader.parse(input)
        if not classlist and not enumlist:
            print 'no classes found in: %s' % input
        else:
            for clazz in classlist:
                writer.write_class(args.outdir, clazz)

            for enum in enumlist:
                writer.write_enum(args.outdir, enum)


if __name__ == '__main__':
    _main()
