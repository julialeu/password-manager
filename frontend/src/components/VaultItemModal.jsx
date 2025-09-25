import { useState, useEffect } from 'react';
import apiClient from '../services/api.js';
import './VaultItemModal.css';

function VaultItemModal({ item, onClose, onSaved }) {
  const [form, setForm] = useState({ url: '', username: '', password: '', notes: '' });
  const [error, setError] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const isEditing = item && item.id;

  useEffect(() => {
    if (isEditing) {
      setForm({
        url: item.url || '',
        username: item.username || '',
        password: '',
        notes: item.notes || '',
      });
      setShowPassword(false);
    } else {
      setForm({ url: '', username: '', password: '', notes: '' });
      setShowPassword(true);
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
      setError('Error saving. Verify that the URL is in the correct format (http://...).');
    } finally {
      setIsSaving(false);
    }
  };

  // Llama al endpoint de detalle para obtener la contraseña descifrada
  const fetchAndShowPassword = async () => {
    if (!isEditing) return;
    try {
      const response = await apiClient.get(`/vault/${item.id}`);
      setForm(prevForm => ({ ...prevForm, password: response.data.password }));
      setShowPassword(true);
    } catch (err) {
      setError('Password could not be loaded.');
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>{isEditing ? 'Edit' : 'Add'} Password</h3>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="url">URL</label>
            <input name="url" type="url" value={form.url} onChange={handleChange} required placeholder="https://example.com" />
          </div>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input name="username" value={form.username} onChange={handleChange} required />
          </div>

          <div className="input-group">
            <label htmlFor="password">Password</label>
            <div className="password-wrapper">
              <input
                name="password"
                type={isEditing ? (showPassword ? 'text' : 'password') : 'password'}
                value={form.password}
                onChange={handleChange}
                required={!isEditing}
              />
              {isEditing && (
                <button type="button" onClick={showPassword ? () => setShowPassword(false) : fetchAndShowPassword} className="btn-secondary">
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              )}
            </div>
            {isEditing && <small>Leave blank to keep unchanged. Click “Show” to display the current one.</small>}
          </div>
          
          <div className="input-group">
            <label htmlFor="notes">Notes</label>
            <textarea name="notes" value={form.notes} onChange={handleChange} rows="3" />
          </div>

          {error && <p className="error-message">{error}</p>}

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn-secondary">Cancel</button>
            <button type="submit" disabled={isSaving} className="btn-primary">
              {isSaving ? 'Saving...' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default VaultItemModal;