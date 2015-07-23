DOT=dot
PYTHON=python

all: $(DOMAIN).pdf $(DOMAIN).png $(DOMAIN).dot

%.pdf: %.dot
	$(DOT) -Tpdf $< -o $@

%.png: %.dot
	$(DOT) -Tpng -Gsize=5,5! -Gdpi=300 $< -o $@

%.dot:
	$(PYTHON) make_dot.py $(DOMAIN) > $@

clean:
	rm -rf *.pdf *.pyc *.dot *.png

setup:
	pip install -r requirements.txt
