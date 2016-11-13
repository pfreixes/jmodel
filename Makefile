.PHONY: _default clean compile test


PYTHON ?= python
PYTEST ?= pytest


_default: compile


clean:
	rm -fr build/lib.* build/temp.*
	rm -fr jmodel/*.c jmodel/*.so
	find . -name '__pycache__' | xargs rm -rf


compile: clean
	$(PYTHON) setup.py build_ext --inplace


debug: clean
	$(PYTHON) setup.py build_ext --inplace --debug \
		--cython-always \
		--cython-annotate \
		--cython-directives="linetrace=True" \
		--define UVLOOP_DEBUG,CYTHON_TRACE,CYTHON_TRACE_NOGIL


test: clean compile
	PYTHONPATH=`pwd` $(PYTEST) -v tests/ut/
