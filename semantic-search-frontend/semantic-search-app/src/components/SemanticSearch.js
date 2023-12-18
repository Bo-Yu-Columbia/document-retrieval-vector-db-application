import React, { useState } from 'react';
import axios from 'axios';

const SemanticSearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const searchContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: '100%'
    };

    const inputStyle = {
        padding: '10px',
        width: '300px',
        marginBottom: '10px',
        borderRadius: '5px',
        border: '1px solid #ccc'
    };

    const buttonStyle = {
        padding: '10px 20px',
        borderRadius: '5px',
        border: 'none',
        backgroundColor: '#3498db',
        color: 'white',
        cursor: 'pointer'
    };

    const resultsStyle = {
        marginTop: '20px',
        width: '500px',
        textAlign: 'left'
    };

    const resultItemStyle = {
        backgroundColor: 'white',
        padding: '10px',
        borderRadius: '5px',
        marginBottom: '10px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
    };

    const handleSearch = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/graphql', {
                query: `
                    query SemanticSearch($query: String!) {
                        semanticLyricsSearch(query: $query) {
                            songName
                            lyric
                            score
                        }
                    }
                `,
                variables: { query }
            });
            console.log("Query with Variables:", { query });

            setResults(response.data.data.semanticLyricsSearch);
        } catch (error) {
            console.error('Error fetching semantic search results', error);
        }
    };

    return (
        <div style={searchContainerStyle}>
            <input
                style={inputStyle}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for lyrics..."
            />
            <button style={buttonStyle} onClick={handleSearch}>Search</button>
            <div style={resultsStyle}>
                {results.map((result, index) => (
                    <div key={index} style={resultItemStyle}>
                        <h3>{result.songName}</h3>
                        <p>{result.lyric} (Score: {result.score})</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SemanticSearch;
//
// // src/components/SemanticSearch.js
// import React, { useState } from 'react';
// import axios from 'axios';
//
// const SemanticSearch = () => {
//     const [query, setQuery] = useState('');
//     const [standardResults, setStandardResults] = useState([]);
//     const [semanticResults, setSemanticResults] = useState([]);
//
//     const handleSearch = async () => {
//         try {
//             const response = await axios.post('http://127.0.0.1:5000/graphql', {
//                 query: `
//                     query Search($query: String!) {
//                         standardLyricsSearch(query: $query) {
//                             songName
//                             lyric
//                         }
//                         semanticLyricsSearch(query: $query) {
//                             songName
//                             lyric
//                             score
//                         }
//                     }
//                 `,
//                 variables: { query }
//             });
//
//             setStandardResults(response.data.data.standardLyricsSearch);
//             setSemanticResults(response.data.data.semanticLyricsSearch);
//         } catch (error) {
//             console.error('Error fetching search results', error);
//         }
//     };
//
//     const resultsContainerStyle = {
//         display: 'flex',
//         justifyContent: 'space-around',
//         marginTop: '20px'
//     };
//
//     const columnStyle = {
//         width: '45%',
//         padding: '0 10px'
//     };
//
//     return (
//         <div>
//             <input
//                 type="text"
//                 value={query}
//                 onChange={(e) => setQuery(e.target.value)}
//                 placeholder="Search for lyrics..."
//             />
//             <button onClick={handleSearch}>Search</button>
//             <div style={resultsContainerStyle}>
//                 <div style={columnStyle}>
//                     <h2>Standard Search</h2>
//                     {standardResults.map((result, index) => (
//                         <div key={index}>
//                             <h3>{result.songName}</h3>
//                             <p>{result.lyric}</p>
//                         </div>
//                     ))}
//                 </div>
//                 <div style={columnStyle}>
//                     <h2>Semantic Search</h2>
//                     {semanticResults.map((result, index) => (
//                         <div key={index}>
//                             <h3>{result.songName}</h3>
//                             <p>{result.lyric} (Score: {result.score})</p>
//                         </div>
//                     ))}
//                 </div>
//             </div>
//         </div>
//     );
// };
//
// export default SemanticSearch;
