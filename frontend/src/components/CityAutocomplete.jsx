import React, { useState, useEffect } from 'react';
import { useDebounce } from '../utils/useDebounce';

export default function CityAutocomplete({ onSelectCity }) {
  const [city, setCity] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const debouncedCity = useDebounce(city, 300);

  const handleChange = (e) => {
    setCity(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedCity = city.trim();
    if (trimmedCity) {
      onSelectCity(trimmedCity);
      setCity('');
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    onSelectCity(suggestion);
    setCity('');
    setSuggestions([]);
  };

  useEffect(() => {
    if (debouncedCity.length < 1) {
      setSuggestions([]);
      return;
    }

    const fetchSuggestions = async () => {
      try {
        const response = await fetch(`/api/v1/tips?city_prefix=${encodeURIComponent(debouncedCity)}`, {
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          setSuggestions(data || []);
        } else {
          setSuggestions([]);
        }
      } catch {
        setSuggestions([]);
      }
    };

    fetchSuggestions();
  }, [debouncedCity]);

  return (
    <form onSubmit={handleSubmit} style={{ position: 'relative' }}>
      <input
        type="text"
        placeholder="Введите город"
        value={city}
        onChange={handleChange}
        autoComplete="off"
        style={{ width: '100%', padding: '8px' }}
      />
      <button type="submit" style={{ marginTop: 8 }}>
        Показать погоду
      </button>

      {suggestions.length > 0 && (
        <ul
          style={{
            position: 'absolute',
            backgroundColor: 'white',
            border: '1px solid #ccc',
            marginTop: 4,
            padding: 0,
            listStyle: 'none',
            width: '100%',
            zIndex: 10,
            color: 'black',
            maxHeight: 150,
            overflowY: 'auto',
            boxShadow: '0 2px 5px rgba(0,0,0,0.15)',
            cursor: 'pointer',
          }}
        >
          {suggestions.map((s, i) => (
            <li
              key={i}
              onClick={() => handleSuggestionClick(s.name)}
              style={{ padding: '8px' }}
              onMouseDown={e => e.preventDefault()}
            >
              {s.name}
            </li>
          ))}
        </ul>
      )}
    </form>
  );
}
