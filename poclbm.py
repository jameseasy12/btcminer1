#!/usr/bin/python

import pyopencl as cl
from time import sleep
from BitcoinMiner import *
from optparse import OptionParser
import json

parser = OptionParser(version=USER_AGENT)
parser.add_option('-u', '--user',     dest='user',     default='bitcoin',   help='user name')
parser.add_option('--pass',	          dest='password', default='password',  help='password')
parser.add_option('-o', '--host',     dest='host',     default='127.0.0.1', help='RPC host (without \'http://\')')
parser.add_option('-p', '--port',     dest='port',     default='8332',      help='RPC port', type='int')
parser.add_option('-r', '--rate',     dest='rate',     default=1,           help='hash rate display interval in seconds, default=1', type='float')
parser.add_option('-f', '--frames',   dest='frames',   default=30,          help='will try to bring single kernel execution to 1/frames seconds, default=30, increase this for less desktop lag', type='int')
parser.add_option('-d', '--device',   dest='device',   default=-1,          help='use device by id, by default asks for device', type='int')
parser.add_option('-a', '--askrate',  dest='askrate',  default=5,           help='how many seconds between getwork requests, default 5, max 10', type='int')
parser.add_option('-w', '--worksize', dest='worksize', default=-1,          help='work group size, default is maximum returned by opencl', type='int')
parser.add_option('-v', '--vectors',  dest='vectors',  action='store_true', help='use vectors')
parser.add_option('--verbose',        dest='verbose',  action='store_true', help='verbose output, suitable for redirection to log file')
parser.add_option('--platform',       dest='platform', default=-1,          help='use platform by id', type='int')
parser.add_option('-c', '--config',   dest='config',   default='',          help='config file')
(options, args) = parser.parse_args()

if options.config:
	f = open(options.config)
	conf = json.load(f)
	f.close()

	if conf['user']:
		options.user = conf['user']
	if conf['pass']:
		options.password = conf['pass']
	if conf['host']:
		options.host = conf['host']
	if conf['port']:
		options.port = int(conf['port'])
	if conf['rate']:
		options.rate = float(conf['rate'])
	if conf['frames']:
		options.frames = int(conf['frames'])
	if conf['device'] >= 0:
		options.device = int(conf['device'])
	if conf['askrate']:
		options.askrate = int(conf['askrate'])
	if conf['worksize']:
		options.worksize = int(conf['worksize'])
	if conf['vectors']:
		options.vectors = bool(conf['vectors'])
	if conf['platform']:
		options.platform = int(conf['platform'])

if not -1 < options.port < 0xFFFF:
	print 'invalid port'
	sys.exit()

platforms = cl.get_platforms()


if options.platform >= len(platforms) or (options.platform == -1 and len(platforms) > 1):
	print 'Wrong platform or more than one OpenCL platforms found, use --platform to select one of the following\n'
	for i in xrange(len(platforms)):
		print '[%d]\t%s' % (i, platforms[i].name)
	sys.exit()

if options.platform == -1:
	options.platform = 0

devices = platforms[options.platform].get_devices()
if (options.device == -1 or options.device >= len(devices)):
	print 'No device specified or device not found, use -d to specify one of the following\n'
	for i in xrange(len(devices)):
		print '[%d]\t%s' % (i, devices[i].name)
	sys.exit()

miner = None
try:
	miner = BitcoinMiner(	devices[options.device],
							options.host,
							options.user,
							options.password,
							options.port,
							options.frames,
							options.rate,
							options.askrate,
							options.worksize,
							options.vectors,
							options.verbose)
	miner.mine()
except KeyboardInterrupt:
	print '\nbye'
finally:
	if miner: miner.exit()
sleep(1.1)
