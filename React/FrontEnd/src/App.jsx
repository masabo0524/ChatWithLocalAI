import { Route, Routes } from 'react-router'

import ChatRoom from './pages/chat_room.jsx'
import TopPage from './pages/top_page.jsx'

const App = () => {
    return(
	<div className="gb-gray-100/50">
	    <Routes>
		<Route path="/chatroom" element={<ChatRoom />} />
		<Route path="/" element={<TopPage />} />
	    </Routes>
	</div>
    )
}

export default App;
