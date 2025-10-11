import axios from 'axios'

const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const client = axios.create({ baseURL: BASE, headers: { 'Content-Type': 'application/json' } })

export function setAuthToken(token){
  if(token) client.defaults.headers.common['Authorization'] = `Bearer ${token}`
  else delete client.defaults.headers.common['Authorization']
}

export function saveToken(token){
  localStorage.setItem('am_token', token)
  setAuthToken(token)
}

export function getToken(){
  return localStorage.getItem('am_token')
}

export async function register(user){
  const res = await client.post('/auth/register', user)
  return res.data
}

export async function login(user){
  const res = await client.post('/auth/login', user)
  return res.data
}

export async function uploadFile(file){
  const form = new FormData()
  form.append('file', file)
  const res = await client.post('/upload/', form, { headers: { 'Content-Type': 'multipart/form-data' } })
  return res.data
}

export async function queryDocs(query){
  const res = await client.post('/chat/query', { query })
  return res.data
}

export async function getCurrentUser(){
  const res = await client.get('/auth/me')
  return res.data
}

export async function changePassword(currentPassword, newPassword){
  const res = await client.put('/auth/change-password', {
    current_password: currentPassword,
    new_password: newPassword
  })
  return res.data
}
