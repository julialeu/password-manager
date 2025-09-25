import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import apiClient from '../services/api.js';
import './LoginPage.css';

function ResetPasswordPage() {
  const [newPassword, setNewPassword] = useState('');
  const [token, setToken] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    // Extraer el token de los parámetros de la URL
    const tokenFromUrl = searchParams.get('token');
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    } else {
      setError('Token not found. The link may be invalid or have expired.');
    }
  }, [searchParams]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    if (!token) {
      setError('Cannot proceed without a valid token..');
      return;
    }
    try {
      await apiClient.post('/login/reset-password/', { token, new_password: newPassword });
      sessionStorage.setItem('successMessage', 'Password successfully updated! You can now log in.');
      navigate('/login');
    } catch (err) {
      setError('The token is invalid, has expired, or the password is invalid.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Set New Password</h2>
        {token ? (
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="newPassword">New Password</label>
              <input
                id="newPassword"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                autoComplete="new-password"
              />
            </div>
            {message && <p style={{color: 'green', textAlign: 'center'}}>{message}</p>}
            {error && <p className="error-message">{error}</p>}
            <button type="submit" className="btn-primary">Save Password</button>
          </form>
        ) : (
          <p className="error-message">{error || 'Loading...'}</p>
        )}
        <p style={{ textAlign: 'center', marginTop: '1rem' }}>
          <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default ResetPasswordPage;