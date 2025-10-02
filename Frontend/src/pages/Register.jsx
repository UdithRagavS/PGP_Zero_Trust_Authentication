import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Register.css"; // ✅ import CSS

export default function Register() {
  const [username, setUsername] = useState("");
  const [pgpKey, setPgpKey] = useState("");
  const [message, setMessage] = useState({ text: "", type: "" });

  const handleRegister = async (e) => {
  e.preventDefault();

  if (!username || !pgpKey) {
    setMessage({ text: "❌ All fields required", type: "error" });
    return;
  }

  try {
    const res = await fetch("http://localhost:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: `username=${encodeURIComponent(username)}&pgp_key=${encodeURIComponent(pgpKey)}`,
    });

    if (res.ok) {
      setMessage({ text: "✅ Registered successfully", type: "success" });
      setUsername("");
      setPgpKey("");
    } else {
      const data = await res.json();
      if (data.error?.includes("exists")) {
        setMessage({ text: "⚠️ Username or key already exists. Please try again.", type: "error" });
      } else {
        setMessage({ text: "❌ Registration failed. Please try again later.", type: "error" });
      }
    }
  } catch (err) {
    setMessage({ text: "❌ Server error. Please try again later.", type: "error" });
  }
};

  return (
    <div className="register-container">
      <div className="register-card">
        <h2 className="register-title">📝 Register User</h2>

        {message.text && (
          <p
            className="register-message"
            style={{ color: message.type === "success" ? "green" : "red" }}
          >
            {message.text}
          </p>
        )}

        <form onSubmit={handleRegister}>
          <label className="register-label">Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="register-input"
          />

          <label className="register-label">PGP Public Key:</label>
          <textarea
            value={pgpKey}
            onChange={(e) => setPgpKey(e.target.value)}
            rows={6}
            required
            className="register-textarea"
          />

          <button type="submit" className="register-button">
            🚀 REGISTER
          </button>
        </form>

        <Link to="/" className="back-button">
          ⬅ Back to Home
        </Link>
      </div>
    </div>
  );
}
