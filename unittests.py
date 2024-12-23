import unittest

from hw3 import *
class TestConfigParser(unittest.TestCase):

    def test_parse_value(self):
        self.assertEqual(parse_value("123"), 123)
        self.assertEqual(parse_value('"Hello World"'), "Hello World")
        
        with self.assertRaises(ValueError):
            parse_value("unknown")

    def test_parse_dict(self):
        self.assertEqual(parse_dict("key1=1, key2=2"), {'key1': 1, 'key2': 2})
        
        self.assertEqual(parse_dict("name=\"John\", age=30"),{'name': 'John', 'age': 30})
        
        with self.assertRaises(ValueError):
            parse_dict("invalid_pair")

    def test_evaluate_expression(self):
        context = {'a': 10, 'b': 20}
        
        self.assertEqual(evaluate_expression('a + b', context), 30)
        self.assertEqual(evaluate_expression('a * b', context), 200)

        with self.assertRaises(ValueError):
            evaluate_expression('', context)  # Пустое выражение
        with self.assertRaises(ValueError):
            evaluate_expression('invalid syntax', context)  # Неверный синтаксис

if __name__ == '__main__':
    unittest.main()
