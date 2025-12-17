import React, { useState, useEffect, useRef } from 'react';
import styles from './ChatWidget.module.css'; // We'll create this CSS module

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState('');
    const [conversation, setConversation] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const chatWindowRef = useRef(null);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        const userMessage = { text: message, sender: 'user' };
        setConversation((prev) => [...prev, userMessage]);
        setMessage('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setConversation((prev) => [...prev, { text: data.response, sender: 'bot' }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setConversation((prev) => [...prev, { text: `Error: ${error.message}`, sender: 'bot' }]);
        } finally {
            setIsLoading(false);
        }
    };

    // Scroll to the bottom of the chat window on new message
    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [conversation]);

    return (
        <>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader} onClick={toggleChat}>
                        AI Assistant
                        <button className={styles.closeButton}>×</button>
                    </div>
                    <div className={styles.chatBody} ref={chatWindowRef}>
                        {conversation.length === 0 && !isLoading && (
                            <div className={styles.welcomeMessage}>
                                Hi there! How can I help you with the Docusaurus book?
                            </div>
                        )}
                        {conversation.map((msg, index) => (
                            <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                                {msg.text}
                            </div>
                        ))}
                        {isLoading && (
                            <div className={`${styles.message} ${styles.bot}`}>
                                <div className={styles.loadingDots}>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        )}
                    </div>
                    <form className={styles.chatInputForm} onSubmit={sendMessage}>
                        <input
                            type="text"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="Type your message..."
                            disabled={isLoading}
                        />
                        <button type="submit" disabled={isLoading} aria-label="Send message">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M3.478 2.405a.75.75 0 0 0-.926.94l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.405Z"/></svg>
                        </button>
                    </form>
                </div>
            )}
            {!isOpen && (
                <button className={styles.chatToggleButton} onClick={toggleChat} aria-label="Open chat">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
                        <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
                    </svg>
                </button>
            )}
        </>
    );
};

export default ChatWidget;

