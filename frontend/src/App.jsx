import React, { useState, useEffect } from 'react';
import CityAutocomplete from './components/CityAutocomplete';
import LastCityReminder from './components/LastCityReminder';

export default function App() {
  const [selectedCity, setSelectedCity] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [lastCity, setLastCity] = useState(null);
  const [cityStats, setCityStats] = useState(null);

  const handleSelectCity = (city) => {
    setSelectedCity(null);
    setTimeout(() => {
      setSelectedCity(city);
    }, 0);
  };

  // Загрузка последнего города при загрузке приложения
  useEffect(() => {
    async function fetchLastCity() {
      try {
        const response = await fetch('/api/v1/last_search', {
          credentials: 'include',
        });
        if (!response.ok) throw new Error('Ошибка при получении последнего города');
        const data = await response.json();
        if (data.last_city) {
          setLastCity(data.last_city);
        } else {
          const savedCity = localStorage.getItem('lastCity');
          if (savedCity) setLastCity(savedCity);
        }
      } catch {
        const savedCity = localStorage.getItem('lastCity');
        if (savedCity) setLastCity(savedCity);
      }
    }
    fetchLastCity();
  }, []);

  // Запрос погоды и обновление статистики с задержкой
  useEffect(() => {
    if (!selectedCity) return;

    async function fetchWeather() {
      try {
        const response = await fetch('/api/v1/weather', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ city: selectedCity }),
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error('Ошибка при получении погоды');
        }

        const data = await response.json();
        setWeatherData(data.weather);

        const normalizedCity = data.city || selectedCity;
        localStorage.setItem('lastCity', normalizedCity);
        setLastCity(normalizedCity);

        // Запрос статистики с задержкой, чтобы данные успели обновиться в БД
        setTimeout(async () => {
          try {
            const respStats = await fetch(`/api/v1/stats?city_name=${encodeURIComponent(normalizedCity)}`, {
              credentials: 'include',
            });
            if (!respStats.ok) throw new Error('Ошибка при получении статистики');
            const count = await respStats.json();
            setCityStats(count);
          } catch {
            setCityStats(null);
          }
        }, 700); // Задержка в миллисекундах (700 мс)

      } catch (err) {
        setWeatherData({ error: err.message });
        setCityStats(null);
      }
    }

    fetchWeather();
  }, [selectedCity]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Прогноз погоды</h1>

      <LastCityReminder lastCity={lastCity} onSelectCity={handleSelectCity} />

      <CityAutocomplete onSelectCity={handleSelectCity} />

      {weatherData && (
        <div style={{ marginTop: 20 }}>
          <h2>Результат:</h2>
          {weatherData.error ? (
            <p style={{ color: 'red' }}>{weatherData.error}</p>
          ) : (
            <>
              <p>Температура: {weatherData.temperature} °C</p>
              <p>Ветер: {weatherData.windspeed} км/ч</p>
              <p>Направление ветра: {weatherData.winddirection}°</p>
              <p>Время данных: {weatherData.time}</p>
            </>
          )}
          {cityStats !== null && (
            <p>Город был запрошен {cityStats} {cityStats === 1 ? 'раз' : 'раза'}</p>
          )}
        </div>
      )}
    </div>
  );
}
