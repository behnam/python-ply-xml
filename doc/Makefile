all: view

view: report.pdf
	evince $< &

edit: report.tex
	vim $<

#%.pdf: %.tex %.bib
	#bibtex $* || ( pdflatex $< && bibtex $* )
	#pdflatex $<

%.pdf: %.tex
	pdflatex $<

