// // frontend/src/pages/VaultPage.jsx
// import { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import apiClient from '../services/api.js';
// import './VaultPage.css';

// function VaultPage() {
//   const [items, setItems] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const navigate = useNavigate();

//   useEffect(() => {
//     const fetchItems = async () => {
//       try {
//         const response = await apiClient.get('/vault/');
//         setItems(response.data);
//       } catch (error) {
//         if (error.response?.status === 401) {
//           handleLogout();
//         }
//       } finally {
//         setLoading(false);
//       }
//     };
//     fetchItems();
//   }, []);

//   const handleLogout = () => {
//     localStorage.removeItem('token');
//     navigate('/login');
//   };

//   return (
//     <div className="vault-container">
//       <nav>
//         <h1>My Password Manager</h1>
//         <button onClick={handleLogout}>Logout</button>
//       </nav>
//       <main>
//         {loading && <p>Loading...</p>}
//         {!loading && items.length === 0 && <p>You dont have any saved password</p>}
//         <div className="items-grid">
//           {items.map(item => (
//             <div key={item.id} className="item-card">
//               <h3>{item.url.replace(/^(https?:\/\/)?(www\.)?/, '').split('/')[0]}</h3>
//               <p>{item.username}</p>
//             </div>
//           ))}
//         </div>
//       </main>
//     </div>
//   );
// }

// export default VaultPage;

// frontend/src/pages/VaultPage.jsx
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../services/api.js'; // Asegúrate del .js
import VaultItemModal from '../components/VaultItemModal.jsx'; // Importamos el modal
import './VaultPage.css';

function VaultPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  // Estado para el modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentItem, setCurrentItem] = useState(null); // null para crear, objeto para editar

  // Estado para la búsqueda
  const [searchQuery, setSearchQuery] = useState('');

  // Función para obtener los items, ahora memorizada con useCallback
  const fetchItems = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const response = await apiClient.get('/vault/', {
        params: { q: searchQuery || undefined } // Añadimos el parámetro de búsqueda
      });
      setItems(response.data);
    } catch (err) {
      console.error("Error al cargar items:", err);
      if (err.response?.status === 401) {
        handleLogout();
      } else {
        setError('No se pudieron cargar las contraseñas.');
      }
    } finally {
      setLoading(false);
    }
  }, [searchQuery]); // Depende de searchQuery

  // useEffect para buscar cuando el usuario deja de teclear
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchItems();
    }, 300); // Espera 300ms antes de buscar

    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery, fetchItems]); // Se ejecuta cada vez que searchQuery o fetchItems cambian

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
    fetchItems(); // Recargamos la lista después de guardar
  };

  const handleDelete = async (itemId) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta contraseña?')) {
      try {
        await apiClient.delete(`/vault/${itemId}`);
        fetchItems(); // Recargamos la lista
      } catch (err) {
        console.error("Error al eliminar item:", err);
        alert('Error al eliminar la contraseña.');
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
        <h1>Mi Bóveda</h1>
        <button onClick={handleLogout} className="btn-danger">
          Cerrar Sesión
        </button>
      </nav>
      <main className="main-content">
        <div className="toolbar">
          <input
            type="text"
            placeholder="Buscar por usuario, url, notas..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button onClick={handleOpenCreateModal} className="btn-primary">
            Añadir Contraseña
          </button>
        </div>

        {loading && <p>Cargando...</p>}
        {!loading && error && <p className="error-message">{error}</p>}
        {!loading && !error && items.length === 0 && (
            <p>{searchQuery ? 'No se encontraron resultados.' : 'No tienes contraseñas guardadas.'}</p>
        )}
        
        <div className="items-grid">
          {items.map(item => (
            <div key={item.id} className="item-card">
              <h3>{item.url?.replace(/^(https?:\/\/)?(www\.)?/, '').split('/')[0] || 'N/A'}</h3>
              <p>{item.username}</p>
              <div className="card-actions">
                <button onClick={() => handleOpenEditModal(item)} className="btn-primary">Editar</button>
                <button onClick={() => handleDelete(item.id)} className="btn-danger">Eliminar</button>
              </div>
            </div>
          ))}
        </div>
      </main>

      {isModalOpen && (
        <VaultItemModal
          item={currentItem}
          onClose={() => setIsModalOpen(false)}
          onSaved={handleModalSave}
        />
      )}
    </div>
  );
}

export default VaultPage;