import React from 'react';

export default function LastCityReminder({ lastCity, onSelectCity }) {
  if (!lastCity) return null;

  return (
    <div>
      <p>Последний выбранный город: <b>{lastCity}</b></p>
      <button onClick={() => onSelectCity(lastCity)}>Показать снова</button>
    </div>
  );
}
