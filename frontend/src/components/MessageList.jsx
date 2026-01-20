import Message from './Message'
import TypingIndicator from './TypingIndicator'

const MessageList = ({ messages, isTyping, messagesEndRef }) => {
  return (
    <div className="flex-1 overflow-y-auto w-full p-4 md:p-6 pb-2">
      <div className="flex flex-col w-full max-w-[900px] mx-auto">
        <div className="bg-card-light dark:bg-card-dark rounded-2xl shadow-sm border border-border-light dark:border-border-dark p-6 md:p-8 min-h-[200px]">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <div className="bg-primary rounded-full size-16 flex items-center justify-center text-white font-bold shadow-md mb-6">
                <span className="text-3xl">🤖</span>
              </div>
              <h3 className="text-2xl font-bold text-text-primary-light dark:text-text-primary-dark mb-3">مرحباً بك في MOJ AI</h3>
              <p className="text-text-secondary-light dark:text-text-secondary-dark max-w-md">
                أنا مساعدك الذكي لإدارة وسائل التواصل الاجتماعي. كيف يمكنني مساعدتك اليوم؟
              </p>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <Message key={message.id} message={message} />
              ))}
              {isTyping && <TypingIndicator />}
            </>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  )
}

export default MessageList
