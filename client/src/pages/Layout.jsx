import React from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar'

const Layout = () => {
  return (
    <div className='min-h-screen bg-gray-300'>
      <Navbar />
      <div>
        <Outlet />
      </div>
    </div>
  )
}

export default Layout
