import React from "react";
import { Routes, Route } from "react-router-dom";
import ChatPage from "../features/ChatPage/ChatPage";
import TopPage from "../features/TopPage/TopPage";

const AppRoutes: React.FC = () => (
  <Routes>
    <Route path="/" element={<TopPage />} />
    <Route path="/chat" element={<ChatPage />} />
  </Routes>
);

export default AppRoutes;
