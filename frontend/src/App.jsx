import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import VaultPage from './pages/VaultPage';
import RequestPasswordResetPage from './pages/RequestPasswordResetPage';
import ResetPasswordPage from './pages/ResetPasswordPage'; 
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/request-password-reset" element={<RequestPasswordResetPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />  
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <VaultPage />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;