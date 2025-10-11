import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { login, saveToken } from '../api'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const navigate = useNavigate()

  async function submit(e){
    e.preventDefault()
    setError(null)
    
    if (!email.trim() || !password) {
      setError('Please fill in all fields')
      return
    }
    
    setLoading(true)
    try{
      const res = await login({ email: email.trim(), password, name: '' })
      saveToken(res.access_token)
      navigate('/dashboard')
    }catch(err){
      setError(err?.response?.data?.detail || 'Login failed. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>📚 Welcome Back</h2>
          <p className="auth-subtitle">Continue with your documents</p>
        </div>
        
        <form onSubmit={submit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">📧 Email Address</label>
            <input 
              id="email"
              type="email"
              value={email} 
              onChange={e=>setEmail(e.target.value)} 
              placeholder="Enter your email address"
              className="auth-input"
              required 
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">🔒 Password</label>
            <div className="password-input-wrapper">
              <input 
                id="password"
                type={showPassword ? "text" : "password"}
                value={password} 
                onChange={e=>setPassword(e.target.value)} 
                placeholder="Enter your password"
                className="auth-input"
                required 
                disabled={loading}
              />
              <button 
                type="button" 
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                disabled={loading}
              >
                {showPassword ? '🙈' : '👁️'}
              </button>
            </div>
          </div>

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          <button 
            className="btn btn-primary auth-submit" 
            type="submit"
            disabled={loading}
          >
            {loading ? (
              <>⏳ Signing In...</>
            ) : (
              <>🚀 Sign In</>
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p>Don't have an account? <Link to="/register" className="auth-link">Create one here</Link></p>
        </div>

        <div className="auth-demo">
          <div className="demo-info">
            <h4>🎯 Quick Demo</h4>
            <p>Try uploading a document and ask questions like:</p>
            <ul>
              <li>"What are the main topics covered?"</li>
              <li>"Summarize the key points"</li>
              <li>"What does this document say about...?"</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
