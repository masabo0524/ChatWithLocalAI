const TextArea = ({ placeholder='placeholder', className, value, onChange, ref, disabled }) => {
    return (
	<textarea value={value}
		  onChange={onChange}
		  ref={ref}
		  cols="30"
		  disabled={disabled}
		  id="chat-message"
		  name="chat-message"
		  rows="3"
		  className={className}
		  placeholder={placeholder}>
	</textarea>
    );
}

export default TextArea;
