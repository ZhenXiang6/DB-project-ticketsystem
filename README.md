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
- **查看銷售報表：** 管理員可查看特定活動的銷售報表。

## 先決條件

- **Python 3.7 或更高版本**
- **PostgreSQL 12 或更高版本**
- **Git**

## 安裝

1. **克隆倉庫**（如果適用）

- git clone https://github.com/ZhenXiang6/DB-project-ticketsystem
- cd ticket-system

2. **安裝所需的 Python 套件**

- pip install -r requirements.txt

3. **創建 PostgreSQL 資料庫**

- 透過backup檔來建置資料庫

## 配置

1. **資料庫連接字串**

開啟 DB-project-ticketsystem\DB_utils.py 並變更資料以連接資料庫

# 請根據您的資料庫設定更改以下變數
db = Database(    
    dbname='ticketsystem',  #替換為資料庫名稱  
    user='postgres',  #替換為您的使用者名稱  
    password='1234',  # 替換為您的密碼  
    host='localhost',   
    port=5432,  
)

## 運行應用程式

1. **啟動伺服器**

- python server.py

您應該會看到類似以下的輸出：
- Server listening on 127.0.0.1:8800 ...

2. **啟動客戶端**

- python client.py
    
您應該會看到類似以下的輸出：
- Connected to the Ticketing System server.

   ----------------------------------------  
   Welcome to the Ticketing System! Please select your option:  
   [1] Log-in  
   [2] Sign-up  
   [3] Leave System  
   --->


# Ticket System 前端說明

這個專案是基於 **React** 和 **TypeScript** 實作的票務系統前端，使用 Node.js 作為開發環境。

## 環境設定

1. **安裝 Node.js**：
   請確保您的開發環境已安裝 Node.js。您可以從 [Node.js 官方網站](https://nodejs.org/) 下載並安裝最新版。

2. **專案安裝步驟**：
   - 下載並解壓此專案後，進入 `ticket_system` 資料夾。
   - 使用 `npm` 安裝所需的依賴：
     ```bash
     npm install
     ```

3. **啟動專案**：
   安裝完依賴後，可以使用以下指令啟動專案：
   ```bash
   npm run dev
   ```

   啟動後，您可以在瀏覽器中訪問 [http://localhost:3000](http://localhost:3000) 來查看應用。

## 資料庫設定

如果在註冊資訊時遇到問題，請確認以下幾個步驟來確保資料庫中的序列 (ID) 序列同步：

使用以下 SQL 查詢來重新設置各個表格的 ID 序列，確保它們從正確的最大值開始遞增：

```sql
-- 更新 CATEGORY 表格的 ID 序列
SELECT setval('category_c_id_seq', COALESCE((SELECT MAX(c_id) FROM CATEGORY), 0) + 1, false);

-- 更新 ORGANIZER 表格的 ID 序列
SELECT setval('organizer_o_id_seq', COALESCE((SELECT MAX(o_id) FROM ORGANIZER), 0) + 1, false);

-- 更新 EVENT 表格的 ID 序列
SELECT setval('event_e_id_seq', COALESCE((SELECT MAX(e_id) FROM EVENT), 0) + 1, false);

-- 更新 TICKET 表格的 ID 序列
SELECT setval('ticket_t_id_seq', COALESCE((SELECT MAX(t_id) FROM TICKET), 0) + 1, false);

-- 更新 CUSTOMER 表格的 ID 序列
SELECT setval('customer_cu_id_seq', COALESCE((SELECT MAX(cu_id) FROM CUSTOMER), 0) + 1, false);

-- 更新 ORDER 表格的 ID 序列
SELECT setval('"ORDER_or_id_seq"', COALESCE((SELECT MAX(or_id) FROM "ORDER"), 0) + 1, false);

-- 更新 PAYMENT 表格的 ID 序列
SELECT setval('payment_p_id_seq', COALESCE((SELECT MAX(p_id) FROM PAYMENT), 0) + 1, false);

-- 更新 VENUE 表格的 ID 序列
SELECT setval('venue_v_id_seq', COALESCE((SELECT MAX(v_id) FROM VENUE), 0) + 1, false);
```

這些 SQL 查詢會幫助您重設資料庫中的 ID 序列，使其正確地對應到資料表中的最大 ID。



