
import os, sys

def sysExec(cmd):
	print " ".join(cmd)
	r = os.system(" ".join(cmd))
	if r != 0: sys.exit(r)


LDFLAGS = os.environ.get("LDFLAGS", "").split()

def link(outfile, infiles, options):
	options = []
	if "--weak-linking" in options:
		idx = options.index("--weak-linking")
		options[idx:idx+1] = ["-undefined", "dynamic_lookup"]

	if sys.platform == "darwin":
		sysExec(
			["libtool", "-dynamic", "-o", outfile] +
			infiles +
			options +
			LDFLAGS +
			["-lc"]
		)
	else:
		sysExec(
			["ld"] +
			["-L/usr/local/lib"] +
			infiles +
			options +
			LDFLAGS +
			["-lc"] +
			["-shared", "-o", outfile]
		)

CFLAGS = os.environ.get("CFLAGS", "").split()

def cc_single(fn, options):
	options += ["-fpic"]
	if os.path.splitext(fn)[1] == ".cpp":
		options += ["-std=c++11"]
	sysExec(["cc"] + options + CFLAGS + ["-c"] + [fn])

def cc(files, options):
	for f in files:
		cc_single(f, options)



LinkPython = False
UsePyPy = False

def get_python_linkopts():
	if LinkPython:
		if sys.platform == "darwin":
			return ["-framework", "Python"]
		else:
			return ["-lpython2.7"]
	else:
		return ["--weak-linking"]

def get_python_ccopts():
	if UsePyPy:
		return ["-I", "/usr/local/Cellar/pypy/1.9/include"]
	else:
		return [
			"-I", "/System/Library/Frameworks/Python.framework/Headers/", # mac
			"-I", "/usr/include/python2.7", # common linux/unix
		]
