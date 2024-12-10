import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";  // 正確引入 useNavigate

function Register() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    address: "", // 新增 address 欄位
    phone: "", // 新增 phone 欄位
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const navigate = useNavigate();  // 初始化 useNavigate

  // 處理表單輸入變更
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // 表單驗證
  const validateForm = () => {
    if (!formData.username || !formData.email || !formData.password || !formData.address || !formData.phone) {
      setError("Please fill out all fields");
      return false;
    }
    return true;
  };

  // 處理註冊表單提交
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setError(null);
    setSuccessMessage(null);

    // 如果表單驗證不通過，則不進行提交
    if (!validateForm()) return;

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8800/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMessage("註冊成功! 請稍等，將跳轉至登入畫面");
        // 註冊成功後跳轉到登入頁面，延遲 2 秒鐘
        setTimeout(() => {
          navigate("/login");  // 使用 navigate 進行跳轉
        }, 2000);
      } else {
        setError(data.message || "Something went wrong!");
      }
    } catch (error) {
      setError("Network error. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Home 連結 */}
      <div className="header">
        <Link to="/" className="isLogin">
          Home
        </Link>
      </div>
      <h1 className="register-size">註冊</h1>
      <hr className="horizontal-line" />
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">
            使用者名稱
            <span className="required">*</span>
          </label>
          <div className="input-container">
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="使用者名稱"
              className="form-input"
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">
            電子郵件地址
            <span className="required">*</span>
          </label>
          <div className="input-container">
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="電子郵件地址"
              className="form-input"
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">
            密碼
            <span className="required">*</span>
          </label>
          <div className="input-container">
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="密碼"
              className="form-input"
            />
          </div>
        </div>

        {/* 新增地址欄位 */}
        <div className="form-group">
          <label className="form-label">
            地址
            <span className="required">*</span>
          </label>
          <div className="input-container">
            <input
              type="text"
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
              placeholder="地址"
              className="form-input"
            />
          </div>
        </div>

        {/* 新增電話欄位 */}
        <div className="form-group">
          <label className="form-label">
            電話號碼
          </label>
          <div className="input-container">
            <input
              type="text"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="電話號碼"
              className="form-input"
            />
          </div>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "送出中..." : "送出"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {successMessage && (
        <p style={{ color: "green" }}>
          {successMessage}
        </p>
      )}
    </div>
  );
}

export default Register;
