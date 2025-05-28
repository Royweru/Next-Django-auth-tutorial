'use client'
import React, { useEffect, useState } from 'react'
import Cookies from 'js-cookie'
import { ACCESS_TOKEN } from '@/constants';
import { AuthService } from '@/lib/services';
import { redirect } from 'next/navigation';
const ProtectedPagesLayout = ({
  children
}:{
  children:React.ReactNode
}) => {
  const  [loading, setLoading] = useState(true);
   const [ user,setUser]  = useState<null | User>(null);
   
    useEffect(() => {
    const initAuth = async () => {
      const accessToken = Cookies.get(ACCESS_TOKEN);
      if (accessToken) {
        try {
          const res = await AuthService.getUserProfile();
          if (res) {
            setUser(res);
          }
        } catch (error) {
          console.error('Failed to fetch user data:', error);
          AuthService.logout();
        }
      }
      setLoading(false);
    };
    
    initAuth();
  }, []);

  if (loading) {
    return <div className=' min-h-screen flex items-center justify-center font-bold bg-gray-100'>Loading...</div>;
  }

  if (!user && !loading) {
    return redirect('/login');
  }
  return (
    <div>
      {children}
    </div>
  )
}

export default ProtectedPagesLayout