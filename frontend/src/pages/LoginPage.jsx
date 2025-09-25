import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../services/api.js';
import './LoginPage.css';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  // --- MENSAJE DE ÉXITO ---
  useEffect(() => {
    // Leemos el mensaje de sessionStorage cuando el componente se carga
    const msg = sessionStorage.getItem('successMessage');
    if (msg) {
      setSuccessMessage(msg);
      // Lo borramos para que no se vuelva a mostrar
      sessionStorage.removeItem('successMessage');
    }
  }, []);

  // --- LOGIN ---
  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage(''); // Limpiamos el mensaje de éxito al intentar hacer login
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await apiClient.post('/login/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      const token = response?.data?.access_token;
      
      if (token) {
        localStorage.setItem('token', token);
        navigate('/');
      } else {
        throw new Error("The server response does not contain a token.");
      }
    } catch (err) {
      console.error("Login error:", err);
      setError('Incorrect email or password.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>My Password Manager</h2>

        {successMessage && (
          <p style={{color: 'green', textAlign: 'center', marginBottom: '1rem'}}>
            {successMessage}
          </p>
        )}

        <form onSubmit={handleLogin}>
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="btn-primary">Login</button>
        </form>
         <div style={{display: 'flex', justifyContent: 'space-between', marginTop: '1rem', fontSize: '0.9rem'}}>
          <Link to="/request-password-reset">Forgot your password?</Link>
          <Link to="/register">Create Account</Link>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;