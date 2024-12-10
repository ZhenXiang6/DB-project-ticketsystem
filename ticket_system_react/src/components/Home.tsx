import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

function Home() {  
  const isLoggedIn = localStorage.getItem("authToken"); // 檢查登入狀態  
  const userRole = localStorage.getItem("role"); // 檢查用戶角色
  const navigate = useNavigate();

  useEffect(() => {
    // 檢查登入狀態和角色，如果是 Admin，導航到管理頁面
    if (isLoggedIn && userRole === "Admin") {
      navigate("/Admin");
    }
  }, [isLoggedIn, userRole, navigate]); // 當 isLoggedIn 或 userRole 改變時觸發導航

  if (isLoggedIn && localStorage.getItem("role") == "Admin") {
    return (
        <div>
          <div className="isLogin">
          {isLoggedIn ? (
            <a href="/customer">會員資料</a>
          ) : (
            <span>您尚未登入，請 <a href="/login" style={{ color: "green" }}>登入</a>。</span>
          )}
        </div>
        <h1>錯誤</h1>
        <p>您不是有效的使用者角色，請聯繫管理員。</p>
      </div>
    );
  }

  return (
    <div>
      <div className="isLogin">
        {isLoggedIn ? (
          <a href="/customer">會員資料</a>
        ) : (
          <span>您尚未登入，請 <a href="/login" style={{ color: "green" }}>登入</a>。</span>
        )}
      </div>

      <h1>歡迎來到票務系統</h1>
      <p>在這裡探索並訂購您的票券。</p>

      {/* 如果未登入，顯示註冊和登入連結 */}
      {!isLoggedIn && (
        <>
          <a href="/register">註冊</a> | <a href="/login">登入 </a>| 
        </>
      )}

      {/* 活動列表連結總是顯示 */}
      <a href="/events"> 活動列表</a>
    </div>
  );
}

export default Home;
