import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Route, Routes } from 'react-router-dom'
import { AuthProvider } from './context/authContext'
import NavBar from './components/navBar'
import { PlatformProvider } from './context/platformContext'
import ProtectedRoute from './auth/ProtectedRoute'
import Home from './pages/Home'
import Login from './pages/LoginPage'
import Register from './pages/RegisterPage'
import Dashboard from './pages/DashboardPage'
import History from './pages/HistoryPage'
import { AppLayout, FullPageLayout } from './layouts'

function App() {

  return (
    <AuthProvider>
      <PlatformProvider>
        <div>
          {/* <NavBar /> */}
          <main className='main-content'>
            <Routes>
              <Route element={<FullPageLayout />}>
                <Route path='/' element={<Home />} />
                <Route path='/login' element={<Login />} />
                <Route path='/register' element={<Register />} />
                <Route
                  path='/history'
                  element={
                    // <ProtectedRoute>
                    //   <History />
                    // </ProtectedRoute>
                    <History />
                  }
                />
              </Route>

              <Route element={<AppLayout />}>
                <Route
                  path='/dashboard'
                  element={
                    // <ProtectedRoute>
                    //   <Dashboard />
                    // </ProtectedRoute>
                    <Dashboard />
                  }
                />
              </Route>

            </Routes>
          </main>
        </div>
      </PlatformProvider>
    </AuthProvider>
  )
}

export default App
