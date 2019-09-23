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
import os
import sys

from pynami import __version__

sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'pynami'
copyright = '2019, Sebastian Scholz'
author = 'Sebastian Scholz'

version = __version__
# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

add_module_names = False

show_authors = True

rst_prolog = """
.. |DPSG| replace:: :abbr:`DPSG (Deutsche Pfadfinderschaft Sankt Georg)`
.. |NAMI| replace:: :abbr:`NaMi (Namentliche Mitgliederverwaltung)`
.. |HTTP| replace:: :abbr:`HTTP (Hypertext Transfer Protocol)`
.. |API| replace:: :abbr:`API (Application Programming Interface)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
.. |URL| replace:: :abbr:`URL (Uniform Resource Locator)`
.. |HTML| replace:: :abbr:`HTML (Hypertext Markup Language)`
.. |CGC| replace:: certificate of good conduct
.. |VAT| replace:: :abbr:`VAT (Value added tax)`
.. |IBAN| replace:: :abbr:`IBAN (International Bank Account Number)`
.. |BIC| replace:: :abbr:`BIC (Bank Identifier Code)`
.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |PDF| replace:: :abbr:`PDF (Portable Document Format)`
.. |CSV| replace:: :abbr:`CSV (Comma-separated values)`
.. |AG| replace:: :abbr:`AG (Arbeitsgruppe)`
"""
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    # 'sphinx_autodoc_annotation',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.httpdomain',
    'sphinx-jsonschema',
    'sphinx.ext.autosectionlabel'
    # 'sphinx_autodoc_typehints',
    # 'sphinxcontrib.tikz'
]

# autosection settings
autosectionlabel_prefix_document = True

# tikz settings
tikz_tikzlibraries = 'shapes,arrows'
# tikz_proc_suite = 'pdf2svg'
# tikz_proc_suite = 'ImageMagick'
tikz_proc_suite = 'GhostScript'

# todo settings
todo_include_todos = True

# Autodoc settings
autodoc_default_options = {
    'member-order': 'bysource',
    'undoc-members': True,
    # 'inherited-members': False,
    'exclude-members': 'opts',
    'special-members': '__model__'
}

inherit_members = ['id', 'descriptor', 'representedClass']


# def maybe_skip_member(app, what, name, obj, skip, options):
#     if name in inherit_members:
#         print(what, name, obj)
#         return False
#     else:
#         return skip


# def setup(app):
#     app.connect('autodoc-skip-member', maybe_skip_member)


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'marshmallow': ('https://marshmallow.readthedocs.io/en/stable/', None),
    'requests': ('https://2.python-requests.org/en/master/', None)
}
# Keep cached intersphinx inventories indefinitely
intersphinx_cache_limit = -1

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'abbr.rst']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'pynamidoc'
