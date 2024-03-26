#!/usr/bin/env python3

import sys
import os
import operator
import argparse
import jinja2

class ParseError(Exception): ...

def parseArgs():
	parser = argparse.ArgumentParser(prog='mermaid_reshuffle.py',description='Mermaid reshuffler')
	parser.add_argument(
		'-i',
		'--input-file',
		metavar='input_file',
		required=True
	)
	parser.add_argument(
		'-o',
		'--output-file',
		metavar='output_file',
		required=True
	)
	parser.add_argument(
		'-t',
		'--target',
		metavar='target',
		required=False,
		default='a'
	)
	parser.add_argument(
		'-s',
		'--shift',
		metavar='shift',
		required=True
	)
	parser.add_argument(
		'-u',
		'--use-spaces',
		action='store_true'
	)
	parser.add_argument(
		'-b',
		'--backwards',
		action='store_true'
	)
	parser.add_argument(
		'-n',
		'--negative-shuffle',
		action='store_true'
	)
	return parser.parse_args()

def getindex_digit(line: str):
	for i, char in enumerate(line):
		if char.isdigit():
			return i
	return len(line)

def tuple_from_string(letters):
	return tuple(ord(i)-96 for i in letters)

def string_from_tuple(ob: tuple):
	return ''.join(chr(i+96) for i in ob)

def parse_line(line: str):
	start = len(line) - len(line.lstrip(' \t'))
	space = line[:start]
	nline = []
	equiv = {}
	for i in line[start:].split('-->'):
		offset = 0
		if i.lstrip(' \t') == '' or i[:1].isupper():
			nline.append(i)
			continue
		elif i.startswith('|'):
			offset = i[1:].find('|')+2
		offset += len(i[offset:]) - len(i[offset:].lstrip())
		limit = offset + getindex_digit(i[offset:].rstrip().replace('{',' ').replace('[',' ').split()[0])
		if i[offset:limit].lower() != i[offset:limit]:
			nline.append(i)
			continue

		equiv[tuple_from_string(i[offset:limit])] = i[offset:limit]

		i = i[:offset] + '{{ ' + i[offset:limit] + ' }}' + i[limit:]
		nline.append(i)
	return equiv,'{}{}'.format(space,'-->'.join(nline))

def parse_file(fname: str):
	template = []
	equiv = {}
	with open(fname,'r') as conf_file:
		flow = conf_file.readline().rstrip('\n')
		if not flow.startswith('flowchart'):
			raise ParseError('Invalid flowchart file: {}'.format(fname))
		for i in conf_file.readlines():
			i = i.rstrip('\n')
			if all(not i.lstrip(' \t').startswith(j) for j in ('subgraph','direction','end')) and i != '':
				e,t = parse_line(i)
				template.append(t)
				equiv.update(e)
				continue
			template.append(i)
	template.insert(0,flow)
	return equiv,'\n'.join(template)

def shuffle(tup,target,shift,args):
	op = operator.add
	if args.backwards and tup > target:
		return tup
	elif tup < target:
		return tup
	elif args.negative_shuffle:
		op = operator.sub
	return tuple(map(op, tup,shift))

def to_file(template,equiv,args):
	target = tuple_from_string(args.target)
	shift = tuple_from_string(args.shift)
	with open(args.output_file,'w') as fd:
		fd.write(template.render(**{
			k:string_from_tuple(shuffle(i,target,shift,args)) for i,k in equiv.items()
		}))

def main():
	args = parseArgs()
	if not args.target.isalpha():
		print('Target must only contain letters')
		return
	elif not args.shift.isalpha():
		print('Shifting valute must only contain letters')
	try:
		equiv,raw_template = parse_file(args.input_file)
	except ParseError as e:
		print(e)
	except FileNotFoundError:
		print('No input file present')
		return
	to_file(
		jinja2.Environment().from_string(raw_template),
		equiv,
		args
	)


if __name__ == '__main__':
	main()
