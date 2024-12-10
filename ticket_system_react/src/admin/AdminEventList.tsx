import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // 使用 useNavigate 進行頁面導航
import './AdminEventList.css';

function AdminEventList() {
  const [events, setEvents] = useState([]); // 用來儲存活動資料
  const [categories, setCategories] = useState([]); // 用來儲存類別資料
  const [selectedCategory, setSelectedCategory] = useState(''); // 儲存選中的類別
  const [searchQuery, setSearchQuery] = useState(''); // 儲存搜索關鍵字
  const token = localStorage.getItem("authToken"); // 取得 token
  const userRole = localStorage.getItem("role"); // 取得使用者角色
  const navigate = useNavigate(); // 使用 useNavigate 進行導航

  // 檢查使用者角色是否為 Admin，若不是則返回錯誤訊息
  if (!token || userRole !== "Admin") {
    return (
      <div>
        <h1>錯誤</h1>
        <p>您不是有效的管理者角色，請聯繫管理員。</p>
      </div>
    );
  }

  useEffect(() => {
    // 獲取類別資料
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

    fetchCategories(); // 獲取類別資料
  }, []); // 空陣列作為依賴，確保只執行一次

  useEffect(() => {
    // 獲取活動資料
    const fetchEvents = async () => {
      try {
        const eventResponse = await fetch('http://127.0.0.1:8800/get_all_event_detail', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const eventData = await eventResponse.json();

        if (eventResponse.ok) {
          setEvents(eventData.data); // 設定活動資料
        } else {
          console.log(eventData.error || "無法獲取活動資料");
        }
      } catch (error) {
        console.log("獲取活動資料時發生錯誤");
      }
    };

    fetchEvents(); // 獲取活動資料
  }, [token]); // 當 token 改變時重新執行 useEffect

  // 跳轉到新增活動頁面
  const handleAddEvent = () => {
    navigate('/admin/add-event'); // 假設新增活動的頁面路徑是 '/admin/add-event'
  };

  return (
    <div className="admin-event-list-container">
      {/* 返回管理頁面的連結 */}
      <div className="header">
        <Link to="/admin" className="isLogin">Home</Link>
      </div>

      <h1>管理者介面</h1>

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

      {/* 搜索框 */}
      <div style={{ marginLeft: '30px', marginBottom: '30px', marginTop: '40px'}}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)} // 更新搜索關鍵字
          placeholder="輸入活動名稱"
        />
      </div>

      <h2>近期活動清單</h2>

      {/* 新增活動按鈕 */}
      <button onClick={handleAddEvent} className="add-event-button">
        新增活動
      </button>

      {/* 顯示活動清單 */}
      <ul className="event-list">
        {events.length === 0 ? (
          <p>目前沒有任何活動</p>
        ) : (
          events
            .filter((event) => {
              // 根據選擇的類別和搜索關鍵字進行篩選
              const matchesCategory = selectedCategory === '' ? true : event.c_name === selectedCategory;
              const matchesSearch = event.e_name.toLowerCase().includes(searchQuery.toLowerCase());
              return matchesCategory && matchesSearch;
            })
            .map((event) => (
              <li key={event.e_id} className="event-item">
                <h3>{event.e_name}</h3> {/* 顯示活動名稱 */}
                <p>{event.e_datetime}</p> {/* 顯示活動日期 */}
                <Link className="book-now" to={`/admin/info/${event.e_id}`}>
                  發行票券
                </Link> {/* 連結到活動詳細頁面 */}
              </li>
            ))
        )}
      </ul>
    </div>
  );
}

export default AdminEventList;
