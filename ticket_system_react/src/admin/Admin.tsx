function Admin() {
  const isLoggedIn = localStorage.getItem("authToken"); // 檢查登入狀態
  const userRole = localStorage.getItem("role"); // 檢查用戶角色
  
  // 如果未登入或角色不是 Admin，顯示錯誤訊息
  if (!isLoggedIn || userRole !== "Admin") {
    return (
      <div>
        <h1>錯誤</h1>
        <p>您不是有效的管理者角色，請聯繫管理員。</p>
      </div>
    );
  }

  return (
    <div>
      <div className="isLogin">
        {isLoggedIn ? (
          <a href="/customer">管理儀表板</a>
        ) : (
          <span>您尚未登入，請 <a href="/login" style={{ color: "green" }}>登入</a>。</span>
        )}
      </div>

      <h1>歡迎來到管理後台</h1>
      <p>在這裡您可以管理所有的用戶和活動。</p>

      {/* 活動列表連結總是顯示 */}
      <a href="/admin/myEvents"> 管理活動</a> |
      <a href="/admin/get-customer-info"> 客戶查詢</a>
    </div>
  );
}

export default Admin;
