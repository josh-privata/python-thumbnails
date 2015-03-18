# -*- coding: utf-8 -*-
import os
import unittest

from PIL import Image

from thumbnails.engines.base import ThumbnailBaseEngine
from thumbnails.engines.dummy import DummmyEngine
from thumbnails.engines.pillow import PillowEngine
from thumbnails.images import SourceFile, Thumbnail


class EngineTestMixin(object):

    def setUp(self):
        self.engine = self.ENGINE()
        self.filename = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        self.file = SourceFile(self.filename)
        self.url = SourceFile('http://puppies.lkng.me/400x600/')

        image = Image.new('L', (400, 600))
        image.save(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    @unittest.skip('Awaiting')
    def test_create_from_file(self):
        thumbnail = self.engine.create(self.file, (200, 300), None)
        self.assertEqual(thumbnail.size[0], 200)
        self.assertEqual(thumbnail.size[1], 300)

    def test_create_from_url(self):
        thumbnail = self.engine.create(self.url, (200, 300), None)
        self.assertEqual(thumbnail.size[0], 200)
        self.assertEqual(thumbnail.size[1], 300)

    def test_no_scale_no_crop(self):
        thumbnail = self.engine.create(self.url, (400, 600), None)
        self.assertEqual(thumbnail.size[0], 400)
        self.assertEqual(thumbnail.size[1], 600)


class BaseEngineTestCase(EngineTestMixin, unittest.TestCase):
    ENGINE = ThumbnailBaseEngine

    def test__calculate_scaling_factor_without_crop(self):
        calculate_scaling_factor = self.engine._calculate_scaling_factor
        original_size = (400, 600)
        self.assertEqual(calculate_scaling_factor(original_size, (400, 600), False), 1)
        self.assertEqual(calculate_scaling_factor(original_size, (100, 600), False), 0.25)
        self.assertEqual(calculate_scaling_factor(original_size, (400, 300), False), 0.5)
        self.assertEqual(calculate_scaling_factor(original_size, (200, 300), False), 0.5)
        self.assertEqual(calculate_scaling_factor(original_size, (200, None), False), 0.5)
        self.assertEqual(calculate_scaling_factor(original_size, (None, 300), False), 0.5)

    def test_create_from_file(self):
        with self.assertRaises(NotImplementedError):
            self.engine.create(self.file, (200, 300), None)

    def test_create_from_url(self):
        with self.assertRaises(NotImplementedError):
            self.engine.create(self.url, (200, 300), None)

    def test_no_scale_no_crop(self):
        with self.assertRaises(NotImplementedError):
            self.engine.create(self.url, (400, 600), None)

    def test_create_thumbnail_object(self):
        name = ['851', '521c21fe9709802e9d4eb20a5fe84c18cd3ad']
        self.assertTrue(isinstance(self.engine.create_thumbnail_object(name), Thumbnail))

    def test_parse_size(self):
        self.assertEqual(self.engine.parse_size('100'), (100, None))
        self.assertEqual(self.engine.parse_size('100x200'), (100, 200))
        self.assertEqual(self.engine.parse_size('1x10'), (1, 10))
        self.assertEqual(self.engine.parse_size('x1000'), (None, 1000))

    def test_parse_crop(self):
        self.assertEqual(self.engine.parse_crop('center', (200, 200)), (100, 100))
        self.assertEqual(self.engine.parse_crop('top', (200, 200)), (100, 0))
        self.assertEqual(self.engine.parse_crop('bottom', (200, 200)), (100, 200))
        self.assertEqual(self.engine.parse_crop('left', (200, 200)), (0, 100))
        self.assertEqual(self.engine.parse_crop('right', (200, 200)), (200, 100))

        self.assertEqual(self.engine.parse_crop('20 20', (200, 200)), (40, 40))
        self.assertEqual(self.engine.parse_crop('20 80', (200, 200)), (40, 160))
        self.assertEqual(self.engine.parse_crop('80 20', (200, 200)), (160, 40))
        self.assertEqual(self.engine.parse_crop('25.55 25.55', (200, 200)), (51, 51))


class PillowEngineTestCase(EngineTestMixin, unittest.TestCase):
    ENGINE = PillowEngine


class DummyEngineTestCase(EngineTestMixin, unittest.TestCase):
    ENGINE = DummmyEngine

    def test_create_from_file(self):
        thumbnail = self.engine.create(self.file, (200, 300), None)
        self.assertEqual(thumbnail.width, 200)
        self.assertEqual(thumbnail.height, 300)
        self.assertEqual(thumbnail.url, 'http://puppies.lkng.me/200x300')

    def test_create_from_url(self):
        thumbnail = self.engine.create(self.url, (200, 300), None)
        self.assertEqual(thumbnail.width, 200)
        self.assertEqual(thumbnail.height, 300)
        self.assertEqual(thumbnail.url, 'http://puppies.lkng.me/200x300')
