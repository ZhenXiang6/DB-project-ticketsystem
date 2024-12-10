import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useEvent } from './EventContext'; // 使用 useEvent 來獲取活動列表

function EventList() {
  const { events } = useEvent(); // 從 context 中取得活動列表
  const [categories, setCategories] = useState([]); // 用於存儲類別
  const [selectedCategory, setSelectedCategory] = useState(''); // 儲存選中的類別
  const [searchQuery, setSearchQuery] = useState(''); // 儲存搜索的關鍵字
  console.log(events);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8800/get_categories');
        const data = await response.json();
        if (data.status === 'success') {
          setCategories(data.categories[0]); // 設置類別資料
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

  // 根據關鍵字篩選活動
  const filteredEvents = events
    .filter((event) =>
      selectedCategory === '' ? true : event.category === selectedCategory
    )
    .filter((event) =>
      event.name.toLowerCase().includes(searchQuery.toLowerCase()) // 根據活動名稱進行關鍵字篩選
    );

  return (
    <div>
      {/* Home 連結 */}
      <div className="header">
        <Link to="/" className="isLogin">
          Home
        </Link>
      </div>

      <h1>近期活動清單</h1>

      {/* 類別選擇框 */}
      <div>
        <p>選擇類別：</p>
        <select
          id="category-select"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)} // 更新選中的類別
        >
          <option value="">全部</option>
          {categories.map((category) => (
            <option key={category.c_name} value={category.c_name}>
              {category.c_name}
            </option>
          ))}
        </select>
      </div>

      {/* 關鍵字搜索框 */}
      <div>
        <p>關鍵字搜索：</p>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)} // 更新關鍵字
          placeholder="輸入活動名稱"
          style={{marginLeft: '30px', marginBottom: '30px'}}
        />

      </div>

      {/* 活動清單 */}
      <ul className="event-list">
        {filteredEvents.length === 0 ? (
          <p>目前沒有任何活動</p> // 如果活動清單為空，顯示無活動提示
        ) : (
          filteredEvents.map((event) => (
            <li key={event.id}>
              <h3>{event.name}</h3> {/* 顯示活動名稱 */}
              <p>{event.time}</p> {/* 顯示活動時間 */}
              <Link className="book-now" to={`/event/${event.id}`}>
                Book Now
              </Link>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default EventList;
