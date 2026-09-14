import { useRef } from 'react'

import TextArea from './TextArea.jsx'
import Button from './Button.jsx'


const ChatBox = ({ sendHandler, setMessage, message, textRef, disabled }) => {
    
    return (
	<div className="left-1/2 -translate-x-1/2  w-full max-h-35 h-1/5 fixed bottom-0 flex justify-center bg-gray-100/50 backdrop-blur-md z-50">
	    <div className=" flex items-center gap-4 p-5 w-2/3">
		<TextArea onChange={(e) => setMessage(e.target.value)}
			  value={message}
			  ref={textRef}
			  placeholder="Write something..."
			  disabled={disabled}
			  className="w-2/3 min-h-15 max-h-30 h-full font-serif flex-1 p-2 rounded-lg border border-taupe-300 hover:border-taupe-600"/>

		<Button onClick={sendHandler}
			disabled={disabled}
			className="font-serif px-6 py-3 text-white bg-taupe-500 rounded-lg shadow hover:bg-taupe-700">
                    Send
		</Button>
            </div>
	</div>

    );
}

export default ChatBox;
