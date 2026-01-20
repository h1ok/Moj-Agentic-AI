import { useState } from 'react'
import { MdDashboard, MdSettings, MdPerson, MdLogout } from 'react-icons/md'
import { BsListUl, BsFileText } from 'react-icons/bs'
import { FiSun, FiMoon, FiMessageSquare, FiUser, FiChevronUp } from 'react-icons/fi'
import { useNavigate } from 'react-router-dom'
import logoLight from '../assets/logos/logo-light.png'
import logoDark from '../assets/logos/logo-dark.png'

const Sidebar = ({ darkMode, setDarkMode, user, onLogout }) => {
  const navigate = useNavigate()
  const [showUserMenu, setShowUserMenu] = useState(false)

  const handleLogout = () => {
    navigate('/login')
  }

  return (
    <aside className="hidden md:flex flex-col w-[260px] bg-sidebar-light dark:bg-sidebar-dark h-full shrink-0 transition-all duration-300">
      <div className="flex flex-col h-full p-4 gap-4">
        {/* فاصل خفيف في الأعلى */}
        <div className="border-b border-border-light dark:border-border-dark pb-4">
          <div className="flex justify-center px-3 pt-4">
            <img 
              src={darkMode ? logoLight : logoDark} 
              alt="MOJ AI Logo" 
              className="h-14 w-auto object-contain"
            />
          </div>
        </div>

        <button className="flex w-full items-center gap-3 px-4 py-3 rounded-xl bg-primary hover:bg-secondary transition-all duration-200 shadow-sm group">
          <MdDashboard className="text-white group-hover:scale-110 transition-transform" size={22} />
          <span className="text-sm font-semibold text-white">+ محادثة جديدة</span>
        </button>

        {/* قسم المحادثات السابقة */}
        <div className="flex flex-col gap-2">
          <h3 className="text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark px-3 mt-2">المحادثات</h3>
          
          <button className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-50 dark:hover:bg-card-dark transition-colors text-right group">
            <FiMessageSquare className="text-text-secondary-light dark:text-text-secondary-dark group-hover:text-text-primary-light dark:group-hover:text-text-primary-dark" size={18} />
            <span className="text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark group-hover:text-text-primary-light dark:group-hover:text-text-primary-dark truncate">خطة محتوى الأسبوع</span>
          </button>
          
          <button className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-50 dark:hover:bg-card-dark transition-colors text-right group">
            <FiMessageSquare className="text-text-secondary-light dark:text-text-secondary-dark group-hover:text-text-primary-light dark:group-hover:text-text-primary-dark" size={18} />
            <span className="text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark group-hover:text-text-primary-light dark:group-hover:text-text-primary-dark truncate">تحليل المنافسين</span>
          </button>
          
          <button className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-50 dark:hover:bg-card-dark transition-colors text-right group">
            <FiMessageSquare className="text-text-secondary-light dark:text-text-secondary-dark group-hover:text-text-primary-light dark:group-hover:text-text-primary-dark" size={18} />
            <span className="text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark group-hover:text-text-primary-light dark:group-hover:text-text-primary-dark truncate">استراتيجية إطلاق المنتج</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto pr-2"></div>

        <div className="mt-auto border-t border-border-light dark:border-border-dark pt-4 flex flex-col gap-1">
          <div className="relative">
            {showUserMenu && (
              <div className="absolute bottom-full left-0 right-0 mb-2 bg-card-light dark:bg-card-dark rounded-lg shadow-lg border border-border-light dark:border-border-dark overflow-hidden">
                {user?.is_admin && (
                  <button
                    onClick={() => {
                      setShowUserMenu(false)
                      navigate('/admin')
                    }}
                    className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-right border-b border-border-light dark:border-border-dark"
                  >
                    <MdDashboard className="text-purple-600 dark:text-purple-400" size={18} />
                    <span className="text-sm font-medium text-purple-600 dark:text-purple-400">لوحة التحكم الإدارية</span>
                  </button>
                )}
                <button
                  onClick={() => {
                    setShowUserMenu(false)
                    navigate('/profile')
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-right"
                >
                  <MdSettings className="text-text-secondary-light dark:text-text-secondary-dark" size={18} />
                  <span className="text-sm font-medium text-text-primary-light dark:text-text-primary-dark">الإعدادات</span>
                </button>
                <button
                  onClick={() => {
                    setShowUserMenu(false)
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-right"
                >
                  <MdPerson className="text-text-secondary-light dark:text-text-secondary-dark" size={18} />
                  <span className="text-sm font-medium text-text-primary-light dark:text-text-primary-dark">كاتب المحتوى</span>
                </button>
                <button
                  onClick={() => {
                    setShowUserMenu(false)
                    setDarkMode(!darkMode)
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-right"
                >
                  {darkMode ? (
                    <FiSun className="text-text-secondary-light dark:text-text-secondary-dark" size={18} />
                  ) : (
                    <FiMoon className="text-text-secondary-light dark:text-text-secondary-dark" size={18} />
                  )}
                  <span className="text-sm font-medium text-text-primary-light dark:text-text-primary-dark">المظهر</span>
                </button>
                <button
                  onClick={() => {
                    setShowUserMenu(false)
                    handleLogout()
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-right"
                >
                  <MdLogout className="text-text-secondary-light dark:text-text-secondary-dark group-hover:text-red-600 dark:group-hover:text-red-400" size={18} />
                  <span className="text-sm font-medium text-text-primary-light dark:text-text-primary-dark group-hover:text-red-600 dark:group-hover:text-red-400">تسجيل الخروج</span>
                </button>
              </div>
            )}
            
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-card-dark transition-colors cursor-pointer"
            >
              <div className="bg-primary rounded-full size-9 shrink-0 flex items-center justify-center text-white font-bold text-sm overflow-hidden">
                {user?.profile_picture ? (
                  <img src={user.profile_picture} alt="Profile" className="w-full h-full object-cover" />
                ) : (
                  user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'
                )}
              </div>
              <div className="flex flex-col min-w-0 flex-1">
                <span className="text-sm font-semibold text-text-primary-light dark:text-text-primary-dark truncate">
                  {user?.name || user?.email || 'المستخدم'}
                </span>
                <span className="text-xs text-text-secondary-light dark:text-text-secondary-dark truncate">Pro Plan</span>
              </div>
              <FiChevronUp 
                className={`text-text-secondary-light dark:text-text-secondary-dark transition-transform ${showUserMenu ? '' : 'rotate-180'}`} 
                size={16} 
              />
            </button>
          </div>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
