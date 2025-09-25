import { useState } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../services/api.js';
import './LoginPage.css';

function RequestPasswordResetPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    try {
      // El endpoint espera el email en la URL
      await apiClient.post(`/login/password-recovery/${email}`);
      setMessage('If an account exists with that email address, a recovery link has been sent.');
    } catch (err) {
      setError('An error has occurred. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Recuperar Contraseña</h2>
        <p style={{textAlign: 'center', marginBottom: '1rem', color: '#666', fontSize: '0.9rem'}}>
          Enter your email address and we will send you a link to reset your password.
        </p>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </div>
          {message && <p style={{color: 'green', textAlign: 'center'}}>{message}</p>}
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="btn-primary">Send</button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '1rem' }}>
          <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default RequestPasswordResetPage;