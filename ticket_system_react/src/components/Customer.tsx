import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Customer.css"; // 引入外部 CSS

const Customer = () => {
  const navigate = useNavigate();

  const [userData, setUserData] = useState(null); // 儲存會員資料
  const [orders, setOrders] = useState([]); // 儲存訂單資料
  const [loading, setLoading] = useState(true); // 加載狀態

  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem("authToken");
      if (!token) {
        console.error("未登入或無效的 token");
        setLoading(false);
        navigate("/login"); // 導向登入頁面
        return;
      }

      try {
        // 獲取會員資料
        const userResponse = await fetch(
          `http://127.0.0.1:8800/customer_detail?cu_name=${token}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (userResponse.ok) {
          const userData = await userResponse.json();
          if (Array.isArray(userData) && userData.length > 0) {
            setUserData(userData[0]);
          } else {
            console.error("無法獲取會員資料");
          }
        } else {
          console.error("會員資料請求失敗", await userResponse.text());
        }

        // 獲取訂單資料
        const ordersResponse = await fetch(
          `http://127.0.0.1:8800/user_purchase_history?cu_name=${token}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (ordersResponse.ok) {
          const ordersData = await ordersResponse.json();
          setOrders(ordersData.purchase_history);
        } else {
          console.error("訂單資料請求失敗", await ordersResponse.text());
        }
      } catch (error) {
        console.error("網絡錯誤，請稍後再試", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = async () => {
    const token = localStorage.getItem("authToken");

    if (token) {
      try {
        const response = await fetch("http://127.0.0.1:8800/logout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ cu_name: token }),
        });

        if (response.ok) {
          localStorage.removeItem("authToken");
          localStorage.removeItem("role");
          navigate("/login");
        } else {
          const result = await response.json();
          console.error("登出失敗", result.message || "未知錯誤");
          alert(result.message || "登出失敗");
        }
      } catch (error) {
        console.error("登出時發生錯誤", error);
        alert("登出時發生錯誤，請稍後再試");
      }
    } else {
      alert("當前未登入");
    }
  };

  if (loading) {
    return <p>載入中...</p>;
  }

  return (
    <div className="customer-container">
      {/* Home 連結 */}
      <div className="header">
        <Link to="/" className="isLogin">
          Home
        </Link>
      </div>

      <div className="user-section">
        <h2>會員資料</h2>
        {userData ? (
          <div>
            <p>用戶名稱: {userData.cu_name}</p>
            <p>電子郵件: {userData.email}</p>
            <p>電話: {userData.phone_number || "未提供"}</p>
            <p>地址: {userData.address || "未提供"}</p>
            <p>角色: {userData.role}</p>
            <button className="button-cu" onClick={handleLogout}>
              登出
            </button>
          </div>
        ) : (
          <p>無法顯示會員資料</p>
        )}
      </div>

      {/* 根據角色判斷是否顯示訂單資訊 */}
      {localStorage.getItem("role") !== "Admin" && (
        <div className="table-container">
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
                  <th>繳費連結</th>
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

                    {order.payment_status === "Pending" && (
                      <td>
                        <Link
                          to={{
                            pathname: "/payment",
                            search: `?orderId=${order.or_id}&paymentStatus=${order.payment_status}&amount=${order.subtotal}`,
                          }}
                        >
                          Go to Payment
                        </Link>
                      </td>
                    )}

                    {order.payment_status !== "Pending" && (
                      <td>No need to pay.</td>
                    )}
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

export default Customer;
