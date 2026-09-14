import ReactMarkdown from "react-markdown"

const ChatBubble = ({ children, fromMe = true, user = "sample", time = "10:10", ref }) => {

    if(fromMe){
	return(
	    <>
		<div className="my-5 w-1/2 translate-x-2/3 flex flex-col"
		     ref={ref}>
		    <div className="flex flex-row-reverse font-serif">
			<p className="">
			{time}
			</p>
		    </div>

		    <div className="font-serif text-white py-5 px-5 bg-taupe-400 shadow rounded-xl">
			<ReactMarkdown>
			    {children}
			</ReactMarkdown>
		    </div>
		</div>

	    </>
	)
    }else{
	return (
	    <>
		<div className="translate-x-1/5 flex flex-row items-center w-1/2"
		     ref={ref}>
		    <div className="grid place-items-center bg-mauve-500 text-white size-10 shrink-0 rounded-full m-5">
			<p className="">{user[0]}</p>
		    </div>
		    <div className="my-5 w-full flex flex-col">
			<div className="flex flex-row font-serif">
			    <p className="">
				{time}
			    </p>
			</div>

			<div className="font-serif text-white py-5 px-5 bg-slate-400 shadow rounded-xl">
			    <ReactMarkdown>
				{children}
			    </ReactMarkdown>
			</div>
		    </div>
		</div>

	    </>
	)
    }
}

export default ChatBubble
