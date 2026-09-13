import { Route, Routes } from 'react-router-dom'
import Layout from './pages/Layout'
import Home from './pages/Home'
import ResumeBuilder from './pages/ResumeBuilder'
import Dashboard from './pages/Dashboard'
import Preview from './pages/Preview'
import Login from './pages/Login'
import { useDispatch } from 'react-redux'
import { login, setLoading } from './app/features/authSlice'
import { useEffect } from 'react'
import toast, { Toaster } from 'react-hot-toast'
import api from './config/api'

function App() {

  const dispatch = useDispatch()
  const getUserData = async ()=>{
    const token = localStorage.getItem('token')
    try{
      if(token){
        const { data } = await api.get('api/users/data/', {
          headers:{Authorization:`Bearer ${token}`}
        })
        if(data.user){
          dispatch(login({token, user: data.user}))
        }
        dispatch(setLoading(false))
      }else{
        dispatch(setLoading(false))
      }
    }catch(error){
      dispatch(setLoading(false))
    }
  }

  useEffect(()=>{
    getUserData()
  },[])

  return (
    <>
      <Toaster />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='app' element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path='builder/:resumeId' element={<ResumeBuilder />} />
        </Route>

        <Route path='view/:resumeId' element={<Preview />} />
        <Route path='login' element={<Login />} />

        
      </Routes>
    </>
  )
}

export default App
