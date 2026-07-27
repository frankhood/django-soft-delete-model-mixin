.. :changelog:

History
-------

1.0.0 (2026-07-27)
++++++++++++++++++

* First release declaring a verified compatibility matrix: Django 4.2, 5.0, 5.1, 5.2 and
  Python 3.8-3.14 (requirements.txt now allows ``django>=4.2,<6.0``). Development Status
  bumped from Alpha to Production/Stable to match.
* The upper bound is capped below Django 6.0 on purpose: Django 6.0 removed
  ``ModelAdmin.log_deletion()`` (used by ``soft_delete_selected``) in favor of
  ``log_deletions()``, which breaks this package as-is.
* Restore the missing ``tests/urls.py`` test URLconf and add a functional test covering the
  ``soft_delete_selected`` admin action, so the suite actually exercises ``get_deleted_objects``.
* Refresh ``tox.ini``/``.travis.yml`` test matrices, which were still targeting Django 1.11/2.1.

0.1.0 (2021-05-05)
++++++++++++++++++

* First release on PyPI.
