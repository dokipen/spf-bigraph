DOT = dot
PYTHON = python
BUILDDIR = build
WORKDIR = work
STATICDIR = static
STATICSRC := $(shell find $(STATICDIR) -type f)
STATICDST := $(patsubst $(STATICDIR)/%, $(BUILDDIR)/%, $(STATICSRC))

all: $(BUILDDIR)/docs/$(DOMAIN).pdf $(BUILDDIR)/images/$(DOMAIN).png $(WORKDIR)/$(DOMAIN).dot $(BUILDDIR)/data/$(DOMAIN).json $(BUILDDIR)/js/index.js $(STATICDST)
static: $(BUILDDIR)/index.html

.PHONY: phony

$(BUILDDIR)/docs/%.pdf: $(WORKDIR)/%.dot
	mkdir -p $(BUILDDIR)/docs
	$(DOT) -Tpdf $< -o $@

$(BUILDDIR)/images/%.png: $(WORKDIR)/%.dot
	mkdir -p $(BUILDDIR)/images
	$(DOT) -Tpng -Gsize=5,5! -Gdpi=300 $< -o $@

$(WORKDIR)/%.dot: phony
	mkdir -p $(WORKDIR)
	$(PYTHON) src/gen.py $(DOMAIN) > $@

$(BUILDDIR)/js/index.js: phony
	mkdir -p $(BUILDDIR)/js
	$(PYTHON) src/index.py $(BUILDDIR)/data > $@

$(BUILDDIR)/data/%.json: phony
	mkdir -p $(BUILDDIR)/data
	FORMAT=json $(PYTHON) src/gen.py $(DOMAIN) > $@

build/%: static/%
	mkdir -p $(dir $@)
	ln -s $(PWD)/$< $@

clean:
	rm -rf $(BUILDDIR) $(WORKDIR)

setup:
	pip install -r requirements.txt

serve:
	cd $(BUILDDIR) && python -m SimpleHTTPServer
