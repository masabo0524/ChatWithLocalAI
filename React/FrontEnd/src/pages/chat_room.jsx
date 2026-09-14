import { useRef, useEffect, useState } from "react"

import Header from '../components/Header.jsx'
import Button from '../components/Button.jsx'
import TextArea from '../components/TextArea.jsx'
import ChatBox from '../components/ChatBox.jsx'
import ChatHistory from '../components/ChatHistory.jsx'

const WS_SERVER = "ws://localhost:8000/ws/chat/new/"


const ChatRoom = () => {
    
    const socketRef = useRef(null);
    const bottomRef = useRef(null);
    const keyRef = useRef(0);
    const textRef = useRef(null);

    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState("");
    const [isThinking, setIsThinking] = useState(false);
    
    const sendHandler = (event) => {
	socketRef.current.send(
	    JSON.stringify({message: message}));
	setMessage('');
	textRef.current.focus();
    };

    useEffect(() => {
	const socket = new WebSocket(WS_SERVER);
	socketRef.current = socket;
	console.log(socket);
	socket.onmessage = (event) => {
	    const receivedData = JSON.parse(event.data);
	    console.log(receivedData);
	    if(receivedData.isMessage){
		const dictMessage = {id: keyRef.current, fromMe: receivedData.message.fromMe, user: receivedData.message.sender, context: receivedData.message.context, time: receivedData.message.time };
		keyRef.current+=1;
		setMessages((prev) => [...prev, dictMessage]);
		setMessage('');
	    }else{
		if(receivedData.status === "thinking"){
		    setIsThinking(true);
		}else{
		    setIsThinking(false);
		};
	    };
	};

	return () => {
            if (
		socket.readyState === WebSocket.OPEN ||
		    socket.readyState === WebSocket.CONNECTING
            ) {
		socket.close();
            }
	};
	
    }, []);

    useEffect(() => {
	bottomRef.current?.scrollIntoView();
    }, [messages, isThinking])

      
    return (
	<>
	    <div className='text-center bg-gray-100 min-h-dvh'>
	    	<Header>Welcome to My Room!</Header>
		<ChatHistory messages={messages} isThinking={isThinking} ref={bottomRef}/>
		<ChatBox sendHandler={sendHandler} setMessage={setMessage} message={message} textRef={textRef} disabled={isThinking}/>
	    </div>
	</>
    )
}

export default ChatRoom;
