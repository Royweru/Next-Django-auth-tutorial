'use client'

import { useAuth } from '@/components/providers/authContext';
import { AuthService } from '@/lib/services';
import { useRouter } from 'next/navigation';
import React from 'react'

const DashboardPage = () => {
  const router= useRouter()
 
    const onLogout = async () => {
      try {
         await AuthService.logout();
         window.location.reload()
      } catch (error) {
        console.log("logout error on the dashboard : ",error) 
      }
    }
  return (
    <div className=' p-20'>
      <div className=' flex items-center justify-between  w-full relative'>
         <h1 className='text-3xl font-bold text-gray-800'>Dashboard</h1>
          <button 
          className=' py-3.5 px-6 cursor-pointer font-semibold rounded-lg
           bg-gray-100/90 hover:bg-gray-100'
           onClick={onLogout}
           >
            <span className='text-blue-500 hover:text-blue-700'
            >Logout</span>
          </button>
      </div>
    </div>
  )
}

export default DashboardPage