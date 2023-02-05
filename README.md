### Hexlet tests and linter status:
[![Actions Status](https://github.com/seeu359/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/seeu359/python-project-83/actions)
[![pytest-check](https://github.com/seeu359/python-project-83/actions/workflows/linter_check.yml/badge.svg)](https://github.com/seeu359/python-project-83/actions/workflows/linter_check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/7b11052e4e21e418e0f3/maintainability)](https://codeclimate.com/github/seeu359/python-project-83/maintainability)

### Description

A site that analyzes said pages for SEO suitability similar to varvy

---

### Installation

1. Clone repo: ``$ git clone https://github.com/seeu359/python-project-83``
2. Go to the directory with code: ``$ cd python-project-83``
3. Install the dependencies:
   1. If you're using poetry, run command: ``$ make p_install``
   2. Else: ``$ make install``

### Environment variables:

DATABASE_URL = postgresql://{username}:{password}@{host}:{port}/{db_name}
SECRET_KEY=
