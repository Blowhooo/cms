const variant = {
  default: 'block rounded-md w-full border border-gray-300 focus:border-green-500 focus:ring focus:ring-blue-100',
  error: 'border border-red-500 focus:border-red-500 focus:ring focus:ring-red-100',
  success: 'border border-green-500 focus:border-green-500 focus:ring focus:ring-green-100',
  disabled: 'bg-gray-100 text-gray-500 border border-gray-200 cursor-not-allowed',
};

export default function TextInput({
  type = "type",
  value,
  onChange,
  placeholder,
  variantType = 'default',
  disabled = false,
}) {
  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      disabled={disabled}
      className={`px-3 py-2 rounded-md outline-none transition duration-200 ${variant[disabled ? 'disabled' : variantType]}`}
    />
  );
}