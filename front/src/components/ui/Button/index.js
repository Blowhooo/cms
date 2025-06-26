import styles from './Button.module.scss';

const Button = ({
   children,
  as = 'button', // 렌더링할 요소 타입 또는 컴포넌트
  type = 'button',
  variant, // primary, secondary, danger, success, warning, ghost, outline
  size, // small, medium, large, xl
  disabled = false,
  href, // a 태그용
  to, // Link 컴포넌트용
  value, // input 태그용
  ...props
}) => {
  const className = [
    styles.btn,
    variant && styles[`btn--${variant}`],
    size && styles[`btn--${size}`],
    disabled && styles['btn--disabled']
  ].filter(Boolean).join(' ');
  
  // Link 컴포넌트로 렌더링 (React Router Link, Next.js Link 등)
  if (as !== 'button' && as !== 'a' && as !== 'input') {
    const Component = as;
    const linkProps = {};
    
    // Next.js Link는 href, React Router Link는 to 사용
    if (href) {
      linkProps.href = href;
    } else if (to) {
      linkProps.to = to;
    }
    
    return (
      <Component
        {...linkProps}
        className={className}
        {...(disabled && { 'aria-disabled': true, tabIndex: -1 })}
        {...props}
      >
        {children}
      </Component>
    );
  }
  
  // a 태그로 렌더링
  if (as === 'a' || (href && !as) || (to && !as)) {
    return (
      <a
        href={href || to}
        className={className}
        {...(disabled && { 'aria-disabled': true, tabIndex: -1 })}
        {...props}
      >
        {children}
      </a>
    );
  }
  
  // input 태그로 렌더링
  if (as === 'input') {
    return (
      <input
        type={type}
        value={value || children}
        className={className}
        disabled={disabled}
        {...props}
      />
    );
  }
  
  // 기본 button 태그로 렌더링
  return (
    <button
      type={type}
      className={className}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;