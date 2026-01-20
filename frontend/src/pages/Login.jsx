import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { FiMail, FiLock, FiEye, FiEyeOff, FiArrowLeft } from 'react-icons/fi'
import { MdOutlineWavingHand } from 'react-icons/md'
import axios from 'axios'
import logoLight from '../assets/logos/logo-light.png'
import logoDark from '../assets/logos/logo-dark.png'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const Login = ({ onLogin }) => {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [darkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return document.documentElement.classList.contains('dark')
    }
    return false
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    if (!email || !password) {
      setError('الرجاء إدخال البريد الإلكتروني وكلمة المرور')
      return
    }

    setIsLoading(true)
    
    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        email,
        password
      })
      
      const { access_token } = response.data
      localStorage.setItem('token', access_token)
      
      // جلب بيانات المستخدم الكاملة
      const userResponse = await axios.get(`${API_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${access_token}`
        }
      })
      
      const userData = {
        id: userResponse.data.id,
        email: userResponse.data.email,
        name: userResponse.data.name || userResponse.data.email.split('@')[0],
        profile_picture: userResponse.data.profile_picture,
        is_admin: userResponse.data.is_admin || false,
        is_active: userResponse.data.is_active || true
      }
      
      onLogin(userData)
      navigate('/chat')
    } catch (err) {
      if (err.response?.status === 401) {
        setError('البريد الإلكتروني أو كلمة المرور غير صحيحة')
      } else {
        setError(err.response?.data?.detail || 'حدث خطأ في تسجيل الدخول')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background-light dark:bg-navy-dark flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-primary/5 dark:bg-primary/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-navy-light/5 dark:bg-navy-light/20 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-br from-primary/3 to-navy-medium/3 dark:from-primary/5 dark:to-navy-medium/10 rounded-full blur-3xl"></div>
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Logo & Welcome */}
        <div className="text-center mb-10">
          <div className="flex justify-center mb-6">
            <img 
              src={logoDark} 
              alt="MOJ AI Logo" 
              className="h-20 w-auto object-contain"
            />
          </div>
          <h1 className="text-3xl font-bold text-text-primary-light dark:text-text-primary-dark mb-3 flex items-center justify-center gap-2">
            مرحباً بك في MOJ AI
          </h1>
          <p className="text-text-secondary-light dark:text-text-secondary-dark text-base">
            نظام إدارة وسائل التواصل الاجتماعي بالذكاء الاصطناعي
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-card-light dark:bg-card-dark rounded-2xl shadow-2xl border border-border-light dark:border-border-dark p-8 backdrop-blur-sm">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Input */}
            <div>
              <label className="block text-sm font-medium text-text-primary-light dark:text-text-primary-dark mb-2">
                البريد الإلكتروني
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <FiMail className="text-gray-400" size={20} />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pr-10 pl-4 py-3 bg-accent-light dark:bg-navy-medium border border-border-light dark:border-border-dark rounded-xl text-text-primary-light dark:text-text-primary-dark placeholder-text-secondary-light dark:placeholder-text-secondary-dark focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
                  placeholder="example@email.com"
                  dir="ltr"
                />
              </div>
            </div>

            {/* Password Input */}
            <div>
              <label className="block text-sm font-medium text-text-primary-light dark:text-text-primary-dark mb-2">
                كلمة المرور
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <FiLock className="text-gray-400" size={20} />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pr-10 pl-12 py-3 bg-accent-light dark:bg-navy-medium border border-border-light dark:border-border-dark rounded-xl text-text-primary-light dark:text-text-primary-dark placeholder-text-secondary-light dark:placeholder-text-secondary-dark focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
                  placeholder="••••••••"
                  dir="ltr"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 left-0 pl-3 flex items-center text-text-secondary-light dark:text-text-secondary-dark hover:text-text-primary-light dark:hover:text-text-primary-dark"
                >
                  {showPassword ? <FiEyeOff size={20} /> : <FiEye size={20} />}
                </button>
              </div>
            </div>

            {/* Remember & Forgot */}
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-primary bg-accent-light border-border-light rounded focus:ring-primary focus:ring-2 dark:bg-navy-medium dark:border-border-dark"
                />
                <span className="text-text-secondary-light dark:text-text-secondary-dark">تذكرني</span>
              </label>
              <Link to="#" className="text-primary hover:text-secondary font-medium">
                نسيت كلمة المرور؟
              </Link>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 px-4 py-3 rounded-xl text-sm">
                {error}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-primary hover:bg-secondary text-white font-semibold py-3.5 px-4 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  جاري تسجيل الدخول...
                </>
              ) : (
                <>
                  تسجيل الدخول
                  <FiArrowLeft />
                </>
              )}
            </button>
          </form>

          {/* Sign Up Link */}
          <p className="text-center text-sm text-text-secondary-light dark:text-text-secondary-dark mt-6">
            ليس لديك حساب؟{' '}
            <Link to="/register" className="text-primary hover:text-secondary font-semibold">
              إنشاء حساب جديد
            </Link>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-text-secondary-light dark:text-text-secondary-dark mt-6">
          بتسجيل الدخول، أنت توافق على{' '}
          <a href="#" className="text-primary hover:underline">شروط الخدمة</a>
          {' '}و{' '}
          <a href="#" className="text-primary hover:underline">سياسة الخصوصية</a>
        </p>
      </div>
    </div>
  )
}

export default Login
