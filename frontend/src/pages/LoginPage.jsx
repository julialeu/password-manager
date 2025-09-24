import { useState, useEffect } from 'react'; // Importa useState y useEffect
import { useNavigate, Link } from 'react-router-dom'; // Importa useNavigate y Link
import apiClient from '../services/api.js';
import './LoginPage.css';

function LoginPage() {
  // --- ESTADOS DEL COMPONENTE ---
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState(''); // Estado para el mensaje de éxito
  const navigate = useNavigate();

  // --- EFECTO PARA LEER EL MENSAJE DE ÉXITO ---
  useEffect(() => {
    // Leemos el mensaje de sessionStorage cuando el componente se carga
    const msg = sessionStorage.getItem('successMessage');
    if (msg) {
      setSuccessMessage(msg);
      // Lo borramos para que no se vuelva a mostrar
      sessionStorage.removeItem('successMessage');
    }
  }, []); // El array vacío [] asegura que esto solo se ejecute una vez al cargar

  // --- FUNCIÓN DE LOGIN ---
  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage(''); // Limpiamos el mensaje de éxito al intentar loguear
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
        navigate('/'); // Redirigir a la bóveda si el login es exitoso
      } else {
        throw new Error("La respuesta del servidor no contiene un token.");
      }
    } catch (err) {
      console.error("Error en el login:", err);
      setError('Email o contraseña incorrectos.');
    }
  };

  // --- JSX (LO QUE SE RENDERIZA) ---
  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Iniciar Sesión</h2>

        {/* Muestra el mensaje de éxito si existe */}
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
          <button type="submit" className="btn-primary">Login</button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1rem' }}>
          ¿No tienes una cuenta? <Link to="/register">Regístrate aquí</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;