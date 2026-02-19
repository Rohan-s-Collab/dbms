import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

type User = {
  name: string;
  email: string;
  role: "logistics" | "exporter";
  company_id: number;
};

type Shipment = {
  shipment_id: number;
  shipment_status: string;
  shipment_request: string;
  exporter?: string;
};

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [shipments, setShipments] = useState<Shipment[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("dummyUser");

    if (!storedUser) {
      navigate("/register");
      return;
    }

    const parsedUser: User = JSON.parse(storedUser);
    setUser(parsedUser);

    // 🔥 FETCH SHIPMENTS BASED ON ROLE
    if (parsedUser.role === "logistics") {
      fetch(
        `http://localhost:5000/api/logistics/${parsedUser.company_id}/shipments`
      )
        .then((res) => res.json())
        .then((data) => setShipments(data));
    }

    if (parsedUser.role === "exporter") {
      fetch(
        `http://localhost:5000/api/exporter/${parsedUser.company_id}/shipments`
      )
        .then((res) => res.json())
        .then((data) => setShipments(data));
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("dummyUser");
    navigate("/register");
  };

  if (!user) return null;

  return (
    <div className="dashboard-container">
      <div className="dashboard-card">
        <h1>Welcome, {user.name} 👋</h1>

        <p className="subtitle">
          Role: {user.role === "logistics" ? "Logistics Manager" : "Exporter"}
        </p>

        {/* =====================
            SHIPMENT DASHBOARD
        ===================== */}
        <div className="role-section">
          <h2>Shipment Requests</h2>

          {shipments.length === 0 ? (
            <p>No shipments found</p>
          ) : (
            shipments.map((s) => (
              <div key={s.shipment_id} className="shipment-card">
                <strong>Shipment ID: {s.shipment_id}</strong>
                <p>
                  <b>Request:</b> {s.shipment_request}
                </p>
                <p>
                  <b>Status:</b> {s.shipment_status}
                </p>

                {user.role === "logistics" && (
                  <small>Exporter: {s.exporter}</small>
                )}
              </div>
            ))
          )}
        </div>

        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
