import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { FiSend, FiPlus, FiShare2, FiMenu, FiSun, FiMoon } from 'react-icons/fi'
import { MdDashboard, MdSettings, MdPerson } from 'react-icons/md'
import { BsListUl, BsFileText } from 'react-icons/bs'
import Sidebar from './Sidebar'
import MessageList from './MessageList'
import MessageInput from './MessageInput'

const ChatInterface = ({ darkMode, setDarkMode, user, onLogout }) => {
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
      
      <main className="flex-1 flex flex-col h-full bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-900 dark:via-background-dark dark:to-gray-900 relative">
        {/* Header */}
        <header className="flex items-center justify-between border-b-2 border-gray-200 dark:border-gray-800 px-6 py-4 shrink-0 bg-white/90 dark:bg-background-dark/90 backdrop-blur-lg shadow-sm z-10">
          <div className="flex items-center gap-3 text-gray-900 dark:text-white">
            <h2 className="text-lg font-bold">MOJ AI</h2>
          </div>
          <div className="flex items-center gap-2">
            <button 
              onClick={() => {}}
              className="flex items-center justify-center rounded-lg size-9 hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300 transition-colors"
              title="مشاركة المحادثة"
            >
              <FiShare2 size={20} />
            </button>
            <button 
              onClick={handleNewChat}
              className="flex items-center justify-center rounded-lg size-9 hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300 transition-colors"
              title="محادثة جديدة"
            >
              <FiPlus size={20} />
            </button>
            <button className="flex items-center justify-center rounded-lg size-9 hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300 transition-colors md:hidden">
              <FiMenu size={20} />
            </button>
          </div>
        </header>

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
