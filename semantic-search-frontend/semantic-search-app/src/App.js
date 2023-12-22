import React from 'react';
import SemanticSearch from './components/SemanticSearch';

function App() {
  const appStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f5f5f5',
    fontFamily: 'Arial, sans-serif',
    color: '#333'
  };

  const headerStyle = {
    color: '#2c3e50',
    marginBottom: '20px'
  };

  return (
    <div style={appStyle}>
      <h1 style={headerStyle}>Semantic Lyrics Search</h1>
      <SemanticSearch />
    </div>
  );
}

export default App;


