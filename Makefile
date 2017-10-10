
# CentOS doesn't have a /usr/bin/pylint3, so we give --which-python-3 to this-pylint instead of --which-3.

py_files=$(shell echo *.py)
base_url=https://scorpius-gead.grokstream.com

interval=300

# This is good for during development, but the actual problem statement wants every 5 minutes (AKA 300 seconds)
# interval=10

go: run-real-thing
	/bin/true

go2: run-test-every-n-seconds
	/bin/true

run-test-every-n-seconds:
	./this-pylint \
		--which-python-2 /usr/bin/python \
		--which-python-3 /usr/bin/python3 \
		--to-pylint test-every-n-seconds every_n_seconds.py
	pep8 test-every-n-seconds every_n_seconds.py
	/usr/bin/python3 test-every-n-seconds
	/usr/bin/python test-every-n-seconds
	
run-real-thing:
	# This is the Python version
	./this-pylint \
		--which-python-2 /usr/bin/python \
		--which-python-3 /usr/bin/python3 \
		--to-pylint ${py_files}
	pep8 ${py_files}
	/usr/bin/python ./real_thing.py \
		--tenacious \
		--source-name perfect-squares \
		--interval ${interval} \
		--base-url ${base_url}
#	/usr/bin/python3 ./real_thing.py \
#		--max-iterations 10 \
#		--tenacious \
#		--source-name perfect-squares \
#		--interval ${interval} \
#		--base-url ${base_url}
	# /usr/bin/python3 ./real_thing.py \
	# 	--max-iterations 10 \
	# 	--source-name perfect-squares \
	# 	--interval ${interval} \
	# 	--base-url ${base_url}
	# /usr/bin/python ./real_thing.py \
	# 	--max-iterations 10 \
	# 	--source-name perfect-squares \
	# 	--interval ${interval} \
	# 	--base-url ${base_url}

run-curl-test:
	# This is a sort of prototype in bash, using curl
	bash -n curl-test
	./curl-test

add-dependencies:
	./os-packages
	pip2.7 install -r requirements.txt
	pip3 install -r requirements.txt

doc-preview:
	markdown_py README.md > README.html
	links -dump file://README.html

clean:
	rm -rf __pycache__
	rm -f *.pyc README.html

