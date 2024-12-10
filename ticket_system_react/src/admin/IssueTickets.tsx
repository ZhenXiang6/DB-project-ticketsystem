import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import './AdminEventList.css';

function IssueTickets() {
  const { eventId } = useParams();
  console.log(eventId);

  const [ticketType, setTicketType] = useState('');
  const [ticketPrice, setTicketPrice] = useState('');
  const [ticketCount, setTicketCount] = useState('');
  const [prices, setPrices] = useState([]);

  useEffect(() => {
    const fetchEventDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8800/view_event_details?e_id=${eventId}`);
        const res = await response.json();

        console.log(res);
        if (res.status === "success") {
          setPrices(res.data || []);
        } else {
          console.error("活動未找到");
        }
      } catch (err) {
        console.error("發生錯誤，請稍後再試");
      }
    };

    fetchEventDetails();
  }, [eventId]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!ticketType || !ticketPrice || !ticketCount) {
      alert('請填寫所有欄位');
      return;
    }

    // 構建要發送的資料
    const ticketData = {
      e_id: eventId,
      t_type: ticketType,
      price: parseFloat(ticketPrice),
      total_quantity: parseInt(ticketCount, 10),
    };

    try {
      // 發送 POST 請求到後端
      const response = await fetch('http://127.0.0.1:8800/issue_tickets', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(ticketData),
      });

      const res = await response.json();

      if (res.status === 'success') {
        alert('票券發行成功');
        // 可以在這裡清空輸入框
        setTicketType('');
        setTicketPrice('');
        setTicketCount('');
        window.location.reload();
      } else {
        alert('票券發行失敗: ' + res.message);
      }
    } catch (err) {
      console.error('發送請求時出錯', err);
      alert('發送請求時出錯，請稍後再試');
    }
  };

  return (
    <div className='issue-tickets-container'>
      {/* 返回管理頁面的連結 */}
      <div className="header">
        <Link to="/admin" className="isLogin">Home</Link>
      </div>

      <h1>發行票券</h1>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>
            票券類型：
            <input
              type="text"
              value={ticketType}
              onChange={(e) => setTicketType(e.target.value)}
              placeholder="輸入票券類型"
              required
              style={{ marginLeft: '10px' }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            票券價格：
            <input
              type="number"
              value={ticketPrice}
              onChange={(e) => setTicketPrice(e.target.value)}
              placeholder="輸入票券價格"
              required
              style={{ marginLeft: '10px' }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            票券張數：
            <input
              type="number"
              value={ticketCount}
              onChange={(e) => setTicketCount(e.target.value)}
              placeholder="輸入票券張數"
              required
              style={{ marginLeft: '10px' }}
            />
          </label>
        </div>

        <button type="submit">
          發行票券
        </button>
      </form>

      <div style={{ marginTop: '30px' }}>
        <h2>現有票型</h2>
        {prices.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>票券類型</th>
                <th>票券價格</th>
                <th>剩餘張數</th>
                <th>總張數</th>
              </tr>
            </thead>
            <tbody>
              {prices.map((price, index) => (
                <tr key={index}>
                  <td>{price.t_type}</td>
                  <td>{price.price}</td>
                  <td>{price.remain_quantity}</td>
                  <td>{price.total_quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>目前沒有可用的票型。</p>
        )}
      </div>
    </div>
  );
}

export default IssueTickets;
