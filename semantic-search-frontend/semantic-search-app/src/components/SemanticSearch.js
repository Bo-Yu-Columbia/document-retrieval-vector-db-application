// src/components/SemanticSearch.js
import React, { useState } from 'react';
import axios from 'axios';

const SemanticSearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

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
        <div>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for lyrics..."
            />
            <button onClick={handleSearch}>Search</button>
            <div>
                {results.map((result, index) => (
                    <div key={index}>
                        <h3>{result.songName}</h3>
                        <p>{result.lyric} (Score: {result.score})</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SemanticSearch;
