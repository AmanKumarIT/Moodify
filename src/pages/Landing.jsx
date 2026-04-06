import React from 'react';
import { Link } from 'react-router-dom';
import { Music, Camera, Zap } from 'lucide-react';

export default function Landing() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', textAlign: 'center', padding: '2rem' }}>
      <div className="glass-panel" style={{ maxWidth: '800px', animation: 'slideUp 0.8s ease forwards' }}>
        <h1 style={{ fontSize: '3.5rem', marginBottom: '1rem', background: 'linear-gradient(to right, var(--accent), #a855f7)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Moodify
        </h1>
        <p style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', marginBottom: '2.5rem' }}>
          Your real-time emotion-based music companion. We analyze your mood and generate the perfect YouTube playlist instantly.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginBottom: '3rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
            <Camera size={48} color="var(--accent)" />
            <span style={{ fontWeight: '500' }}>Live Detection</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
            <Zap size={48} color="var(--success)" />
            <span style={{ fontWeight: '500' }}>AI Powered</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
            <Music size={48} color="#a855f7" />
            <span style={{ fontWeight: '500' }}>Dynamic Playlists</span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <Link to="/register" className="btn-primary" style={{ width: 'auto', padding: '1rem 2rem', fontSize: '1.125rem' }}>
            Get Started Free
          </Link>
          <Link to="/login" className="btn-primary" style={{ width: 'auto', padding: '1rem 2rem', fontSize: '1.125rem', background: 'transparent', border: '1px solid var(--accent)' }}>
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
