#!/usr/bin/env python3
#
#  latex_layout.py
"""
Makes minor adjustments to the LaTeX layout.

* Increases the whitespace above function signatures by 5px,
  to prevent the function visually merging with the previous one.
* Remove unnecessary indentation and allow "raggedright" for the fields in
  the body of functions, which prevents ugly whitespace and line breaks.
* Disables justification for function signatures.
  This is a backport of changes from Sphinx 4 added in :github:pull:`8997 <sphinx-doc/sphinx>`.

  .. versionadded:: 2.12.0

.. versionadded:: 2.10.0
.. extensions:: sphinx_toolbox.tweaks.latex_layout

-----

"""  # noqa: D400
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# 3rd party
from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.writers.latex import LaTeXTranslator

# this package
from sphinx_toolbox.utils import SphinxExtMetadata, metadata_add_version

__all__ = ["setup"]


def visit_desc(translator: LaTeXTranslator, node: addnodes.desc) -> None:
	translator.body.append('\n\n\\vspace{5px}')
	LaTeXTranslator.visit_desc(translator, node)


def visit_field_list(translator: LaTeXTranslator, node: nodes.field_list) -> None:
	translator.body.append('\\vspace{10px}\\begin{flushleft}\\begin{description}\n')
	if translator.table:  # pragma: no cover
		translator.table.has_problematic = True


def depart_field_list(translator: LaTeXTranslator, node: nodes.field_list) -> None:
	translator.body.append('\\end{description}\\end{flushleft}\\vspace{10px}\n')


def configure(app: Sphinx, config: Config):
	"""
	Configure Sphinx Extension.

	:param app: The Sphinx application.
	:param config:
	"""

	if not hasattr(config, "latex_elements"):  # pragma: no cover
		config.latex_elements = {}  # type: ignore

	latex_elements = (config.latex_elements or {})

	latex_preamble = latex_elements.get("preamble", '')

	# Backported from Sphinx 4
	# See https://github.com/sphinx-doc/sphinx/pull/8997
	config.latex_elements["preamble"] = '\n'.join([
			latex_preamble,
			r"\makeatletter",
			'',
			r"\renewcommand{\py@sigparams}[2]{%",
			r"  \parbox[t]{\py@argswidth}{\raggedright #1\sphinxcode{)}#2\strut}%",
			"  % final strut is to help get correct vertical separation in case of multi-line",
			"  % box with the item contents.",
			'}',
			r"\makeatother",
			])


@metadata_add_version
def setup(app: Sphinx) -> SphinxExtMetadata:
	"""
	Setup :mod:`sphinx_toolbox.tweaks.latex_layout`.

	:param app: The Sphinx application.
	"""

	app.connect("config-inited", configure)

	app.add_node(addnodes.desc, latex=(visit_desc, LaTeXTranslator.depart_desc), override=True)
	app.add_node(nodes.field_list, latex=(visit_field_list, depart_field_list), override=True)

	return {"parallel_read_safe": True}
