.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/cds-portal.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/cds-portal
    .. image:: https://readthedocs.org/projects/cds-portal/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://cds-portal.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/cds-portal/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/cds-portal
    .. image:: https://img.shields.io/pypi/v/cds-portal.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/cds-portal/
    .. image:: https://img.shields.io/conda/vn/conda-forge/cds-portal.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/cds-portal
    .. image:: https://pepy.tech/badge/cds-portal/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/cds-portal
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/cds-portal

Cosmic Data Stories Portal
==========================

The portal for the Cosmic Data Stories project acts as the front-end for educators and students to manager their class
associations and available active data stories.

Usage
-----

To run the project locally, clone the repository and install using

.. code-block:: bash

   pip install cds-portal

Then, run the following command to start the server:

.. code-block:: bash

   SOLARA_SESSION_SECRET_KEY="..." SOLARA_OAUTH_CLIENT_ID="..." SOLARA_OAUTH_CLIENT_SECRET="..."
   SOLARA_OAUTH_API_BASE_URL="..." SOLARA_OAUTH_SCOPE="openid profile email" SOLARA_SESSION_HTTPS_ONLY=false
   CDS_API_KEY="..." solara run cds_portal.pages --port=8865