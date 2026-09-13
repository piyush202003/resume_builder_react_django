import React from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { useSelector } from 'react-redux'
import { Loader } from 'lucide-react'
import Login from './Login'


const Layout = () => {

  const { user, loading} = useSelector(state => state.auth)

  if(loading){
    return <Loader />
  }

  return (
    <>
    {
      user ? (
        <div className='min-h-screen bg-gray-300'>
          <Navbar />
          <div>
            <Outlet />
          </div>
        </div>
      ): (
        <Login />
      )
    }
      
    </>
  )
}

export default Layout
