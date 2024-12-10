import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './Event_noSeat.css';
import { useEvent } from './EventContext';
import { useNavigate, Link } from "react-router-dom";

function Event_noSeat() {
  const navigate = useNavigate();

  const { id } = useParams();
  const { getEventbyId } = useEvent();
  const event = getEventbyId(Number(id));
  const [loading, setLoading] = useState(true);
  const [prices, setPrices] = useState([]);
  const [selectedPrice, setSelectedPrice] = useState();
  const [selectedQuantity, setSelectedQuantity] = useState(1);  // 預設為選擇 1 張票

  useEffect(() => {
    const fetchEventDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8800/view_event_details?e_id=${id}`);
        const res = await response.json();

        console.log(res); // 確認響應數據
        if (res.status === "success") {
          setPrices(res.data || []);
        } else {
          console.error("活動未找到");
        }
      } catch (err) {
        console.error("發生錯誤，請稍後再試");
      } finally {
        setLoading(false);
      }
    };

    fetchEventDetails();
  }, [id]);

  const handlePriceSelect = (price) => {
    setSelectedPrice(price);
  };

  if (loading) {
    return <div>載入中...</div>;
  }

  if (!event) {
    return <div>活動未找到</div>;
  }

  const handleSubmit = () => {
    // 驗證選擇的數量是否有效
    if (selectedQuantity < 1 || selectedQuantity > selectedPrice.total_quantity) {
      alert("請選擇有效的數量");
      return;
    }
  
    // 計算總價，假設 selectedPrice.price 是每張票的價格
    const totalPrice = selectedPrice.price * selectedQuantity;
  
    // 生成訂單項目
    const orderitems = {
      event_things: event,
      e_id: Number(id),
      t_type: selectedPrice.t_type,
      selectedQuantity: selectedQuantity,
      total_price: totalPrice, // 使用計算出來的總價
    };

  
    // 進行訂單提交邏輯，可以跳轉到訂購頁面
    console.log("提交訂單", orderitems);
  
    // 跳轉到訂購頁面
    navigate("/order", { state: orderitems });
  };

  
  return (
    <div className="event-container">
      {/* Home 連結 */}
      <div className="header">
        <Link to="/" className="isLogin">
          Home
        </Link>
      </div>

      <div className="event-info">
        <h2>{event.name}</h2>
        <p>{event.time}</p>
        <div className="event-description">{event.description}</div>
      </div>

      <div className="event-price-info">
        <h3>票價詳情:</h3>
        {prices.length > 0 ? (
          prices.map((price, index) => (
            <div 
              key={index} 
              className={`price-item ${selectedPrice === price ? 'selected' : ''}`}
              onClick={() => handlePriceSelect(price)}
            >
              <p>票種: {price.t_type} 票價: ${price.price} 剩餘票數: {price.remain_quantity}</p>
            </div>
          ))
        ) : (
          <p>沒有票價資料</p>
        )}
      </div>

      {selectedPrice && (
      <div className="selected-price-info">
        <h3>已選擇的票種:</h3>
        <p>票種: {selectedPrice.t_type}</p>
        
        {/* 計算總金額 */}
        <p>總金額: ${selectedPrice.price * selectedQuantity}</p>

        {/* 選擇的數量 */}
        <div>
          <p>選擇數量: </p>
          <input 
            id="quantity" 
            type="number" 
            value={selectedQuantity} 
            onChange={(e) => setSelectedQuantity(Number(e.target.value))}
            min="1" 
            max={selectedPrice.total_quantity} 
          />
        </div>

        {/* 送出按鈕 */}
        <button 
          onClick={() => handleSubmit()}
          className="submit-button"
        >
          送出
        </button>
      </div>
    )}
    </div>
  );
}

export default Event_noSeat;
