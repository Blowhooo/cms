import styles from './Input.module.scss';

const Input = ({
  type = 'text',
  placeholder,
  id,
  name,
  required = false,
  autoComplete,
  variant, // primary, error, success 등
  size, // small, medium, large 등
  disabled = false,
  ...props
}) => {
  const className = [
    styles.frmInput,
    variant && styles[`frmInput--${variant}`],
    size && styles[`frmInput--${size}`],
    disabled && styles['frmInput--disabled']
  ].filter(Boolean).join(' ');

  return (
    <input
      type={type}
      id={id}
      name={name}
      className={className}
      placeholder={placeholder}
      required={required}
      aria-required={required}
      autoComplete={autoComplete}
      disabled={disabled}
      {...props}
    />
  );
};

export default Input;