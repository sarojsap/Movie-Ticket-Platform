import { useEffect, useState } from 'react';
import api from './api/axios';

function App() {
  const [movies, setMovies] = useState([]);

  // Theory: useEffect is a "Hook". It runs code when the component mounts (loads).
  useEffect(() => {
    api.get('movies/')
      .then(response => {
        console.log("Data received:", response.data);
        setMovies(response.data);
      })
      .catch(error => {
        console.error("Error connecting to backend:", error);
      });
  }, []);

  return (
    <div>
      <h1>Movie Platform</h1>
      {movies.length === 0 ? (
        <p>Loading movies...</p>
      ) : (
        movies.map(movie => (
          <div key={movie.id} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
            <h2>{movie.title}</h2>
            <p>{movie.description}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default App;