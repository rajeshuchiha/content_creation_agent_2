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
              </Route>

              <Route element={<AppLayout />}>
                <Route
                  path='/dashboard'
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                    // <Dashboard />
                  }
                />
                <Route
                  path='/history'
                  element={
                    <ProtectedRoute>
                      <History />
                    </ProtectedRoute>
                    // <History />
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

// function App() {
//   return (
//     <div style={{ padding: '20px', background: 'lightblue' }}>
//       <h1 style={{ color: 'black' }}>Hello App</h1>
//     </div>
//   );
// }

export default App
