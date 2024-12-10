import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminEventList.css'; // 確保使用相同的 CSS 樣式

function AddEvent() {
  const navigate = useNavigate();

  const [eventName, setEventName] = useState('');
  const [eventDescription, setEventDescription] = useState('');
  const [eventDate, setEventDate] = useState('');
  const [eventLocation, setEventLocation] = useState('');
  const [categoryName, setCategoryName] = useState(''); // 類別名稱
  const [organizerName, setOrganizerName] = useState('');
  const [categories, setCategories] = useState<any[]>([]); // 存儲類別資料

  // 從後端獲取類別
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8800/get_categories');
        const data = await response.json();
        if (data.status === 'success') {
          setCategories(data.categories[0]);  // 設置類別資料
        } else {
          alert('無法獲取類別資料');
        }
      } catch (err) {
        console.error('獲取類別時出錯', err);
        alert('獲取類別資料時出錯，請稍後再試');
      }
    };

    fetchCategories();
  }, []); // 空陣列作為依賴，意味著只在組件加載時執行一次

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!eventName || !eventDescription || !eventDate || !eventLocation || !categoryName || !organizerName) {
      alert('請填寫所有欄位');
      return;
    }

    // 構建要發送的資料
    const eventData = {
      e_name: eventName,
      c_name: categoryName,  // 使用 categoryName
      o_name: organizerName,
      e_datetime: eventDate,
      e_location: eventLocation,
      description: eventDescription,
    };

    try {
        console.log(eventData)
      // 發送 POST 請求到後端
      const response = await fetch('http://127.0.0.1:8800/addevent?role=' + localStorage.getItem("role"), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData),
      });

      const res = await response.json();

      if (res.status === 'success') {
        alert('活動新增成功');
        setEventName('');
        setEventDescription('');
        setEventDate('');
        setEventLocation('');
        setCategoryName(''); // 清空類別名稱
        setOrganizerName('');
        navigate('/admin'); // 可選：成功後跳轉至管理頁面
      } else {
        alert('活動新增失敗: ' + res.message);
      }
    } catch (err) {
      console.error('發送請求時出錯', err);
      alert('發送請求時出錯，請稍後再試');
    }
  };

  return (
    <div className="issue-tickets-container">
      <h1>新增活動</h1>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>
            活動名稱：
            <input
              type="text"
              value={eventName}
              onChange={(e) => setEventName(e.target.value)}
              placeholder="輸入活動名稱"
              required
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            活動描述：
            <input
              type="text"
              value={eventDescription}
              onChange={(e) => setEventDescription(e.target.value)}
              placeholder="輸入活動描述"
              required
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            活動日期：
            <input
              type="date"
              value={eventDate}
              onChange={(e) => setEventDate(e.target.value)}
              required
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            活動地點：
            <input
              type="text"
              value={eventLocation}
              onChange={(e) => setEventLocation(e.target.value)}
              placeholder="輸入活動地點"
              required
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            類別：
            <select
              value={categoryName}
              onChange={(e) => setCategoryName(e.target.value)} // 改為使用 categoryName
              required
            >
              <option value="">選擇活動類別</option>
              {categories.map((category) => (
                <option key={category.c_name} value={category.c_name}>
                  {category.c_name}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            主辦方：
            <input
              type="text"
              value={organizerName}
              onChange={(e) => setOrganizerName(e.target.value)}
              placeholder="輸入主辦方名字"
              required
            />
          </label>
        </div>

        <button type="submit">新增活動</button>
      </form>
    </div>
  );
}

export default AddEvent;
