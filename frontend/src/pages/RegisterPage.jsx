// frontend/src/pages/RegisterPage.jsx
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../services/api.js';
import './LoginPage.css';

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await apiClient.post('/users/', { email, password });
      
      // Opcional: Se podría iniciar sesión automáticamente después del registro
      // para simplificar,vredirigimos al login
      // con un mensaje de éxito.
      sessionStorage.setItem('successMessage', '¡Registro exitoso! Ahora puedes iniciar sesión.');
    
      // Redirigimos
      navigate('/login');

    } catch (err) {
      if (err.response && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Ocurrió un error durante el registro.');
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Crear Cuenta</h2>
        <form onSubmit={handleRegister}>
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="btn-primary">Registrarse</button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '1rem' }}>
          ¿Ya tienes una cuenta? <Link to="/login">Inicia sesión aquí</Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;