import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { FiCamera, FiUser, FiMail, FiLock, FiArrowRight, FiCheck } from 'react-icons/fi'
import { MdClose } from 'react-icons/md'

const Profile = ({ user, setUser, darkMode }) => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ text: '', type: '' })
  
  const [profileData, setProfileData] = useState({
    name: user?.name || '',
    email: user?.email || ''
  })
  
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  })
  
  const [profilePicture, setProfilePicture] = useState(user?.profile_picture || '')
  const [previewImage, setPreviewImage] = useState(user?.profile_picture || '')

  useEffect(() => {
    if (user) {
      setProfileData({
        name: user.name || '',
        email: user.email || ''
      })
      setProfilePicture(user.profile_picture || '')
      setPreviewImage(user.profile_picture || '')
    }
  }, [user])

  const showMessage = (text, type) => {
    setMessage({ text, type })
    setTimeout(() => setMessage({ text: '', type: '' }), 5000)
  }

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        showMessage('حجم الصورة يجب أن يكون أقل من 5 ميجابايت', 'error')
        return
      }

      const reader = new FileReader()
      reader.onloadend = () => {
        setPreviewImage(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleUploadProfilePicture = async () => {
    if (!previewImage || previewImage === profilePicture) {
      showMessage('الرجاء اختيار صورة جديدة', 'error')
      return
    }

    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/auth/profile-picture`,
        { profile_picture: previewImage },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      const newProfilePicture = response.data.profile_picture
      const updatedUser = { ...user, profile_picture: newProfilePicture }
      
      // Update all states immediately
      setProfilePicture(newProfilePicture)
      setPreviewImage(newProfilePicture)
      setUser(updatedUser)
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      showMessage('تم تحديث الصورة الشخصية بنجاح', 'success')
    } catch (error) {
      showMessage(error.response?.data?.detail || 'فشل تحديث الصورة', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateProfile = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const token = localStorage.getItem('token')
      const response = await axios.put(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/auth/profile`,
        profileData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      const updatedUser = { ...user, ...response.data }
      setUser(updatedUser)
      localStorage.setItem('user', JSON.stringify(updatedUser))
      showMessage('تم تحديث البروفايل بنجاح', 'success')
    } catch (error) {
      showMessage(error.response?.data?.detail || 'فشل تحديث البروفايل', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleChangePassword = async (e) => {
    e.preventDefault()

    if (!passwordData.current_password) {
      showMessage('الرجاء إدخال كلمة المرور الحالية', 'error')
      return
    }

    if (!passwordData.new_password) {
      showMessage('الرجاء إدخال كلمة المرور الجديدة', 'error')
      return
    }

    if (passwordData.new_password !== passwordData.confirm_password) {
      showMessage('كلمة المرور الجديدة غير متطابقة', 'error')
      return
    }

    if (passwordData.new_password.length < 6) {
      showMessage('كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'error')
      return
    }

    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      
      const requestData = {
        current_password: passwordData.current_password,
        new_password: passwordData.new_password
      }
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/auth/change-password`,
        requestData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      })
      showMessage('تم تغيير كلمة المرور بنجاح', 'success')
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'فشل تغيير كلمة المرور'
      showMessage(errorMessage, 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-text-primary-light dark:text-text-primary-dark">
            إعدادات الحساب
          </h1>
          <button
            onClick={() => navigate('/chat')}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-card-light dark:bg-card-dark hover:bg-gray-100 dark:hover:bg-gray-700 text-text-primary-light dark:text-text-primary-dark transition-colors"
          >
            <span>العودة للمحادثة</span>
            <FiArrowRight />
          </button>
        </div>

        {message.text && (
          <div className={`mb-6 p-4 rounded-lg flex items-center justify-between ${
            message.type === 'success' 
              ? 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400' 
              : 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400'
          }`}>
            <div className="flex items-center gap-2">
              {message.type === 'success' ? <FiCheck size={20} /> : <MdClose size={20} />}
              <span>{message.text}</span>
            </div>
            <button onClick={() => setMessage({ text: '', type: '' })}>
              <MdClose size={20} />
            </button>
          </div>
        )}

        <div className="space-y-6">
          <div className="bg-card-light dark:bg-card-dark rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-text-primary-light dark:text-text-primary-dark mb-6">
              الصورة الشخصية
            </h2>
            
            <div className="flex flex-col md:flex-row items-center gap-6">
              <div className="relative">
                <div className="w-32 h-32 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                  {previewImage ? (
                    <img src={previewImage} alt="Profile" className="w-full h-full object-cover" />
                  ) : (
                    <FiUser size={48} className="text-gray-400" />
                  )}
                </div>
                <label className="absolute bottom-0 right-0 bg-primary hover:bg-secondary text-white p-2 rounded-full cursor-pointer shadow-lg transition-colors">
                  <FiCamera size={20} />
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="hidden"
                  />
                </label>
              </div>
              
              <div className="flex-1 text-center md:text-right">
                <p className="text-text-secondary-light dark:text-text-secondary-dark mb-4">
                  اختر صورة بصيغة JPG أو PNG. الحد الأقصى للحجم 5 ميجابايت.
                </p>
                <button
                  onClick={handleUploadProfilePicture}
                  disabled={loading || !previewImage || previewImage === profilePicture}
                  className="px-6 py-2 bg-primary hover:bg-secondary text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'جاري الرفع...' : 'حفظ الصورة'}
                </button>
              </div>
            </div>
          </div>

          <div className="bg-card-light dark:bg-card-dark rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-text-primary-light dark:text-text-primary-dark mb-6">
              المعلومات الشخصية
            </h2>
            
            <form onSubmit={handleUpdateProfile} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark mb-2">
                  الاسم
                </label>
                <div className="relative">
                  <FiUser className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-secondary-light dark:text-text-secondary-dark" />
                  <input
                    type="text"
                    value={profileData.name}
                    onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                    className="w-full pr-10 pl-4 py-3 bg-background-light dark:bg-background-dark border border-border-light dark:border-border-dark rounded-lg text-text-primary-light dark:text-text-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="أدخل اسمك"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark mb-2">
                  البريد الإلكتروني
                </label>
                <div className="relative">
                  <FiMail className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-secondary-light dark:text-text-secondary-dark" />
                  <input
                    type="email"
                    value={profileData.email}
                    onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                    className="w-full pr-10 pl-4 py-3 bg-background-light dark:bg-background-dark border border-border-light dark:border-border-dark rounded-lg text-text-primary-light dark:text-text-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="example@email.com"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-primary hover:bg-secondary text-white rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'جاري الحفظ...' : 'حفظ التغييرات'}
              </button>
            </form>
          </div>

          <div className="bg-card-light dark:bg-card-dark rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-text-primary-light dark:text-text-primary-dark mb-6">
              تغيير كلمة المرور
            </h2>
            
            <form onSubmit={handleChangePassword} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark mb-2">
                  كلمة المرور الحالية
                </label>
                <div className="relative">
                  <FiLock className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-secondary-light dark:text-text-secondary-dark" />
                  <input
                    type="password"
                    value={passwordData.current_password}
                    onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                    className="w-full pr-10 pl-4 py-3 bg-background-light dark:bg-background-dark border border-border-light dark:border-border-dark rounded-lg text-text-primary-light dark:text-text-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="أدخل كلمة المرور الحالية"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark mb-2">
                  كلمة المرور الجديدة
                </label>
                <div className="relative">
                  <FiLock className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-secondary-light dark:text-text-secondary-dark" />
                  <input
                    type="password"
                    value={passwordData.new_password}
                    onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                    className="w-full pr-10 pl-4 py-3 bg-background-light dark:bg-background-dark border border-border-light dark:border-border-dark rounded-lg text-text-primary-light dark:text-text-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="أدخل كلمة المرور الجديدة"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark mb-2">
                  تأكيد كلمة المرور الجديدة
                </label>
                <div className="relative">
                  <FiLock className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-secondary-light dark:text-text-secondary-dark" />
                  <input
                    type="password"
                    value={passwordData.confirm_password}
                    onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                    className="w-full pr-10 pl-4 py-3 bg-background-light dark:bg-background-dark border border-border-light dark:border-border-dark rounded-lg text-text-primary-light dark:text-text-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="أعد إدخال كلمة المرور الجديدة"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-primary hover:bg-secondary text-white rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'جاري التغيير...' : 'تغيير كلمة المرور'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile
