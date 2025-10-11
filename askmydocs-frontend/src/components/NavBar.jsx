import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getToken, setAuthToken } from '../api'

export default function NavBar(){
  const navigate = useNavigate()
  const token = getToken()

  function logout(){
    localStorage.removeItem('am_token')
    setAuthToken(null)
    navigate('/login')
  }

  return (
    <nav className="nav">
      <div className="nav-left">
        <Link to="/dashboard" className="brand">AskMyDocs</Link>
      </div>
      <div className="nav-right">
        {token ? (
          <button onClick={logout} className="btn">Logout</button>
        ) : (
          <>
            <Link to="/login" className="btn">Login</Link>
            <Link to="/register" className="btn btn-primary">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  )
}
