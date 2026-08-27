import { useState } from 'react'
import LandingPage from './components/LandingPage'
import Dashboard from './components/Dashboard'
import MockInterviewModal from './components/MockInterviewModal'

function App() {
  const [currentView, setCurrentView] = useState('landing') // 'landing' | 'dashboard'
  const [showInterviewModal, setShowInterviewModal] = useState(false)

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-blue-600 selection:text-white">
      {currentView === 'landing' && (
        <LandingPage
          onStart={() => setCurrentView('dashboard')}
          onOpenInterview={() => setShowInterviewModal(true)}
        />
      )}

      {currentView === 'dashboard' && (
        <Dashboard />
      )}

      {showInterviewModal && (
        <MockInterviewModal
          onClose={() => setShowInterviewModal(false)}
          initialRole="Senior React Developer"
        />
      )}
    </div>
  )
}

export default App

