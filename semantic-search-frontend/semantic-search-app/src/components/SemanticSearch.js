import React, { useState } from 'react';
import axios from 'axios';

const SemanticSearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [image, setImage] = useState(null);
    const [imageURL, setImageURL] = useState('');

    const searchContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: '100%',
        overflow: 'auto', // Ensure content can scroll
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

    const imagePreviewStyle = {
        maxWidth: '500px',
        maxHeight: '300px',
        margin: '10px',
        border: '1px solid #ddd',
        borderRadius: '5px',
        objectFit: 'contain',
    };

    const fileInputStyle = {
        margin: '10px 0',
        padding: '10px',
        border: '1px dashed #3498db',
        borderRadius: '5px',
        backgroundColor: '#f3f3f3',
        textAlign: 'center',
        color: '#3498db',
        cursor: 'pointer',
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

            // setResults(response_semantic.sample-data.sample-data.semanticLyricsSearch);
            setResults({
                semantic: response_semantic.data.data.semanticLyricsSearch,
                standard: response_standard.data.data.standardLyricsSearch
            });
        } catch (error) {
            console.error('Error fetching semantic search results', error);
        }
    };

    const handleImageChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            const img = e.target.files[0];
            setImage(e.target.files[0]);
            setImageURL(URL.createObjectURL(img));
        }
    };

    // const handleImageUpload = async () => {
    //     if (!image) {
    //         console.error('No image selected');
    //         return;
    //     }
    //
    //     const formData = new FormData();
    //     formData.append('file', image);
    //
    //     try {
    //         const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
    //             headers: {
    //                 'Content-Type': 'multipart/form-sample-data'
    //             }
    //         });
    //
    //         // Assuming the response contains the search results
    //         setResults({
    //             semantic: response.data.semantic,
    //             standard: response.data.standard
    //         });
    //     } catch (error) {
    //         console.error('Error uploading image:', error);
    //     }
    // };
    const handleImageUpload = async () => {
        console.log('It is starting');
        if (!image) {
            console.error('No image selected');
            return;
        }
        console.log('It is starting2');
        const formData = new FormData();
            formData.append('file', image);
            console.log('It is starting 3');

            // try {
                const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data' // Corrected the MIME type
                    }
                });
                console.log('It is starting 4');

                // Print the response to the console
                console.log('Response from backend:', response);

                // Assuming the response contains the search results in a 'results' key
                if (response.data && response.data.results) {
                    setResults(response.data.results);
                } else {
                    console.error('Invalid response structure:', response.data);
                }
            // } catch (error) {
            //     console.error('Error uploading image:', error);
            // }
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
            <label style={fileInputStyle}>
                {image ? 'Change Image' : 'Select Image'}
                <input
                    type="file"
                    onChange={handleImageChange}
                    accept="image/*"
                    style={{ display: 'none' }}  // Hide the default file input
                />
            </label>
            {/* Image Preview */}
            {imageURL && (
                <img
                    src={imageURL}
                    alt="Uploaded"
                    style={imagePreviewStyle}
                />
            )}
            {/*<button style={buttonStyle} onClick={handleImageUpload}>Search by Image</button>*/}
            {/* {imageURL && <img src={imageURL} alt="Uploaded" style={{ maxWidth: '500px', maxHeight: '300px', margin: '10px' }} />}*/}
            <button style={buttonStyle} onClick={handleImageUpload}>Search by Image</button>
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
            )}{results.length > 0 && (
            <div style={resultsStyle}>
                <h2>Search Results</h2>
                {results.map((result, index) => (
                    <div key={index} style={resultItemStyle}>
                        <h3>{result.song_name}</h3>
                        <p>{result.lyric}</p>
                        <p>Score: {result.score.toFixed(2)}</p>
                        <p>Singer: {result.singer}</p>
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

