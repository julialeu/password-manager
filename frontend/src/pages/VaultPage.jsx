import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../services/api.js';
import VaultItemModal from '../components/VaultItemModal.jsx';
import './VaultPage.css';

function VaultPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentItem, setCurrentItem] = useState(null);

  const [searchQuery, setSearchQuery] = useState('');

  // Función para obtener los items
  const fetchItems = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const response = await apiClient.get('/vault/', {
        params: { q: searchQuery || undefined } 
      });
      setItems(response.data);
    } catch (err) {
      console.error("Error loading items:", err);
      if (err.response?.status === 401) {
        handleLogout();
      } else {
        setError('Passwords could not be loaded.');
      }
    } finally {
      setLoading(false);
    }
  }, [searchQuery]);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchItems();
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery, fetchItems]);

  const handleOpenCreateModal = () => {
    setCurrentItem(null);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (item) => {
    setCurrentItem(item);
    setIsModalOpen(true);
  };

  const handleModalSave = () => {
    setIsModalOpen(false);
    fetchItems(); 
  };

  const handleDelete = async (itemId) => {
    if (window.confirm('Are you sure you want to delete this password?')) {
      try {
        await apiClient.delete(`/vault/${itemId}`);
        fetchItems(); 
      } catch (err) {
        console.error("Error deleting item:", err);
        alert('Error deleting password.');
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="vault-container">
      <nav className="navbar">
        <h1>My Password Manager</h1>
        <button onClick={handleLogout} className="btn-danger">
          Logout
        </button>
      </nav>
      <main className="main-content">
        <div className="toolbar">
          <input
            type="text"
            placeholder="Search by user, URL, notes..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button onClick={handleOpenCreateModal} className="btn-primary">
            Add Password
          </button>
        </div>

        {loading && <p>Loading...</p>}
        {!loading && error && <p className="error-message">{error}</p>}
        {!loading && !error && items.length === 0 && (
            <p>{searchQuery ? 'No results found.' : 'You have no saved passwords.'}</p>
        )}
        
        <div className="items-grid">
          {items.map(item => (
            <div key={item.id} className="item-card">
              <h3>{item.url?.replace(/^(https?:\/\/)?(www\.)?/, '').split('/')[0] || 'N/A'}</h3>
              <p>{item.username}</p>
              <div className="card-actions">
                <button onClick={() => handleOpenEditModal(item)} className="btn-primary">Edit</button>
                <button onClick={() => handleDelete(item.id)} className="btn-danger">Delete</button>
              </div>
            </div>
          ))}
        </div>
      </main>

      {isModalOpen && (
        <VaultItemModal
          key={currentItem ? `edit-${currentItem.id}` : 'create'}
          item={currentItem}
          onClose={() => setIsModalOpen(false)}
          onSaved={handleModalSave}
        />
      )}
    </div>
  );
}

export default VaultPage;