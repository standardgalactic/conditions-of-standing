.PHONY: pdf check clean
pdf:
	latexmk -pdf -interaction=nonstopmode main.tex
check:
	./examples/check.sh
clean:
	latexmk -C
