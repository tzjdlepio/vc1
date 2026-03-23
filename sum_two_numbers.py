def main():
    try:
        num1_input = input("請輸入第一個整數: ")
        num2_input = input("請輸入第二個整數: ")
        
        # 嘗試將輸入轉換為整數
        num1 = int(num1_input)
        num2 = int(num2_input)
        
        # 計算並輸出總和
        result = num1 + num2
        print(f"兩數總和為: {result}")
        
    except ValueError:
        # 如果轉換失敗（輸入不是整數），顯示錯誤訊息
        print("錯誤：輸入內容不是整數，請重新輸入。")

if __name__ == "__main__":
    main()
