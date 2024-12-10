import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

interface OrderItems {
  event_things: any; // 假設 event 是一個物件，可以包含事件的詳細資料
  e_id: number;
  t_type: string;
  selectedQuantity: number;
  total_price: number;
}

const Order: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // 從 location.state 取得傳遞過來的 orderitems 資料
  const {
    event_things,
    e_id,
    t_type,
    selectedQuantity,
    total_price,
  }: OrderItems = location.state || {};

  const [totalPrice, setTotalPrice] = useState<number>(total_price || 0);

  useEffect(() => {
    if (selectedQuantity && total_price) {
      // 如果沒有 total_price，則可以透過 selectedQuantity 和其他資訊重新計算
      setTotalPrice(total_price);
    }
  }, [selectedQuantity, total_price]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const message = {
      e_id: e_id, // Example event ID from the event object
      t_type: t_type, // Ticket type
      quantity: selectedQuantity, // Quantity selected by the user
    };

    try {
      // Send a POST request to the Flask API
      const response = await fetch(
        "http://127.0.0.1:8800/buyticket?user_name=" +
          localStorage.getItem("authToken"),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(message), // Send ticket data as JSON
        }
      );

      const result = await response.json();

      if (response.ok) {
        // 顯示訂購成功訊息
        alert("訂購成功");
        // 等待兩秒後再導向到 confirmation 頁面
        navigate("/Customer");
      } else {
        // 處理伺服器的錯誤回應
        alert(result.message || "Error occurred while purchasing the ticket.");
      }
    } catch (error) {
      // Handle any network or other errors
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
    <div className="order-container">
      <h2>Order Details</h2>

      {/* 使用表格排版顯示訂單資訊 */}
      {event_things && (
        <table className="order-table">
          <thead>
            <tr>
              <th>Event Name</th>
              <th>Ticket Type</th>
              <th>Quantity</th>
              <th>Total Price</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{event_things.name}</td>
              <td>{t_type}</td>
              <td>{selectedQuantity}</td>
              <td>${totalPrice}</td>
            </tr>
          </tbody>
        </table>
      )}

      {/* 訂單確認區塊 */}
      <div className="order-form">
        <button type="button" onClick={handleSubmit}>
          Submit Order
        </button>
      </div>
    </div>
  );
};

export default Order;
