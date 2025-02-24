import React from "react";
import "./RestaurantCard.css";

const RestaurantCard = ({ restaurant }) => {
  return (
    <div className="restaurant-card">
      <img src={restaurant.logo} alt={`${restaurant.name} logo`} />
      <div className="info">
        <div className="name">{restaurant.name}</div>
        <div className="hours">{restaurant.hours}</div>
      </div>
      <button className="order-btn">Order</button>
    </div>
  );
};

export default RestaurantCard;