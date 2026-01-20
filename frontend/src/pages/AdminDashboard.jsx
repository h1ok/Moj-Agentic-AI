import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { FiUsers, FiActivity, FiUserCheck, FiUserX, FiShield, FiTrash2, FiEdit, FiArrowRight } from 'react-icons/fi'
import { MdAdminPanelSettings } from 'react-icons/md'

const AdminDashboard = ({ user, darkMode }) => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState(null)
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [showEditModal, setShowEditModal] = useState(false)
  const [message, setMessage] = useState({ text: '', type: '' })

  useEffect(() => {
    if (!user?.is_admin) {
      navigate('/chat')
      return
    }
    fetchDashboardData()
  }, [user, navigate])

  const showMessage = (text, type) => {
    setMessage({ text, type })
    setTimeout(() => setMessage({ text: '', type: '' }), 5000)
  }

  const fetchDashboardData = async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }

      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const [statsRes, usersRes] = await Promise.all([
        axios.get(`${API_URL}/api/admin/stats`, { headers }),
        axios.get(`${API_URL}/api/admin/users`, { headers })
      ])

      setStats(statsRes.data)
      setUsers(usersRes.data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      showMessage('فشل تحميل البيانات', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleToggleActive = async (userId, currentStatus) => {
    try {
      const token = localStorage.getItem('token')
      await axios.put(
        `http://localhost:8000/api/admin/users/${userId}`,
        { is_active: !currentStatus },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )
      showMessage('تم تحديث حالة المستخدم بنجاح', 'success')
      fetchDashboardData()
    } catch (error) {
      showMessage(error.response?.data?.detail || 'فشل تحديث المستخدم', 'error')
    }
  }

  const handleToggleAdmin = async (userId, currentStatus) => {
    try {
      const token = localStorage.getItem('token')
      await axios.put(
        `http://localhost:8000/api/admin/users/${userId}`,
        { is_admin: !currentStatus },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )
      showMessage('تم تحديث صلاحيات المستخدم بنجاح', 'success')
      fetchDashboardData()
    } catch (error) {
      showMessage(error.response?.data?.detail || 'فشل تحديث الصلاحيات', 'error')
    }
  }

  const handleDeleteUser = async (userId, userEmail) => {
    if (!window.confirm(`هل أنت متأكد من حذف المستخدم ${userEmail}؟`)) {
      return
    }

    try {
      const token = localStorage.getItem('token')
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      await axios.delete(
        `${API_URL}/api/admin/users/${userId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      )
      showMessage('تم حذف المستخدم بنجاح', 'success')
      fetchDashboardData()
    } catch (error) {
      showMessage(error.response?.data?.detail || 'فشل حذف المستخدم', 'error')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background-light dark:bg-background-dark flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-text-secondary-light dark:text-text-secondary-dark">جاري التحميل...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <MdAdminPanelSettings className="text-primary" size={40} />
            <div>
              <h1 className="text-3xl font-bold text-text-primary-light dark:text-text-primary-dark">
                لوحة التحكم الإدارية
              </h1>
              <p className="text-text-secondary-light dark:text-text-secondary-dark">
                إدارة المستخدمين والنظام
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/chat')}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-card-light dark:bg-card-dark hover:bg-gray-100 dark:hover:bg-gray-700 text-text-primary-light dark:text-text-primary-dark transition-colors"
          >
            <span>العودة للمحادثة</span>
            <FiArrowRight />
          </button>
        </div>

        {/* Message */}
        {message.text && (
          <div className={`mb-6 p-4 rounded-lg ${
            message.type === 'success' 
              ? 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400' 
              : 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400'
          }`}>
            {message.text}
          </div>
        )}

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div className="bg-card-light dark:bg-card-dark rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-text-secondary-light dark:text-text-secondary-dark text-sm mb-1">
                    إجمالي المستخدمين
                  </p>
                  <p className="text-3xl font-bold text-text-primary-light dark:text-text-primary-dark">
                    {stats.total_users}
                  </p>
                </div>
                <div className="bg-primary/10 p-3 rounded-lg">
                  <FiUsers className="text-primary" size={24} />
                </div>
              </div>
            </div>

            <div className="bg-card-light dark:bg-card-dark rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-text-secondary-light dark:text-text-secondary-dark text-sm mb-1">
                    المستخدمين النشطين
                  </p>
                  <p className="text-3xl font-bold text-green-600 dark:text-green-400">
                    {stats.active_users}
                  </p>
                </div>
                <div className="bg-green-100 dark:bg-green-900/20 p-3 rounded-lg">
                  <FiUserCheck className="text-green-600 dark:text-green-400" size={24} />
                </div>
              </div>
            </div>

            <div className="bg-card-light dark:bg-card-dark rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-text-secondary-light dark:text-text-secondary-dark text-sm mb-1">
                    المسؤولين
                  </p>
                  <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                    {stats.admin_users}
                  </p>
                </div>
                <div className="bg-purple-100 dark:bg-purple-900/20 p-3 rounded-lg">
                  <FiShield className="text-purple-600 dark:text-purple-400" size={24} />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Users Table */}
        <div className="bg-card-light dark:bg-card-dark rounded-xl shadow-sm overflow-hidden">
          <div className="p-6 border-b border-border-light dark:border-border-dark">
            <h2 className="text-xl font-semibold text-text-primary-light dark:text-text-primary-dark">
              إدارة المستخدمين
            </h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wider">
                    المستخدم
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wider">
                    البريد الإلكتروني
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wider">
                    الحالة
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wider">
                    الصلاحيات
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wider">
                    تاريخ الإنشاء
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wider">
                    الإجراءات
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-light dark:divide-border-dark">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-bold overflow-hidden">
                          {u.profile_picture ? (
                            <img src={u.profile_picture} alt={u.name} className="w-full h-full object-cover" />
                          ) : (
                            u.name?.charAt(0) || u.email?.charAt(0) || 'U'
                          )}
                        </div>
                        <span className="text-text-primary-light dark:text-text-primary-dark font-medium">
                          {u.name || 'بدون اسم'}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-text-secondary-light dark:text-text-secondary-dark">
                      {u.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => handleToggleActive(u.id, u.is_active)}
                        disabled={u.id === user.id}
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          u.is_active
                            ? 'bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400'
                            : 'bg-red-100 dark:bg-red-900/20 text-red-600 dark:text-red-400'
                        } ${u.id === user.id ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:opacity-80'}`}
                      >
                        {u.is_active ? 'نشط' : 'معطل'}
                      </button>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => handleToggleAdmin(u.id, u.is_admin)}
                        disabled={u.id === user.id}
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          u.is_admin
                            ? 'bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                        } ${u.id === user.id ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:opacity-80'}`}
                      >
                        {u.is_admin ? 'مسؤول' : 'مستخدم'}
                      </button>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-text-secondary-light dark:text-text-secondary-dark text-sm">
                      {new Date(u.created_at).toLocaleDateString('ar-SA')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => handleDeleteUser(u.id, u.email)}
                        disabled={u.id === user.id}
                        className={`text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 ${
                          u.id === user.id ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                        title="حذف المستخدم"
                      >
                        <FiTrash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
