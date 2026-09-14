const Button = ({ children='Button', className, onClick, disabled }) => {

    if(disabled){
	return (
	    <div className="flex justify-center" aria-label="読み込み中">
		<div className="animate-spin h-8 w-8 bg-blue-300 rounded-xl"></div>
	    </div>
	);
    }else{
	return (
	    <button onClick={onClick}
		    disabled={disabled}
		    className={className}>
		{children}
	    </button>
	);
    };


}

export default Button;
