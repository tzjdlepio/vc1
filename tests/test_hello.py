import unittest
from asgards.hello import say_hello

class TestHello(unittest.TestCase):
    """
    測試 asgards/hello.py 中的功能
    """

    def test_say_hello_with_name(self):
        """測試正常輸入名字的情況"""
        self.assertEqual(say_hello("Alice"), "Hello, Alice!")
        self.assertEqual(say_hello("Bob"), "Hello, Bob!")

    def test_say_hello_with_empty_name(self):
        """測試輸入空字串的情況（應回傳預設值）"""
        self.assertEqual(say_hello(""), "Hello, World!")

    def test_say_hello_with_none(self):
        """測試輸入 None 的情況（應回傳預設值）"""
        self.assertEqual(say_hello(None), "Hello, World!")

if __name__ == "__main__":
    unittest.main()
