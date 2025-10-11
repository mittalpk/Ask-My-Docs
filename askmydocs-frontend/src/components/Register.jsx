import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register, saveToken } from '../api'

export default function Register(){
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const navigate = useNavigate()

  function validateForm() {
    if (!name.trim()) {
      setError('Name is required')
      return false
    }
    if (!email.trim()) {
      setError('Email is required')
      return false
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters long')
      return false
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return false
    }
    return true
  }

  async function submit(e){
    e.preventDefault()
    setError(null)
    
    if (!validateForm()) {
      return
    }
    
    setLoading(true)
    try{
      const res = await register({ name: name.trim(), email: email.trim(), password })
      saveToken(res.access_token)
      navigate('/dashboard')
    }catch(err){
      setError(err?.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>📚 Create Your Account</h2>
          <p className="auth-subtitle">Join AskMyDocs and start querying your documents with AI</p>
        </div>
        
        <form onSubmit={submit} className="auth-form">
          <div className="form-group">
            <label htmlFor="name">👤 Full Name</label>
            <input 
              id="name"
              type="text"
              value={name} 
              onChange={e=>setName(e.target.value)} 
              placeholder="Enter your full name"
              className="auth-input"
              required 
              disabled={loading}
            />
          </div>

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
                placeholder="Create a strong password (min. 6 characters)"
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

          <div className="form-group">
            <label htmlFor="confirmPassword">🔒 Confirm Password</label>
            <input 
              id="confirmPassword"
              type={showPassword ? "text" : "password"}
              value={confirmPassword} 
              onChange={e=>setConfirmPassword(e.target.value)} 
              placeholder="Confirm your password"
              className="auth-input"
              required 
              disabled={loading}
            />
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
              <>⏳ Creating Account...</>
            ) : (
              <>🚀 Create Account</>
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p>Already have an account? <Link to="/login" className="auth-link">Sign in here</Link></p>
        </div>

        <div className="auth-features">
          <h4>✨ What you'll get:</h4>
          <ul>
            <li>🤖 AI-powered document analysis</li>
            <li>📄 Upload PDFs, text files, and more</li>
            <li>💬 Natural language querying</li>
            <li>🔒 Secure document storage</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
