import React, { useState } from 'react';
import { Upload, FileText, CheckCircle2, AlertCircle, PlayCircle, Loader2 } from 'lucide-react';
import MockInterviewModal from './MockInterviewModal';

const Dashboard = () => {
  const [step, setStep] = useState('upload'); // 'upload' | 'analyzing' | 'results'
  const [showInterview, setShowInterview] = useState(false);

  const handleAnalyze = () => {
    setStep('analyzing');
    setTimeout(() => {
      setStep('results');
    }, 2000); 
  };

  return (
    <div style={{ background: 'var(--bg)', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Simple Header */}
      <header style={{ padding: '1rem 2rem', borderBottom: '1px solid var(--border-color)', background: 'white' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ fontWeight: 600, fontSize: '1.25rem' }}>
             Career Copilot
          </div>
          {step === 'results' && (
            <button className="btn btn-outline" onClick={() => setShowInterview(true)}>
              <PlayCircle size={16} /> Practice Interview
            </button>
          )}
        </div>
      </header>

      {/* Main Content Area */}
      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem', width: '100%', flex: 1 }}>
        <div style={{ display: 'grid', gridTemplateColumns: step === 'results' ? '1fr 2fr' : '1fr', gap: '2rem' }}>
          
          {/* Left Column: Input Forms */}
          <div className="card animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', alignSelf: 'start' }}>
            <div>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 500, marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                <FileText size={16} className="text-muted" /> Target Job Description
              </label>
              <textarea 
                className="input-field" 
                rows="5" 
                placeholder="Paste the job description here..."
                defaultValue="Junior React Developer. Requirements: 1+ year React, state management (Redux/Zustand), Tailwind CSS, basic understanding of CI/CD and testing (Jest)."
              ></textarea>
            </div>

            <div>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 500, marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                <Upload size={16} className="text-muted" /> Resume Upload (PDF)
              </label>
              <div style={{ 
                border: '1px dashed var(--border-color)', 
                borderRadius: 'var(--radius)', 
                padding: '2rem 1rem', 
                textAlign: 'center',
                background: '#fafafa',
                cursor: 'pointer'
              }}>
                <p className="text-muted" style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>Drag & drop file or click to browse</p>
                <div style={{ display: 'inline-block', padding: '0.25rem 0.75rem', background: 'var(--secondary)', borderRadius: '4px', fontSize: '0.75rem', color: 'var(--fg)', fontWeight: 500 }}>
                  resume_johndoe.pdf
                </div>
              </div>
            </div>

            {step === 'upload' && (
              <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleAnalyze}>
                Run Analysis
              </button>
            )}

            {step === 'analyzing' && (
              <div style={{ textAlign: 'center', padding: '1rem', color: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                <Loader2 size={20} className="animate-pulse" style={{ animation: 'spin 2s linear infinite' }} />
                <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>Processing document...</span>
              </div>
            )}
          </div>

          {/* Right Column: Results Dashboard */}
          {step === 'results' && (
            <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              
              <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <h3 style={{ fontSize: '1.125rem', marginBottom: '0.25rem' }}>Match Score</h3>
                  <p className="text-muted" style={{ fontSize: '0.875rem' }}>Based on semantic keyword matching.</p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--fg)', lineHeight: 1 }}>68%</div>
                  <div style={{ background: '#fef9c3', color: '#a16207', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 600 }}>Partial Match</div>
                </div>
              </div>

              <div className="card">
                <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>Skills Assessment</h3>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  
                  {/* Verified Skills */}
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                      <CheckCircle2 size={16} color="var(--success)" />
                      <h4 style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--fg)' }}>Verified Competencies</h4>
                    </div>
                    <p className="text-muted" style={{ fontSize: '0.875rem', marginLeft: '1.5rem' }}>React.js, JavaScript (ES6+), HTML/CSS</p>
                  </div>

                  {/* Missing Skills & Recommendations */}
                  <div style={{ marginTop: '0.5rem', padding: '1rem', background: 'var(--danger-bg)', borderRadius: 'var(--radius)', border: '1px solid #fecaca' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                      <AlertCircle size={16} color="var(--danger)" />
                      <h4 style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--danger)' }}>Identified Skill Gaps</h4>
                    </div>
                    <p style={{ fontSize: '0.875rem', color: '#7f1d1d', marginLeft: '1.5rem', marginBottom: '1rem' }}>
                      Missing experience with State Management (Redux/Zustand) and Testing frameworks (Jest).
                    </p>
                    
                    <div style={{ marginLeft: '1.5rem' }}>
                      <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '0.05em' }}>Recommended Learning:</span>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.5rem' }}>
                        <a href="#" style={{ display: 'block', padding: '0.75rem', background: 'white', borderRadius: '4px', color: 'var(--primary)', textDecoration: 'none', border: '1px solid var(--border-color)', fontSize: '0.875rem', fontWeight: 500 }}>
                          Introduction to State Management Patterns (2 hrs)
                        </a>
                        <a href="#" style={{ display: 'block', padding: '0.75rem', background: 'white', borderRadius: '4px', color: 'var(--primary)', textDecoration: 'none', border: '1px solid var(--border-color)', fontSize: '0.875rem', fontWeight: 500 }}>
                          Software Testing Basics with JavaScript (3 hrs)
                        </a>
                      </div>
                    </div>
                  </div>

                </div>
              </div>

            </div>
          )}
        </div>
      </main>

      {showInterview && <MockInterviewModal onClose={() => setShowInterview(false)} />}
    </div>
  );
};

export default Dashboard;
