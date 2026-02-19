import React, { useState } from "react";
import "./Registration.css";
import { useNavigate } from "react-router-dom";

type Role = "logistics" | "explorer" | "";

const Registration: React.FC = () => {
  const navigate = useNavigate();

  // 🔹 basic user info
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<Role>("");

  // 🔹 company info
  const [companyName, setCompanyName] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // ✅ REAL USER DATA
    const userData = {
      name,
      email,
      role,
      company: companyName,
    };

    // ✅ store for dashboard usage
    localStorage.setItem("dummyUser", JSON.stringify(userData));

    // 🔜 later: send to backend (already ready)
    /*
    fetch("http://localhost:5000/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        email,
        role,
        company_id: 1,
      }),
    });
    */

    navigate("/dashboard");
  };

  return (
    <div className="registration-page">
      <div className="registration-card">
        <h1>Create your account</h1>
        <p>Choose your role and get started with LogiSphere</p>

        <form className="registration-form" onSubmit={handleSubmit}>
          {/* 🔹 Basic Details */}
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {/* 🔹 Role Selection */}
          <select
            value={role}
            onChange={(e) => setRole(e.target.value as Role)}
            required
          >
            <option value="">Select Your Role</option>
            <option value="logistics">Logistics Manager</option>
            <option value="explorer">Exporter</option>
          </select>

          {/* 🚚 Logistics Manager */}
          {role === "logistics" && (
            <div className="role-options">
              <input
                type="text"
                placeholder="Logistics Company Name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                required
              />

              <select required>
                <option value="">Container Types Provided</option>
                <option>Dry Container</option>
                <option>Refrigerated (Reefer)</option>
                <option>Open Top</option>
                <option>Flat Rack</option>
                <option>Tank Container</option>
              </select>

              <input type="text" placeholder="Primary Source Location" required />
              <input type="text" placeholder="Operating Regions" required />
            </div>
          )}

          {/* 🌍 Exporter */}
          {role === "explorer" && (
            <div className="role-options">
              <input
                type="text"
                placeholder="Exporter / Company Name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                required
              />

              <select required>
                <option value="">Type of Goods Exported</option>
                <option>Agricultural Products</option>
                <option>Textiles & Garments</option>
                <option>Electronics</option>
                <option>Machinery</option>
                <option>Chemicals</option>
              </select>

              <input type="text" placeholder="Export Location" required />
              <input type="text" placeholder="Target Regions" required />

              <select required>
                <option value="">Preferred Container Type</option>
                <option>Dry Container</option>
                <option>Reefer Container</option>
                <option>Open Top</option>
                <option>Flat Rack</option>
              </select>
            </div>
          )}

          <button type="submit">Create Account</button>
        </form>

        <span className="divider">or</span>

        <button className="secondary-btn" onClick={() => navigate("/")}>
          Back to Home
        </button>
      </div>
    </div>
  );
};

export default Registration;
