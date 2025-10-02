import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>🔐 Zero-Trust Authentication</h1>
      <p>Select an option to continue:</p>
      <Link to="/login" className="btn">Login</Link>
      <Link to="/register" className="btn">Register</Link>

      <style>{`
        .btn {
          display: inline-block;
          padding: 12px 24px;
          margin: 10px;
          font-size: 18px;
          font-weight: bold;
          text-decoration: none;
          color: white;
          background-color: #007BFF;
          border-radius: 6px;
          transition: background-color 0.3s;
        }
        .btn:hover {
          background-color: #0056b3;
        }
      `}</style>
    </div>
  );
}
