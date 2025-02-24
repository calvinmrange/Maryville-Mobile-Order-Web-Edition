import React from "react";
import "./Header.css";

const Header = () => {
  return (
    <header className="header">
      <div className="header-title">Sleeping Totoros Order Page</div>
      <div className="header-icons">
        <button title="Home">🏠</button>
        <button title="Account Settings">⚙️</button>
        <button title="Notifications">🔔</button>
        <button title="Order Ratings">⭐</button>
      </div>
    </header>
  );
};

export default Header;