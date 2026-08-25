import React from 'react';
import { ArrowRight, BrainCircuit, Target, Briefcase } from 'lucide-react';

const LandingPage = ({ onStart }) => {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Simple Header */}
      <header style={{ padding: '1.5rem 2rem', borderBottom: '1px solid var(--border-color)', background: 'white' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', alignItems: 'center', fontWeight: 600, fontSize: '1.25rem' }}>
          <span style={{ color: 'var(--primary)', marginRight: '0.5rem' }}>IBM</span> SkillsBuild | Career Copilot
        </div>
      </header>

      {/* Hero Section */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '4rem 2rem', textAlign: 'center' }}>
        <div className="animate-fade-in" style={{ maxWidth: '700px' }}>
          <h1 style={{ fontSize: '3.5rem', lineHeight: 1.2, marginBottom: '1.5rem' }}>
            Accelerate your career with AI-driven insights.
          </h1>
          
          <p className="text-muted" style={{ fontSize: '1.125rem', marginBottom: '2.5rem' }}>
            Analyze your resume against any job description. Identify skill gaps instantly and get a personalized learning roadmap with IBM SkillsBuild.
          </p>

          <button className="btn btn-primary" onClick={onStart} style={{ fontSize: '1rem', padding: '0.75rem 2rem' }}>
            Get Started <ArrowRight size={18} />
          </button>
        </div>

        {/* Feature Grid */}
        <div className="animate-fade-in" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', width: '100%', maxWidth: '1000px', marginTop: '5rem', animationDelay: '0.2s' }}>
          
          <div className="card" style={{ display: 'flex', alignItems: 'flex-start', textAlign: 'left', gap: '1rem' }}>
            <BrainCircuit size={24} className="text-primary" style={{ flexShrink: 0, marginTop: '0.25rem' }} />
            <div>
              <h3 style={{ fontSize: '1.125rem', marginBottom: '0.5rem' }}>Skill Gap Analysis</h3>
              <p className="text-muted" style={{ fontSize: '0.875rem' }}>Automatically cross-reference your experience with specific role requirements.</p>
            </div>
          </div>
          
          <div className="card" style={{ display: 'flex', alignItems: 'flex-start', textAlign: 'left', gap: '1rem' }}>
            <Target size={24} className="text-primary" style={{ flexShrink: 0, marginTop: '0.25rem' }} />
            <div>
              <h3 style={{ fontSize: '1.125rem', marginBottom: '0.5rem' }}>Custom Roadmaps</h3>
              <p className="text-muted" style={{ fontSize: '0.875rem' }}>Receive targeted IBM SkillsBuild course recommendations to bridge your gaps.</p>
            </div>
          </div>

          <div className="card" style={{ display: 'flex', alignItems: 'flex-start', textAlign: 'left', gap: '1rem' }}>
            <Briefcase size={24} className="text-primary" style={{ flexShrink: 0, marginTop: '0.25rem' }} />
            <div>
              <h3 style={{ fontSize: '1.125rem', marginBottom: '0.5rem' }}>Mock Interviews</h3>
              <p className="text-muted" style={{ fontSize: '0.875rem' }}>Practice your answers in real-time with an intelligent AI recruiter.</p>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
};

export default LandingPage;
