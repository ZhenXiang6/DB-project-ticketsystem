import { useState } from 'react';
import './SearchCustomer.css'; // 引入外部的 CSS 檔案
import { Link } from 'react-router-dom'

const SearchCustomer = () => {
  const [searchTerm, setSearchTerm] = useState(""); // 使用者輸入的搜尋字串
  const [customerDetail, setCustomerDetail] = useState(null); // 查詢到的客戶資料
  const [errorMessage, setErrorMessage] = useState(""); // 儲存錯誤訊息
  const [orders, setOrders] = useState([]); // 客戶的訂單資訊
  const [loading, setLoading] = useState(false); // 加載狀態

  const fetchCustomerDetail = async () => {
    if (!searchTerm.trim()) {
      setErrorMessage("請輸入客戶名稱");
      return;
    }

    setLoading(true); // 開始加載資料
    setErrorMessage(""); // 清除錯誤訊息
    setCustomerDetail(null); // 清空現有的客戶資料
    setOrders([]); // 清空現有的訂單資料

    try {
      // 查詢客戶基本資料
      const customerResponse = await fetch(
        `http://127.0.0.1:8800/customer_detail?cu_name=${encodeURIComponent(searchTerm)}`
      );
      const customerData = await customerResponse.json();

      if (customerResponse.ok) {
        setCustomerDetail(customerData); // 設置客戶詳細資料
      } else {
        setErrorMessage(customerData.error || "無法獲取客戶資料");
        return;
      }

      // 查詢客戶的訂單資訊
      const orderResponse = await fetch(
        `http://127.0.0.1:8800/user_purchase_history?cu_name=${encodeURIComponent(searchTerm)}`
      );
      const orderData = await orderResponse.json();

      if (orderResponse.ok) {
        setOrders(orderData.purchase_history || []); // 設置訂單資訊
      } else {
        setErrorMessage(orderData.error || "無法獲取訂單資料 或 使用者尚未訂購");
      }
      
    } catch (err) {
      console.error("請求失敗:", err);
      setErrorMessage("請求失敗，請稍後再試");
    } finally {
      setLoading(false); // 結束加載狀態
    }
  };

  return (
    <div className="search-customer-container">
      {/* Home 連結 */}
      <div className="header">
        <Link to="/" className="isLogin">
          Home
        </Link>
      </div>
      <h2 className="search-customer-title">Search Customer</h2>
      <input
        type="text"
        placeholder="Enter customer name"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="search-customer-input"
        onKeyPress={(e) => e.key === 'Enter' && fetchCustomerDetail()}  // 按 Enter 鍵觸發搜尋
      />
      <button onClick={fetchCustomerDetail} className="button-info">
        搜尋
      </button>
      {loading && <p>加載中...</p>} {/* 顯示加載中的提示 */}
      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {customerDetail && (
        <div className="customer-detail">
          <h3>客戶資料</h3>
          <div className="customer-info">
            <div><strong>姓名:</strong> {customerDetail[0].cu_name}</div>
            <div><strong>電子郵件:</strong> {customerDetail[0].email}</div>
            <div><strong>地址:</strong> {customerDetail[0].address || "未提供"}</div>
            <div><strong>電話號碼:</strong> {customerDetail[0].phone_number || "未提供"}</div>
            <div><strong>角色:</strong> {customerDetail[0].role}</div>
          </div>

          <h2>訂單資訊</h2>
          {orders.length > 0 ? (
            <table className="orders-table">
              <thead>
                <tr>
                  <th>訂單編號</th>
                  <th>活動名稱</th>
                  <th>票種</th>
                  <th>購買數量</th>
                  <th>小計金額</th>
                  <th>訂單日期</th>
                  <th>付款狀態</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.or_id}>
                    <td>{order.or_id}</td>
                    <td>{order.e_name}</td>
                    <td>{order.t_type}</td>
                    <td>{order.quantity}</td>
                    <td>${parseFloat(order.subtotal).toLocaleString()}</td>
                    <td>{new Date(order.or_date).toLocaleString()}</td>
                    <td>{order.payment_status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>尚無訂單資訊</p>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchCustomer;
