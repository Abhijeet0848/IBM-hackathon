import { useState } from 'react'
import LandingPage from './components/LandingPage'
import Dashboard from './components/Dashboard'
import MockInterviewModal from './components/MockInterviewModal'

function App() {
  const [currentView, setCurrentView] = useState('landing') // 'landing' | 'dashboard'
  const [activeTab, setActiveTab] = useState('eli10')
  const [showInterviewModal, setShowInterviewModal] = useState(false)

  const handleStartTab = (tabName = 'eli10') => {
    setActiveTab(tabName)
    setCurrentView('dashboard')
  }

  const handleGoHome = () => {
    setCurrentView('landing')
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-blue-600 selection:text-white">
      {currentView === 'landing' && (
        <LandingPage
          onStart={handleStartTab}
          onOpenInterview={() => setShowInterviewModal(true)}
        />
      )}

      {currentView === 'dashboard' && (
        <Dashboard
          initialTab={activeTab}
          onHomeClick={handleGoHome}
        />
      )}

      {showInterviewModal && (
        <MockInterviewModal
          onClose={() => setShowInterviewModal(false)}
          initialRole="Computer Science & AI Engineer"
        />
      )}
    </div>
  )
}

export default App
