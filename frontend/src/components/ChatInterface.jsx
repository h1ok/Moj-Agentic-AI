import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { FiSend, FiPlus, FiShare2, FiMenu, FiSun, FiMoon } from 'react-icons/fi'
import { MdDashboard, MdSettings, MdPerson } from 'react-icons/md'
import { BsListUl, BsFileText } from 'react-icons/bs'
import Sidebar from './Sidebar'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import logoLight from '../assets/logos/logo-light.png'
import logoDark from '../assets/logos/logo-dark.png'

const ChatInterface = ({ darkMode, setDarkMode, user, onLogout }) => {
  const logo = darkMode ? logoLight : logoDark
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'مرحباً! أنا مساعدك الذكي في MOJ AI. يمكنني مساعدتك في إدارة وسائل التواصل الاجتماعي، التحليلات، والأتمتة. كيف يمكنني مساعدتك اليوم؟',
      timestamp: new Date().toISOString()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [ws, setWs] = useState(null)
  const [isConnected, setIsConnected] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  useEffect(() => {
    connectWebSocket()
    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [])

  const connectWebSocket = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.hostname}:8000/ws/chat`
    
    const websocket = new WebSocket(wsUrl)
    
    websocket.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
    }
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handleWebSocketMessage(data)
    }
    
    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    websocket.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
      setTimeout(connectWebSocket, 3000)
    }
    
    setWs(websocket)
  }

  const handleWebSocketMessage = (data) => {
    if (data.type === 'typing') {
      setIsTyping(data.status)
    } else if (data.type === 'assistant_message') {
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'assistant',
        content: data.message,
        timestamp: data.timestamp
      }])
    } else if (data.type === 'error') {
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'error',
        content: data.message,
        timestamp: data.timestamp
      }])
    }
  }

  const handleSendMessage = () => {
    if (!inputValue.trim() || !isConnected) return

    const newMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, newMessage])
    
    if (ws && ws.readyState === WebSocket.OPEN) {
      // إرسال الرسالة مع user_id و user_email و session_id
      const messageData = {
        message: inputValue,
        user_id: user?.id || null,
        user_email: user?.email || null,
        session_id: localStorage.getItem('session_id') || `session_${Date.now()}`
      }
      
      // حفظ session_id إذا لم يكن موجوداً
      if (!localStorage.getItem('session_id')) {
        localStorage.setItem('session_id', messageData.session_id)
      }
      
      ws.send(JSON.stringify(messageData))
    }

    setInputValue('')
  }

  const handleNewChat = () => {
    if (window.confirm('هل تريد بدء محادثة جديدة؟ سيتم حذف المحادثة الحالية.')) {
      setMessages([{
        id: Date.now(),
        type: 'assistant',
        content: 'مرحباً! أنا مساعدك الذكي في MOJ AI. يمكنني مساعدتك في إدارة وسائل التواصل الاجتماعي، التحليلات، والأتمتة. كيف يمكنني مساعدتك اليوم؟',
        timestamp: new Date().toISOString()
      }])
    }
  }

  return (
    <div className="flex h-screen w-full overflow-hidden">
      <Sidebar darkMode={darkMode} setDarkMode={setDarkMode} user={user} onLogout={onLogout} />
      
      {/* فاصل عمودي بين Sidebar والمحتوى */}
      <div className="w-px bg-border-light dark:bg-border-dark"></div>
      
      <main className="flex-1 flex flex-col h-full bg-background-light dark:bg-background-dark relative">
        <div className="flex flex-col">
          {/* Header */}
          <header className="flex items-center justify-between px-6 py-4 shrink-0 bg-card-light dark:bg-sidebar-dark z-10">
            <div className="flex items-center gap-3 text-text-primary-light dark:text-text-primary-dark">
            </div>
            <div className="flex items-center gap-2">
              <button 
                onClick={() => {}}
                className="flex items-center justify-center rounded-lg size-9 hover:bg-gray-50 dark:hover:bg-card-dark text-text-secondary-light dark:text-text-secondary-dark transition-colors"
                title="مشاركة المحادثة"
              >
                <FiShare2 size={18} />
              </button>
              <button 
                onClick={handleNewChat}
                className="flex items-center justify-center rounded-lg size-9 hover:bg-gray-50 dark:hover:bg-card-dark text-text-secondary-light dark:text-text-secondary-dark transition-colors"
                title="محادثة جديدة"
              >
                <FiPlus size={18} />
              </button>
              <button className="flex items-center justify-center rounded-lg size-9 hover:bg-gray-50 dark:hover:bg-card-dark text-text-secondary-light dark:text-text-secondary-dark transition-colors md:hidden">
                <FiMenu size={18} />
              </button>
            </div>
          </header>

          {/* فاصل أفقي تحت Header - يمتد بعرض كامل */}
          <div className="h-px bg-border-light dark:bg-border-dark w-full"></div>
        </div>

        {/* Messages */}
        <MessageList 
          messages={messages} 
          isTyping={isTyping}
          messagesEndRef={messagesEndRef}
        />

        {/* Input */}
        <MessageInput 
          inputValue={inputValue}
          setInputValue={setInputValue}
          handleSendMessage={handleSendMessage}
          isConnected={isConnected}
        />
      </main>
    </div>
  )
}

export default ChatInterface
