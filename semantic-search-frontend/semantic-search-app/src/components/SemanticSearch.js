import React, { useState } from 'react';
import axios from 'axios';

const SemanticSearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [image, setImage] = useState(null);

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

    const parentContainerStyle = {
        display: 'flex',
        justifyContent: 'space-around', // This spreads out the child divs evenly
        alignItems: 'flex-start', // This aligns items to the start of the flex direction
        flexWrap: 'wrap', // This allows items to wrap onto multiple lines, if needed
        // You can adjust the gap or add other styles as needed
        gap: '20px' // Adds space between the two divs
    };

    const handleSearch = async () => {
        try {
            const response_semantic = await axios.post('http://127.0.0.1:5000/graphql', {
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
            const response_standard = await axios.post('http://127.0.0.1:5000/graphql', {
                query: `
                    query SemanticSearch($query: String!) {
                        standardLyricsSearch(query: $query) {
                            songName
                            lyric
                            score
                        }
                    }
                `,
                variables: { query }
            });
            console.log("Query with Variables:", { query });

            // setResults(response_semantic.data.data.semanticLyricsSearch);
            setResults({
                semantic: response_semantic.data.data.semanticLyricsSearch,
                standard: response_standard.data.data.standardLyricsSearch
            });
        } catch (error) {
            console.error('Error fetching semantic search results', error);
        }
    };

    const handleImageUpload = async () => {
        if (!image) {
            console.error('No image selected');
            return;
        }

        const formData = new FormData();
        formData.append('file', image);

        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Assuming the response contains the search results
            setResults({
                semantic: response.data.semantic,
                standard: response.data.standard
            });
        } catch (error) {
            console.error('Error uploading image:', error);
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
            {/*<input*/}
            {/*    type="file"*/}
            {/*    onChange={(e) => setImage(e.target.files[0])}*/}
            {/*    accept="image/*"*/}
            {/*    style={{ margin: '10px 0' }}*/}
            {/*/>*/}
            {/*<button style={buttonStyle} onClick={handleImageUpload}>Search by Image</button>*/}
            <div style={parentContainerStyle}>
            {results.semantic && results.semantic.length > 0 && (
                <div style={resultsStyle}>
                    <h2>Semantic Results</h2> {/* Title for Semantic Results */}
                    {results.semantic.map((result, index) => (
                        <div key={index} style={resultItemStyle}>
                            <h3>{result.songName}</h3>
                            <p>{result.lyric} (Score: {result.score})</p>
                        </div>
                    ))}
                </div>
            )}

            {results.standard && results.standard.length > 0 && (
                <div style={resultsStyle}>
                    <h2>Standard Results</h2> {/* Title for Standard Results */}
                    {results.standard.map((result, index) => (
                        <div key={index} style={resultItemStyle}>
                            <h3>{result.songName}</h3>
                            <p>{result.lyric} </p>
                        </div>
                    ))}
                </div>
            )}
        </div>
        </div>
    );
};


export default SemanticSearch;

