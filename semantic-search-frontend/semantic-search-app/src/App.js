// import logo from './logo.svg';
// import './App.css';
//
// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }
//
// export default App;

// src/App.js
// import React from 'react';
// import SemanticSearch from './components/SemanticSearch';
//
// function App() {
//   return (
//     <div>
//       <h1>Semantic Lyrics Search</h1>
//       <SemanticSearch />
//     </div>
//   );
// }
//
// export default App;

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


