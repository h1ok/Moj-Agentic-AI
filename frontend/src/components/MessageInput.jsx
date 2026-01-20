import { FiSend, FiPlus } from 'react-icons/fi'

const MessageInput = ({ inputValue, setInputValue, handleSendMessage, isConnected }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="w-full bg-background-light dark:bg-background-dark pt-3 pb-4 px-4 md:px-8">
      <div className="w-full max-w-[840px] mx-auto">
        <div className="relative flex items-end w-full p-3 bg-card-light dark:bg-card-dark border border-border-light dark:border-border-dark rounded-2xl shadow-sm hover:shadow-md focus-within:border-primary dark:focus-within:border-primary transition-all duration-200">
          <button className="p-2 text-text-secondary-light dark:text-text-secondary-dark hover:text-primary dark:hover:text-primary transition-all duration-200 rounded-lg hover:bg-gray-50 dark:hover:bg-sidebar-dark shrink-0 mb-0.5">
            <FiPlus size={20} />
          </button>
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            className="w-full max-h-[200px] py-3 px-3 bg-transparent border-0 focus:ring-0 text-text-primary-light dark:text-text-primary-dark placeholder-text-secondary-light dark:placeholder-text-secondary-dark resize-none leading-relaxed outline-none text-sm"
            placeholder="اكتب رسالتك بالتفصيل..."
            rows="1"
            style={{ minHeight: '48px' }}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || !isConnected}
            className={`p-2.5 mb-0.5 rounded-lg transition-all duration-200 shrink-0 ${
              inputValue.trim() && isConnected
                ? 'bg-primary hover:bg-secondary text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed'
            }`}
          >
            <FiSend size={18} />
          </button>
        </div>
        <div className="text-center mt-2">
          <p className="text-xs text-text-secondary-light dark:text-text-secondary-dark">
            MOJ AI يمكن أن يخطئ. تحقق من المعلومات المهمة.
          </p>
        </div>
      </div>
    </div>
  )
}

export default MessageInput
