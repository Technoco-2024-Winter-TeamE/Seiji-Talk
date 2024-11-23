import React from "react";
import { Routes, Route } from "react-router-dom";
import ChatPage from "../features/ChatPage/ChatPage";

const AppRoutes: React.FC = () => (
  <Routes>
    <Route path="/" element={<ChatPage />} />
  </Routes>
);

export default AppRoutes;
