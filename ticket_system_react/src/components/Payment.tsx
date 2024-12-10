import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import "./Payment.css";

const Payment = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);

  const orderId = queryParams.get("orderId");
  const paymentStatus = queryParams.get("paymentStatus");
  const amount = queryParams.get("amount");

  const [paymentMethod, setPaymentMethod] = useState(""); // 記錄選擇的付款方式
  const [responseMessage, setResponseMessage] = useState("");

  const handlePaymentMethodChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setPaymentMethod(event.target.value);
  };

  const handleSubmit = async () => {
    if (!paymentMethod || !orderId || !amount) {
      setResponseMessage("Please fill in all the fields.");
      return;
    }

    const requestData = {
      or_id: orderId,
      payment_method: paymentMethod,
      amount: amount,
    };

    try {
      const res = await fetch(
        "http://127.0.0.1:8800/payment?user_name=" +
          localStorage.getItem("authToken"),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        }
      );

      const data = await res.json();

      if (res.ok) {
        console.log(data.message);

        alert("繳費成功");
        navigate("/Customer"); // 导向到 Customer 页
      } else {
        console.log(data.message || "Something went wrong.");
      }
    } catch (error) {
      console.log("An error occurred during the payment process.");
      console.error(error);
    }
  };

  const handleCancel = async () => {
    // 顯示確認提示
    const isConfirmed = window.confirm("確定要取消這個訂單嗎？");
    if (!isConfirmed) {
      return; // 如果使用者選擇取消，則不繼續執行
    }
  
    const requestData = {
      or_id: orderId,
    };
  
    try {
      const res = await fetch(
        "http://127.0.0.1:8800/cancelticket?user_name=" +
          localStorage.getItem("authToken"),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        }
      );
  
      const data = await res.json();
  
      if (res.ok) {
        console.log(data.message);
        alert("取消成功");
        navigate("/Customer"); // 導向到 Customer 頁
      } else {
        console.log(data.message || "Something went wrong.");
        alert(data.message || "取消失敗，請稍後再試。");
      }
    } catch (error) {
      console.log("An error occurred during the cancel process.");
      alert("系統錯誤：" + error.message);
    }
  };
  
  
  
  return (
    <div className="payment-container">
      <h2>Payment Page</h2>
      <p>Order ID: {orderId}</p>
      <p>Payment Status: {paymentStatus}</p>
      <p>Amount: ${amount}</p>

      <div className="payment-method-container">
        <p>Select Payment Method:</p>
        <select
          id="payment-method"
          value={paymentMethod}
          onChange={handlePaymentMethodChange}
        >
          <option value="">--Select--</option>
          <option value="Credit Card">Credit Card</option>
          <option value="PayPal">PayPal</option>
          <option value="Bank Transfer">Bank Transfer</option>
          <option value="Apple Pay">Apple Pay</option>
          <option value="Google Pay">Google Pay</option>
        </select>
      </div>

      <div className="button-group">
        <button className="button-p" onClick={handleSubmit} disabled={!paymentMethod}>
          Submit Payment
        </button>
        <button className="button-p cancel-button" onClick={handleCancel}>
          Cancel The Ticket
        </button>
      </div>


      {responseMessage && <p className="error-message">{responseMessage}</p>}
    </div>
  );
};

export default Payment;
