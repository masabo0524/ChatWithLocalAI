const Header = ( { children='Welcome' }) => {
    return (
	<header className="text-center font-serif sticky top-0 left-0 w-full py-10 px-10 bg-gray-100/50 backdrop-blur-sm z-50">
	    <h1 className='text-zinc-500 text-2xl'>{children}</h1>
	</header>
    )
}

export default Header;
