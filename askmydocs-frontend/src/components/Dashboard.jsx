import React, { useState, useEffect } from 'react'
import { uploadFile, queryDocs, getToken, saveToken, getCurrentUser, changePassword } from '../api'

export default function Dashboard(){
  const [tab, setTab] = useState('upload')
  const [file, setFile] = useState(null)
  const [text, setText] = useState('')
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [msg, setMsg] = useState('')
  const [user, setUser] = useState(null)
  const [selectedModel, setSelectedModel] = useState('llama3')
  const [showPasswordForm, setShowPasswordForm] = useState(false)
  const [passwordData, setPasswordData] = useState({ current: '', new: '', confirm: '' })

  // Auto-logout after 15 minutes of inactivity
  useEffect(() => {
    let timeout
    const resetTimeout = () => {
      clearTimeout(timeout)
      timeout = setTimeout(() => {
        logout()
      }, 15 * 60 * 1000) // 15 minutes
    }
    
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart']
    events.forEach(event => {
      document.addEventListener(event, resetTimeout, true)
    })
    
    resetTimeout() // Initial timeout
    
    return () => {
      clearTimeout(timeout)
      events.forEach(event => {
        document.removeEventListener(event, resetTimeout, true)
      })
    }
  }, [])

  useEffect(() => {
    loadUserInfo()
  }, [])

  async function loadUserInfo() {
    try {
      const userInfo = await getCurrentUser()
      setUser(userInfo)
    } catch (err) {
      console.error('Failed to load user info:', err)
    }
  }

  function logout() {
    localStorage.removeItem('am_token')
    window.location.href = '/login'
  }

  async function handlePasswordChange(e) {
    e.preventDefault()
    if (passwordData.new !== passwordData.confirm) {
      setMsg('New passwords do not match')
      return
    }
    if (passwordData.new.length < 6) {
      setMsg('New password must be at least 6 characters')
      return
    }
    
    setLoading(true)
    try {
      await changePassword(passwordData.current, passwordData.new)
      setMsg('Password updated successfully')
      setShowPasswordForm(false)
      setPasswordData({ current: '', new: '', confirm: '' })
    } catch (err) {
      setMsg(err?.response?.data?.detail || 'Failed to update password')
    } finally {
      setLoading(false)
    }
  }

  async function handleUpload(e){
    e.preventDefault()
    if(!file){ setMsg('Please select a file'); return }
    setLoading(true)
    try{
      const res = await uploadFile(file)
      setMsg(`Uploaded: ${res.filename}`)
    }catch(err){
      setMsg(err?.response?.data?.detail || 'Upload failed')
    }finally{ setLoading(false) }
  }

  async function handleAddText(e){
    e.preventDefault()
    if(!text.trim()){ setMsg('Enter some text'); return }
    setLoading(true)
    try{
      // use chat/add_document endpoint to add the text
      await fetch((import.meta.env.VITE_API_BASE||'http://localhost:8000')+'/chat/add_document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getToken()}` },
        body: JSON.stringify({ title: `doc-${Date.now()}`, content: text })
      })
      setMsg('Text added for indexing')
      setText('')
    }catch(err){
      setMsg('Failed to add text')
    }finally{ setLoading(false) }
  }

  async function handleQuery(e){
    e.preventDefault()
    if(!query.trim()){ setMsg('Enter a question'); return }
    setLoading(true)
    try{
      const res = await queryDocs(query, selectedModel)
      setAnswer(res.answer)
      setMsg(`Response from ${res.llm_used || selectedModel}`)
    }catch(err){
      setMsg('Query failed')
    }finally{ setLoading(false) }
  }

  return (
    <div className="dashboard-container">
      {/* Compact Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <div className="brand-section">
            <h1>📚 AskMyDocs</h1>
            {user && <span className="user-greeting">Hello, <strong>{user.name}</strong></span>}
          </div>
          <div className="header-actions">
            <button 
              className="btn btn-ghost" 
              onClick={() => setShowPasswordForm(!showPasswordForm)}
              title="Change Password"
            >
              🔑
            </button>
            <button className="btn btn-ghost" onClick={logout} title="Logout">
              🚪
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="dashboard-main">
        {/* Password change modal */}
        {showPasswordForm && (
          <div className="modal-overlay" onClick={() => setShowPasswordForm(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <h3>🔑 Change Password</h3>
              <form onSubmit={handlePasswordChange}>
                <input
                  type="password"
                  placeholder="Current Password"
                  value={passwordData.current}
                  onChange={(e) => setPasswordData({...passwordData, current: e.target.value})}
                  required
                />
                <input
                  type="password"
                  placeholder="New Password (min. 6 chars)"
                  value={passwordData.new}
                  onChange={(e) => setPasswordData({...passwordData, new: e.target.value})}
                  required
                />
                <input
                  type="password"
                  placeholder="Confirm New Password"
                  value={passwordData.confirm}
                  onChange={(e) => setPasswordData({...passwordData, confirm: e.target.value})}
                  required
                />
                <div className="modal-actions">
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Updating...' : 'Update Password'}
                  </button>
                  <button type="button" className="btn btn-secondary" onClick={() => setShowPasswordForm(false)}>
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Content Grid */}
        <div className="content-grid">
          {/* Left Panel - Upload/Text */}
          <div className="left-panel">
            <div className="panel-tabs">
              <button 
                className={`panel-tab ${tab==='upload'? 'active':''}`} 
                onClick={()=>setTab('upload')}
              >
                📄 Documents
              </button>
              <button 
                className={`panel-tab ${tab==='text'? 'active':''}`} 
                onClick={()=>setTab('text')}
              >
                ✏️ Text
              </button>
            </div>

            {tab==='upload' && (
              <div className="panel-content">
                <h3>Upload Document</h3>
                <div className="upload-section">
                  <div className="file-input-row">
                    <input 
                      type="file" 
                      accept=".pdf,.txt,.md" 
                      onChange={e=>setFile(e.target.files[0])} 
                      className="file-input"
                      id="file-upload"
                    />
                    <label htmlFor="file-upload" className="file-select-btn">
                      {file ? `📎 ${file.name}` : '📎 Choose File'}
                    </label>
                    <button 
                      className="btn btn-primary upload-btn" 
                      onClick={handleUpload} 
                      disabled={loading || !file}
                    >
                      {loading ? '⏳ Uploading...' : '⬆️ Upload'}
                    </button>
                  </div>
                  <p className="help-text">PDF, TXT, or MD files supported</p>
                </div>
              </div>
            )}

            {tab==='text' && (
              <div className="panel-content">
                <h3>Add Text Content</h3>
                <div className="text-section">
                  <textarea 
                    value={text} 
                    onChange={e=>setText(e.target.value)} 
                    rows={6} 
                    placeholder="Enter your text content here..."
                    className="text-input"
                  />
                  <button 
                    className="btn btn-primary" 
                    onClick={handleAddText} 
                    disabled={loading || !text.trim()}
                  >
                    {loading ? '⏳ Adding...' : '➕ Add Text'}
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Right Panel - Chat */}
          <div className="right-panel">
            <div className="chat-header">
              <h3>🤖 Ask Your Documents</h3>
              <div className="model-selection">
                <label className="model-label">Model:</label>
                <div className="radio-group">
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="model"
                      value="llama3"
                      checked={selectedModel === 'llama3'}
                      onChange={(e) => setSelectedModel(e.target.value)}
                    />
                    <span>🦙 Llama3</span>
                  </label>
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="model"
                      value="openai"
                      checked={selectedModel === 'openai'}
                      onChange={(e) => setSelectedModel(e.target.value)}
                    />
                    <span>🤖 OpenAI</span>
                  </label>
                </div>
              </div>
            </div>
            <div className="chat-content">
              {answer && (
                <div className="answer-bubble">
                  <div className="answer-header">💡 Answer</div>
                  <div className="answer-text">{answer}</div>
                </div>
              )}
              
              {msg && (
                <div className={`status-message ${msg.includes('failed') || msg.includes('error') ? 'error' : 'success'}`}>
                  {msg}
                </div>
              )}
            </div>
            
            <div className="chat-input">
              <div className="input-row">
                <input 
                  value={query} 
                  onChange={e=>setQuery(e.target.value)} 
                  placeholder="Ask about your documents..." 
                  className="query-input"
                  disabled={loading}
                  onKeyPress={e => e.key === 'Enter' && handleQuery(e)}
                />
                <button 
                  className="btn btn-primary ask-btn" 
                  onClick={handleQuery} 
                  disabled={loading || !query.trim()}
                >
                  {loading ? '🤔' : '❓'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
