import Header from '../components/Header.jsx'
import { Link } from "react-router"

const TopPage = () => {
    return (
	<div className="h-60 bg-gray-100 h-lvh">
	    <Header>Let's Chat with AI</Header>
	    <Link to='/chatroom'>
		<div className="text-center font-serif text-gray-500 text-2xl p-10">
		    Enter the Chat Room
		</div>
	    </Link>
	</div>
    )
}

export default TopPage;
