"""
範例 Python 程式
遵循 PEP 8 規範，使用具描述性的命名方式。
"""

def say_hello(name: str) -> str:
    """
    接收名字並回傳問候語。
    """
    if not name:
        return "Hello, World!"
    return f"Hello, {name}!"

if __name__ == "__main__":
    user_name = "Student"
    print(say_hello(user_name))
