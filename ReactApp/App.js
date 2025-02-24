import React from "react";
import Header from "./components/Header";
import RestaurantList from "./components/RestaurantList";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Header />
      <RestaurantList />
    </div>
  );
}

export default App;