// // frontend/src/components/VaultItemModal.jsx
// import { useState, useEffect } from 'react';
// import apiClient from '../services/api.js';
// import './VaultItemModal.css';

// function VaultItemModal({ item, onClose, onSaved }) {
//   const [form, setForm] = useState({ url: '', username: '', password: '', notes: '' });
//   const [error, setError] = useState('');
//   const [isSaving, setIsSaving] = useState(false);
  
//   const isEditing = item && item.id;

//   useEffect(() => {
//     if (isEditing) {
//       setForm({
//         url: item.url || '',
//         username: item.username || '',
//         password: '', // Siempre vacía al inicio
//         notes: item.notes || '',
//       });
//     } else {
//       setForm({ url: '', username: '', password: '', notes: '' });
//     }
//   }, [item]);

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setForm(prevForm => ({ ...prevForm, [name]: value }));
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setIsSaving(true);
//     setError('');

//     const payload = { ...form };
//     // Si estamos editando y no se ha escrito una nueva contraseña, no la enviamos.
//     if (isEditing && !payload.password) {
//       delete payload.password;
//     }

//     try {
//       if (isEditing) {
//         await apiClient.put(`/vault/${item.id}`, payload);
//       } else {
//         await apiClient.post('/vault/', payload);
//       }
//       onSaved();
//     } catch (err) {
//       const errorDetail = err.response?.data?.detail;
//       if (errorDetail && Array.isArray(errorDetail)) {
//           const errorMsg = errorDetail.map(e => `${e.loc.slice(-1)[0]}: ${e.msg}`).join('; ');
//           setError(errorMsg);
//       } else {
//         setError('Error al guardar. Verifica los datos, especialmente la URL (debe empezar con http:// o https://).');
//       }
//     } finally {
//       setIsSaving(false);
//     }
//   };

//   return (
//     <div className="modal-overlay">
//       <div className="modal-box">
//         <h3>{isEditing ? 'Editar' : 'Añadir'} Contraseña</h3>
//         <form onSubmit={handleSubmit}>
//           {/* --- AÑADIMOS 'required' Y PLACEHOLDERS --- */}
//           <div className="input-group">
//             <label htmlFor="url">URL</label>
//             <input name="url" type="url" value={form.url} onChange={handleChange} required placeholder="https://ejemplo.com" />
//           </div>
//           <div className="input-group">
//             <label htmlFor="username">Username</label>
//             <input name="username" value={form.username} onChange={handleChange} required />
//           </div>
//           <div className="input-group">
//             <label htmlFor="password">Password</label>
//             <input name="password" type="password" value={form.password} onChange={handleChange} required={!isEditing} />
//             {isEditing && <small>Dejar en blanco para no cambiar</small>}
//           </div>
//           <div className="input-group">
//             <label htmlFor="notes">Notas (Opcional)</label>
//             <textarea name="notes" value={form.notes} onChange={handleChange} rows="3" />
//           </div>

//           {error && <p className="error-message">{error}</p>}

//           <div className="modal-actions">
//             <button type="button" onClick={onClose} className="btn-secondary">Cancelar</button>
//             <button type="submit" disabled={isSaving} className="btn-primary">
//               {isSaving ? 'Guardando...' : 'Guardar'}
//             </button>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// }

// export default VaultItemModal;

// frontend/src/components/VaultItemModal.jsx
import { useState, useEffect } from 'react';
import apiClient from '../services/api.js';
import './VaultItemModal.css';

function VaultItemModal({ item, onClose, onSaved }) {
  const [form, setForm] = useState({ url: '', username: '', password: '', notes: '' });
  const [error, setError] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [showPassword, setShowPassword] = useState(false); // Nuevo estado para controlar la visibilidad

  const isEditing = item && item.id;

  useEffect(() => {
    if (isEditing) {
      setForm({
        url: item.url || '',
        username: item.username || '',
        password: '', // Siempre empieza vacío
        notes: item.notes || '',
      });
      setShowPassword(false); // Siempre empieza oculta
    } else {
      setForm({ url: '', username: '', password: '', notes: '' });
      setShowPassword(true); // En modo creación, el campo está visible para escribir
    }
    setError('');
  }, [item]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prevForm => ({ ...prevForm, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setError('');
    
    const payload = { ...form };
    if (isEditing && !payload.password) {
      delete payload.password;
    }

    try {
      if (isEditing) {
        await apiClient.put(`/vault/${item.id}`, payload);
      } else {
        await apiClient.post('/vault/', payload);
      }
      onSaved();
    } catch (err) {
      setError('Error al guardar. Verifica que la URL tenga el formato correcto (http://...).');
    } finally {
      setIsSaving(false);
    }
  };

  // --- NUEVA FUNCIÓN ---
  // Llama al endpoint de detalle para obtener la contraseña descifrada
  const fetchAndShowPassword = async () => {
    if (!isEditing) return;
    try {
      const response = await apiClient.get(`/vault/${item.id}`);
      setForm(prevForm => ({ ...prevForm, password: response.data.password }));
      setShowPassword(true);
    } catch (err) {
      setError('No se pudo cargar la contraseña.');
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>{isEditing ? 'Editar' : 'Añadir'} Contraseña</h3>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="url">URL</label>
            <input name="url" type="url" value={form.url} onChange={handleChange} required placeholder="https://ejemplo.com" />
          </div>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input name="username" value={form.username} onChange={handleChange} required />
          </div>

          {/* --- LÓGICA DE CONTRASEÑA MEJORADA --- */}
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <div className="password-wrapper">
              <input
                name="password"
                type={showPassword ? 'text' : 'password'}
                value={form.password}
                onChange={handleChange}
                required={!isEditing} // Requerido solo al crear
              />
              {isEditing && (
                <button type="button" onClick={showPassword ? () => setShowPassword(false) : fetchAndShowPassword} className="btn-secondary">
                  {showPassword ? 'Ocultar' : 'Ver'}
                </button>
              )}
            </div>
            {isEditing && <small>Dejar en blanco para no cambiar. Haz clic en "Ver" para mostrar la actual.</small>}
          </div>
          
          <div className="input-group">
            <label htmlFor="notes">Notas (Opcional)</label>
            <textarea name="notes" value={form.notes} onChange={handleChange} rows="3" />
          </div>

          {error && <p className="error-message">{error}</p>}

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn-secondary">Cancelar</button>
            <button type="submit" disabled={isSaving} className="btn-primary">
              {isSaving ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default VaultItemModal;