
all: ctags test
test:
	clear
	#./parser.py samples/sample-3.xml
	#./parser.py samples/sample-4.xml
	./parser.py samples/sample-5.xml

ctags:
	ctags -R .

clean:
	rm -f tags *.out
	find -name '*.pyc' | xargs rm -f
	rm -f parsetab.py

