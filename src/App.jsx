import { useState } from 'react'
import LandingPage from './components/LandingPage'
import Dashboard from './components/Dashboard'

function App() {
  const [currentView, setCurrentView] = useState('landing') // 'landing' | 'dashboard'
  const [activeTab, setActiveTab] = useState('syllabus')
  const [extractedSyllabus, setExtractedSyllabus] = useState(null)

  const handleStartTab = (tabName = 'syllabus') => {
    setActiveTab(tabName)
    setCurrentView('dashboard')
  }

  const handleGoHome = () => {
    setCurrentView('landing')
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-600 selection:text-white">
      {currentView === 'landing' && (
        <LandingPage
          onStart={handleStartTab}
        />
      )}

      {currentView === 'dashboard' && (
        <Dashboard
          initialTab={activeTab}
          onHomeClick={handleGoHome}
          extractedSyllabus={extractedSyllabus}
          onSyllabusExtracted={setExtractedSyllabus}
        />
      )}
    </div>
  )
}

export default App
