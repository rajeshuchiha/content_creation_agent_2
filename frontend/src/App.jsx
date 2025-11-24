import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/LoginPage'
import Register from './pages/RegisterPage'
import Dashboard from './pages/DashboardPage'
import { AuthProvider } from './context/authContext'
import NavBar from './components/navBar'
import { PlatformProvider } from './context/platformContext'
import ProtectedRoute from './auth/ProtectedRoute'

function App() {

  return (
    <AuthProvider>
      <PlatformProvider>
        <div>
          <NavBar />
          <main className='main-content'>
            <Routes>
              <Route path='/' element={<Home />} />
              <Route 
                path='/dashboard' 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                  // <Dashboard />
                } 
              />
              <Route path='/login' element={<Login />} />
              <Route path='/register' element={<Register />} />
            </Routes>
          </main>
        </div>
      </PlatformProvider>
    </AuthProvider>
  )
}

// function App() {
//   return (
//     <div style={{ padding: '20px', background: 'lightblue' }}>
//       <h1 style={{ color: 'black' }}>Hello App</h1>
//     </div>
//   );
// }

export default App
