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

    def test_example_usage(self):
        """模擬 if __name__ == '__main__' 中的執行範例"""
        user_name = "Student"
        result = say_hello(user_name)
        self.assertEqual(result, "Hello, Student!")

    def test_hello_main_execution(self):
        """真正執行 hello.py 的 main 區塊"""
        import runpy
        import io
        from unittest.mock import patch
        
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            runpy.run_path("asgards/hello.py", run_name="__main__")
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "Hello, Student!")

if __name__ == "__main__":
    unittest.main()
