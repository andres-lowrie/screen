from unittest import TestCase
from app.utils import parse_with_type 


class TestUtils(TestCase):
    """Test utils procedures."""
    def setUp(self):
        self._float = '6.0006'
        self._int = '6'
        self._word = 'test'
        self._date = '2019-08-14'

    def test_parse_with_type(self):
        """Test if is_int working."""
        self.assertEqual(
            (float, 6.0006), 
            parse_with_type(self._float)
        )

        self.assertEqual(
            (int, 6), 
            parse_with_type(self._int)
        )

        self.assertEqual(
            (str, 'test'), 
            parse_with_type(self._word)
        )

        self.assertEqual(
            (str, '2019-08-14'), 
            parse_with_type(self._date)
        )
