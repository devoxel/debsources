# Copyright (C) 2013-2015  The Debsources developers <info@sources.debian.net>.
# See the AUTHORS file at the top-level directory of this distribution and at
# https://anonscm.debian.org/gitweb/?p=qa/debsources.git;a=blob;f=AUTHORS;hb=HEAD
#
# This file is part of Debsources. Debsources is free software: you can
# redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.  For more information
# see the COPYING file at the top-level directory of this distribution and at
# https://anonscm.debian.org/gitweb/?p=qa/debsources.git;a=blob;f=COPYING;hb=HEAD

from __future__ import absolute_import

import json
import unittest

from nose.plugins.attrib import attr

from debsources.tests.test_webapp import DebsourcesBaseWebTests


@attr('copyright')
class CopyrightTestCase(DebsourcesBaseWebTests, unittest.TestCase):

    def test_api_ping(self):
        rv = json.loads(self.app.get('/copyright/api/ping/').data)
        self.assertEqual(rv["status"], "ok")
        self.assertEqual(rv["http_status_code"], 200)

    def test_api_packages_list(self):
        rv = json.loads(
            self.app.get('/copyright/api/list/').data)
        self.assertIn({'name': "ocaml-curses"}, rv['packages'])
        self.assertEqual(len(rv['packages']), 18)

    def test_api_by_prefix(self):
        rv = json.loads(
            self.app.get('/copyright/api/prefix/o/').data)
        self.assertIn({'name': "ocaml-curses"}, rv['packages'])
        # suite specified
        rv = json.loads(
            self.app.get('/copyright/api/prefix/o/?suite=wheezy').data)
        self.assertIn({'name': "ocaml-curses"}, rv['packages'])
        # a non-existing suite specified
        rv = json.loads(self.app.get(
            '/copyright/api/prefix/libc/?suite=non-existing').data)
        self.assertEqual([], rv['packages'])
        # special suite name "all" is specified
        rv = json.loads(
            self.app.get('/copyright/api/prefix/libc/?suite=all').data)
        self.assertIn({'name': "libcaca"}, rv['packages'])

    def test_by_prefix(self):
        rv = self.app.get('/copyright/prefix/libc/')
        self.assertIn("/license/libcaca", rv.data)
        # suite specified
        rv = self.app.get('/copyright/prefix/libc/?suite=squeeze')
        self.assertIn("/license/libcaca", rv.data)
        # a non-existing suite specified
        rv = self.app.get(
            '/copyright/prefix/libc/?suite=non-existing')
        self.assertNotIn("/license/libcaca", rv.data)
        # special suite name "all" is specified
        rv = self.app.get(
            '/copyright/prefix/libc/?suite=all')
        self.assertIn("/license/libcaca", rv.data)

    def test_latest(self):
        rv = self.app.get('/copyright/license/gnubg/latest/',
                          follow_redirects=True)
        self.assertIn("Package: gnubg / 1.02.000-2", rv.data)

    def test_non_machine_readable_license(self):
        rv = self.app.get('/copyright/license/gnubg/0.90+20091206-4/')
        self.assertNotIn("<p class=\'r_glob\'>", rv.data)

    def test_machine_readable_license(self):
        rv = self.app.get('/copyright/license/gnubg/1.02.000-2/')
        self.assertIn("<p class=\'r_glob\'>", rv.data)

if __name__ == '__main__':
    unittest.main(exit=False)