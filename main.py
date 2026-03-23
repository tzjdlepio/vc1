def main():
    name = input("請輸入您的名字: ")
    
    # 檢查是否為空字串或僅包含空格
    if not name.strip():
        print("請輸入名字")
    else:
        print(f"Hello, {name}")

if __name__ == "__main__":
    main()
