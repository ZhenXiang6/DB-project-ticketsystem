# Ticketing System

## 介紹

這是一個簡單的售票系統，允許用戶查看活動、購買票券、管理個人資訊等。同時，管理員可以新增活動、發行票券、查詢用戶資訊及購票紀錄。

## 功能

### 用戶功能

1. **查詢活動細節**：查看活動的詳細資訊。
2. **購買票券**：選擇活動、票種並購買票券。
3. **取消購買票券**：取消已購買的票券。
4. **付款**：處理訂單付款。
5. **查看及編輯使用者資訊**：管理個人資訊。
6. **查看購買紀錄**：查看過往的購票紀錄。

### 管理員功能

1. **發行票券**：新增不同區段的票價。
2. **新增活動**：新增活動及其細節。
3. **查詢使用者資訊**：查看用戶的個人資訊。
4. **查詢使用者購買紀錄**：查看用戶的購票紀錄。

## 安裝

1. **克隆專案**
    ```bash
    git clone https://github.com/your-username/ticket_system.git
    cd ticket_system
    ```

2. **安裝依賴**
    ```bash
    pip install -r requirements.txt
    ```

3. **配置資料庫**
    - 確保 PostgreSQL 已安裝並運行。
    - 建立資料庫 `ticketsystem` 
    - 修改 `models/database.py` 中的 `DATABASE_URL` 以符合您的資料庫設定。

4. **執行資料庫腳本**
    ```bash
    psql -U ticket_user -d ticketing_system -f schema.sql
    ```

## 使用

1. **啟動伺服器**
    ```bash
    python server.py
    ```

2. **啟動客戶端**
    ```bash
    python client.py
    ```

3. **操作流程**
    - 在客戶端，選擇登入或註冊。
    - 根據角色（用戶或管理員）進行相應的操作。

## 測試

使用 `pytest` 進行測試。

1. **安裝 pytest**
    ```bash
    pip install pytest
    ```

2. **運行測試**
    ```bash
    pytest
    ```


