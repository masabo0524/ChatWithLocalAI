import ChatBubble from './ChatBubble.jsx'


const ChatHistory = ({ messages, isThinking=false, ref }) => {

    console.log("ChatHistory isThinking: ", isThinking);

    const chatBubbles = messages.map((message, index) => (
	<ChatBubble key={message.id} fromMe={message.fromMe} user={message.user} time={message.time} ref={ref}>
	    {message.context}
	</ChatBubble>
    ));

    return(
	<>
	    <div className="mx-5 my-5 pb-32">
		{chatBubbles}
		{isThinking ? <div className="flex justify-center" aria-label="読み込み中"><div className="animate-spin h-8 w-8 bg-blue-300 rounded-xl"></div></div> : ""}
	    </div>

	</>
    );
}

export default ChatHistory;
