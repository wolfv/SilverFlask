# do nothing on default
default:

.PHONY: freeze requirements clean

clean:
	find . -name '*~' -delete
	find . -name '*.pyc' -delete
	find * -type d -empty -delete

#
# PIP/Libs
#

# save current requirements
freeze:
	pip freeze -r requirements.txt | sort -f > requirements.txt

# install requirements
requirements: requirements.txt
	pip install -r requirements.txt
