import React from "react";
import RestaurantCard from "./RestaurantCard";
import "./RestaurantList.css";

const restaurants = [
  { id: 1, name: "Urban Hen", hours: "11:00 AM - 9:00 PM", logo: "https://via.placeholder.com/60" },
  { id: 2, name: "Mozzie's Handcrafted Pizza", hours: "12:00 PM - 10:00 PM", logo: "https://via.placeholder.com/60" },
  { id: 3, name: "Sushi By Faith", hours: "11:30 AM - 9:00 PM", logo: "https://via.placeholder.com/60" },
  { id: 4, name: "Epic Eats", hours: "10:00 AM - 10:00 PM", logo: "https://via.placeholder.com/60" },
  { id: 5, name: "Louie's", hours: "12:00 PM - 10:00 PM", logo: "https://via.placeholder.com/60" },
  { id: 6, name: "Starbucks", hours: "7:00 AM - 7:00 PM", logo: "https://via.placeholder.com/60" },
];

const RestaurantList = () => {
  return (
    <div className="restaurant-list">
      {restaurants.map((restaurant) => (
        <RestaurantCard key={restaurant.id} restaurant={restaurant} />
      ))}
    </div>
  );
};

export default RestaurantList;