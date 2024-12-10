import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

// 登入元件
function Login() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // 處理表單輸入變更
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // 驗證表單
  const validateForm = () => {
    if (!formData.username || !formData.password) {
      setError("Please fill out all fields");
      return false;
    }
    return true;
  };

  // 登入表單提交
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setError(null);
    setSuccessMessage(null);

    if (!validateForm()) return;

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8800/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMessage("Login successful!");
        localStorage.setItem("authToken", formData.username);
        localStorage.setItem("role", data.role)
        if (data.role == "User")
          navigate("/")
        else
          navigate("/Admin")
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
      <h1 className="register-size">會員登入</h1>
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

        <button className='button-login'type="submit" disabled={loading}>
          {loading ? "送出中 ..." : "送出"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
    </div>
  );
}

export default Login;
