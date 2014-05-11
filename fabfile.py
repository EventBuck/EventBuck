from fabric.api import local

def run_tests():
	local("python tests/main.py /usr/local/google_appengine /Users/didia/Documents/workspace/eventbuck-fork/")
def prepare_deploy():
	local("nosetests --with-gae")