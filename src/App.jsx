import { useState } from 'react'
import LandingPage from './components/LandingPage'
import Dashboard from './components/Dashboard'
import './index.css'

function App() {
  const [currentView, setCurrentView] = useState('landing') // 'landing' | 'dashboard' | 'interview'
  
  // Mock Data State
  const [resumeData, setResumeData] = useState(null)
  
  const handleStart = () => {
    setCurrentView('dashboard')
  }

  return (
    <div className="app-container">
      {/* Dynamic View Rendering */}
      {currentView === 'landing' && <LandingPage onStart={handleStart} />}
      {currentView === 'dashboard' && <Dashboard />}
    </div>
  )
}

export default App
