const variant = {
  default:
    'border border-green-500 text-green-500 cursor-pointer hover:bg-green-600 hover:text-white focus:ring focus:ring-green-200',
  error:
    'bg-red-500 text-white hover:bg-red-600 focus:ring focus:ring-red-200',
  success:
    'bg-blue-500 text-white hover:bg-blue-600 focus:ring focus:ring-blue-200',
  disabled:
    'bg-gray-300 text-gray-600 cursor-not-allowed border border-gray-200',
};

export default function Button({
  type = 'button',
  onClick,
  text = '버튼',
  variantType = 'default',
  disabled = false,
  className
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`
        ${className}
        px-4 py-2 rounded-md outline-none transition duration-200
        ${variant[disabled ? 'disabled' : variantType]}
      `}
    >
      {text}
    </button>
  );
}
