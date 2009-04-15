
all: ctags test

test:
	./parser.py samples/sample-1.xml | tee samples/sample-1.out
	./parser.py samples/sample-2.xml | tee samples/sample-2.out

ctags:
	ctags -R .

clean:
	rm -f tags *.out
	find -name '*.pyc' | xargs rm -f
	rm -f parsetab.py
	rm -f samples/*.out

