# 售票系統

一個基於命令行的售票系統，允許用戶註冊、登錄、瀏覽活動、購買票券、處理付款以及管理個人資訊。管理員擁有額外的功能，如新增活動、發行票券以及查詢用戶資訊和購買歷史。

## 功能

### 所有用戶

- **註冊與登錄：** 創建新帳戶或登錄現有帳戶。
- **瀏覽活動：** 查看所有即將舉行的活動列表。
- **查看活動詳情：** 獲取特定活動的詳細資訊。
- **購買票券：** 為活動購買票券，選擇票種和數量。
- **處理付款：** 使用各種付款方式完成待付款訂單。
- **查看購買歷史：** 查看所有過去和當前的票券購買記錄。
- **編輯個人資訊：** 更新用戶名、密碼、電子郵件、電話號碼和地址。

### 管理員

- **新增活動：** 創建具有詳細資訊的新活動。
- **發行票券：** 為活動新增不同類型的票券。
- **查詢用戶資訊：** 查看系統中任何用戶的詳細資訊。
- **查詢用戶購買歷史：** 存取任何用戶的購買歷史記錄。

## 先決條件

- **Python 3.7 或更高版本**
- **PostgreSQL 12 或更高版本**
- **Git**

## 安裝

1. **克隆倉庫**（如果適用）

   - git clone https://github.com/ZhenXiang6/DB-project-ticketsystem
   - cd ticketing-system

2. **安裝所需的 Python 套件**

   - pip install -r requirements.txt

3. **創建 PostgreSQL 資料庫**

    - 透過backup檔來建置資料庫

## 配置

1. **資料庫連接字串**

   - 更新 models/database.py 中的 DATABASE_URL 以符合您的 PostgreSQL 資料庫憑證。
   - # models/database.py

    # 請根據您的資料庫設定更改以下變數
    - your_username = "postgres"
    - your_password = "1234"

    - DATABASE_URL = "postgresql://" + your_username + ":" + your_password + "@localhost:5432/ticketsystem"


## 運行應用程式

1. **啟動伺服器**

    - cd ticketing-system
    - python server.py

    您應該會看到類似以下的輸出：
    - Server listening on 127.0.0.1:8800 ...

2. **啟動客戶端**

    - cd ticketing-system
    - python client.py
    
    您應該會看到類似以下的輸出：
    - Connected to the Ticketing System server.

    ----------------------------------------
    Welcome to the Ticketing System! Please select your option:
    [1] Log-in
    [2] Sign-up
    [3] Leave System
    --->



