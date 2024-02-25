import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { TaskPage } from "./pages/TaskPage";
import { TaskFormPage } from "./pages/TaskFormPage";
import { RegisterFormPage } from "./pages/RegisterFormPage.jsx"; 
import { LoginFormPage } from "./pages/LoginFormPage.jsx"; 
import  ProductDetail  from "./components/Product";
import CustomDesign from "./components/CustomDesign.jsx";
import { Navigation } from "./components/Navigation";
import { ChatPage } from "./pages/ChatPage"
import UserDetail from "./components/User";

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/" element={<Navigate to="/tasks" />} />
        <Route path="/tasks" element={<TaskPage />} />
        <Route path="/tasks-create" element={<TaskFormPage />} />
        <Route path="/product-details/:id" element={<ProductDetail />} />
        <Route path="/designs/my-design" element={<CustomDesign />} />
        <Route path="/register" element={<RegisterFormPage />} /> 
        <Route path="/login" element={<LoginFormPage />} /> 
        <Route path="/user-details/:id" element={<UserDetail />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
