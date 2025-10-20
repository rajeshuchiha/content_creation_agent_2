import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Login from './components/auth/login'
import { Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Dashboard from './pages/DashboardPage'
import { AuthProvider } from './context/authContext'
import NavBar from './components/navBar'
import Register from './components/auth/Register'


function App() {

  return (
    <AuthProvider>
      <div>
        <NavBar />
        <main className='main-content'>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/dashboard' element={<Dashboard />} /> 
            <Route path='/login' element={<Login />} />
            <Route path='/register' element={<Register />} />
          </Routes>
        </main>
      </div>
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
