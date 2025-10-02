import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Login.css"; // ✅ Import CSS

export default function Login() {
  const [username, setUsername] = useState("");
  const [challenge, setChallenge] = useState("");
  const [signature, setSignature] = useState("");
  const [step, setStep] = useState(1);
  const [message, setMessage] = useState({ text: "", type: "" });

  const handleGetChallenge = async () => {
    if (!username.trim()) {
      setMessage({ text: "❌ Please enter a username", type: "error" });
      return;
    }

    try {
      const res = await fetch("/auth/challenge", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${encodeURIComponent(username)}`
      });
      const data = await res.json();

      if (data.challenge) {
        setChallenge(data.challenge);
        setStep(2);
        setMessage({
          text: "✅ Challenge received. Now sign it with your PGP private key.",
          type: "success"
        });
      } else {
        setMessage({ text: data.error || "❌ Failed to get challenge.", type: "error" });
      }
    } catch {
      setMessage({ text: "❌ Server error. Try again later.", type: "error" });
    }
  };

  const handleVerify = async () => {
    if (!signature.trim()) {
      setMessage({ text: "❌ Please paste your signed challenge.", type: "error" });
      return;
    }

    try {
      const res = await fetch("/auth/verify", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${encodeURIComponent(username)}&signature=${encodeURIComponent(signature)}`
      });
      const data = await res.json();

      if (data.message) {
        setMessage({ text: data.message, type: "success" });
      } else {
        setMessage({ text: data.error || "❌ Login failed.", type: "error" });
      }
    } catch {
      setMessage({ text: "❌ Server error. Try again later.", type: "error" });
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">🔐 Login</h2>

        <label className="login-label">Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="login-input"
          placeholder="Enter your username"
        />

        <button onClick={handleGetChallenge} className="login-button">
          Get Challenge
        </button>

        {step === 2 && (
          <div>
            <label className="login-label">Challenge:</label>
            <textarea
              value={challenge}
              readOnly
              className="login-textarea"
              rows={2}
            />

            <label className="login-label">Paste your signed message (PGP signature):</label>
            <textarea
              value={signature}
              onChange={(e) => setSignature(e.target.value)}
              className="login-textarea"
              rows={5}
              placeholder="-----BEGIN PGP SIGNATURE-----"
            />

            <button onClick={handleVerify} className="login-button">
              Verify & Login
            </button>
          </div>
        )}

        {message.text && (
          <div className={`login-message ${message.type}`}>
            {message.text}
          </div>
        )}

        <Link to="/" className="back-button">
          ⬅ Back to Home
        </Link>
      </div>
    </div>
  );
}
