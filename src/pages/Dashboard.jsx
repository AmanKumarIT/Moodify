import React, { useRef, useState, useEffect, useCallback, useContext } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { LogOut, RefreshCw, History, User, Music, Pause } from 'lucide-react';

export default function Dashboard() {
  const webcamRef = useRef(null);
  const [emotion, setEmotion] = useState('Detecting...');
  const [confidence, setConfidence] = useState(0);
  const [songs, setSongs] = useState([]);
  const [history, setHistory] = useState([]);
  const [currentVideoId, setCurrentVideoId] = useState(null);
  const [isDetecting, setIsDetecting] = useState(true);
  const { user, logout } = useContext(AuthContext);

  const getHeaders = useCallback(() => {
    return { Authorization: `Bearer ${localStorage.getItem('token')}` };
  }, []);

  const fetchHistory = useCallback(async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/playlist/history/', { headers: getHeaders() });
      setHistory(res.data.history);
    } catch (e) {
      console.error('History fetch error', e);
    }
  }, [getHeaders]);

  const generatePlaylist = useCallback(async (detectedEmotion) => {
    try {
      const res = await axios.post('http://localhost:8000/api/playlist/generate/', 
        { emotion: detectedEmotion }, 
        { headers: getHeaders() }
      );
      setSongs(res.data.songs);
      if (res.data.songs.length > 0) {
        setCurrentVideoId(res.data.songs[0].videoId);
      }
      fetchHistory(); // Refresh history
    } catch (e) {
      console.error('Playlist gen error', e);
    }
  }, [getHeaders, fetchHistory]);

  const capture = useCallback(async () => {
    if (!isDetecting || !webcamRef.current) return;
    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    try {
      const res = await axios.post('http://localhost:8000/api/emotion/predict/', 
        { image: imageSrc },
        { headers: getHeaders() }
      );
      
      const newEmotion = res.data.emotion;
      setConfidence(res.data.confidence || 0);

      if (newEmotion && newEmotion !== emotion && newEmotion !== 'Detecting...') {
        setEmotion(newEmotion);
        // Only generate new playlist if mood changed significantly
        generatePlaylist(newEmotion);
      } else if (emotion === 'Detecting...') {
        setEmotion(newEmotion);
        generatePlaylist(newEmotion);
      }
    } catch (e) {
      console.error('Prediction error', e);
    }
  }, [webcamRef, emotion, isDetecting, generatePlaylist, getHeaders]);

  useEffect(() => {
    // Poll the webcam every 3 seconds for emotion
    const intervalId = setInterval(capture, 3000);
    return () => clearInterval(intervalId);
  }, [capture]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const loadHistoryItem = (item) => {
    setEmotion(item.emotion);
    setSongs(item.songs);
    if(item.songs.length > 0) {
      setCurrentVideoId(item.songs[0].videoId);
    }
    setIsDetecting(false); // Stop live detection while viewing history
  };

  return (
    <div className="dashboard-layout">
      {/* Sidebar for History */}
      <div className="sidebar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '2rem' }}>
          <User size={24} color="var(--accent)" />
          <h2 style={{ fontSize: '1.25rem' }}>{user?.username}</h2>
        </div>
        
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: 'var(--text-secondary)' }}>
          <History size={18} /> History
        </h3>
        
        <div style={{ overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: '0.5rem', marginRight: '-1rem', paddingRight: '1rem' }}>
          {history.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>No history yet.</p>
          ) : (
            history.map((item) => (
              <div key={item.id} className="history-item" onClick={() => loadHistoryItem(item)}>
                <div style={{ textTransform: 'capitalize', fontWeight: 'bold' }}>{item.emotion} Mood</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  {new Date(item.created_at).toLocaleDateString()}
                </div>
              </div>
            ))
          )}
        </div>

        <button onClick={logout} className="btn-primary" style={{ marginTop: '1rem', background: 'transparent', border: '1px solid var(--danger)', color: 'var(--danger)', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}>
          <LogOut size={18} /> Logout
        </button>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <div className="top-bar">
          <h1 style={{ fontSize: '2rem' }}>Live Mood Station</h1>
          {isDetecting ? (
            <button onClick={() => setIsDetecting(false)} className="btn-primary" style={{ width: 'auto', display: 'flex', gap: '0.5rem', alignItems: 'center', background: 'transparent', border: '1px solid var(--accent)', color: 'var(--accent)' }}>
              <Pause size={18} /> Pause AI Detection
            </button>
          ) : (
             <button onClick={() => { setIsDetecting(true); setEmotion('Detecting...'); setSongs([]); }} className="btn-primary" style={{ width: 'auto', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
               <RefreshCw size={18} /> Resume Live AI
             </button>
          )}
        </div>

        <div className="webcam-section">
          {/* Tracker Module */}
          <div className="webcam-container">
            {isDetecting ? (
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                className="webcam"
              />
            ) : (
              <div style={{ width: '100%', height: '100%', background: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Live Detection Paused</span>
              </div>
            )}
            
            <div className="emotion-overlay">
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>CURRENT MOOD</div>
                <div className="emotion-title" style={{ color: emotion === 'happy' ? 'var(--success)' : emotion === 'angry' ? 'var(--danger)' : 'var(--accent)' }}>
                  {emotion}
                </div>
              </div>
              {isDetecting && (
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.75rem', marginBottom: '0.25rem' }}>Confidence: {Math.round(confidence * 100)}%</div>
                  <div className="confidence-bar-container">
                    <div className="confidence-bar" style={{ width: `${confidence * 100}%` }}></div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* YouTube Player Module */}
          <div className="webcam-container" style={{ background: '#000' }}>
            {currentVideoId ? (
              <iframe 
                width="100%" 
                height="100%" 
                src={`https://www.youtube.com/embed/${currentVideoId}?autoplay=1`} 
                title="YouTube video player" 
                frameBorder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowFullScreen
              ></iframe>
            ) : (
              <div style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                <Music size={48} style={{ opacity: 0.5, marginBottom: '1rem' }} />
                <p>Playlist will appear here soon.</p>
              </div>
            )}
          </div>
        </div>

        {/* Playlist Items */}
        <div>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Generated Playlist</h2>
          <div className="playlist-section">
            {songs.length === 0 ? (
               <div className="empty-state">
                 <RefreshCw size={32} style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }} />
                 Scanning emotions to build your perfect playlist...
               </div>
            ) : (
              songs.map((song, i) => (
                <div key={i} className="song-card" onClick={() => setCurrentVideoId(song.videoId)}>
                  <img src={song.thumbnail} alt={song.title} className="song-img" />
                  <div className="song-info">
                    <div className="song-title">{song.title}</div>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Click to play</div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
