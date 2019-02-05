
import os, sys

def isfloat(value):
	try:
		x = float(value)
		return x
	except ValueError:
		return None


def isint(value):
	try:
		x = int(value)
		return x
	except ValueError:
		return None

def is_float_int(value):
	if isfloat(value) != None:
		return isfloat(value)
	elif isint(value) != None:
		return isint(value)
	else:
		return None


def str2bool(v):
	if v.lower() in ("yes", "true", "t", "1"):
		return True
	elif v.lower() in ("no", "false", "f", "0"):
		return False
	else:
		return None

