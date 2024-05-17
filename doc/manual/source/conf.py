# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sys
import os
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'PDFmorph'
copyright = '2009-2019, Trustees of Columbia University in the City of New York, all rights reserved.'
author = 'Chris Farrow, Christopher J. Wright, Pavol Juhás, Chia-Hao (Timothy) Liu, S. Matthew Román, Simon J.L. Billinge'

# The full version, including alpha/beta/rc tags
release = '0.1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
import sphinx_rtd_theme
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 
	'sphinx.ext.todo', 'sphinx.ext.viewcode', 
	'sphinx.ext.intersphinx', 'm2r']
napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

from jinja2 import Template, Environment, FileSystemLoader

source_suffix = '.rst'

master_doc = 'index'

language = 'en'
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['Thumbs.db', '.DS_Store'] 

pygments_style = 'sphinx'

todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

htmlhelp_basename = 'PDFmorphdoc'

latex_documents = [
	(master_doc, 'pdfmorph.tex', 'PDFmorph Documentation', 
	'author', 'manual'),
]

man_pages = [
	(master_doc, 'pdfmorph', 'PDFmorph Documentation', [author], 1)
]

texinfo_documents = [
	(master_doc, 'PDFmorph', 'PDFmorph Documentation', author,
	'PDFmorph', 'One line description of project.', 'Miscellaneous'),
]

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

epub_exclude_files = ['search.html']
