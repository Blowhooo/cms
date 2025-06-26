import Link from 'next/link';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import '@/components/common/styles/login.scss';

const formSet = [
  { 
    tag: "label",
    id: "username",
    name: "username",
    type: "text",
    placeholder: "아이디를 입력하세요",
    labelText: "아이디"
  },
  {    
    tag: "label",
    id: "nickname", 
    name: "nickname",
    type: "text",
    placeholder: "닉네임을 입력하세요",
    labelText: "닉네임"
  },
  {    
    tag: "label",
    id: "password",
    name: "password", 
    type: "password",
    placeholder: "비밀번호를 입력하세요",
    labelText: "비밀번호"
  },
  {    
    tag: "label",
    id: "password-chk",
    name: "password-chk", 
    type: "password",
    placeholder: "비밀번호를 다시 한번 입력하세요.",
    labelText: "비밀번호 확인"
  }
];

const btnSet = [
  {
    as: Link,
    href: "/success",
    key: "register",
    text: "회원가입",
    variant: "primary"
  },
  {
    as: Link,
    href: "/",
    key: "back",
    text: "뒤로가기",
    variant: "secondary"
  }
];

const Form = () => {
  return (
    <form 
      className="login-form"
      noValidate
      aria-describedby="register-desc"
    >
      <fieldset className="login-form__fieldset">
        <legend className="blind">회원가입 정보 입력</legend>
        <p id="register-desc" className="blind">
          회원가입을 위한 정보를 입력해주세요.
        </p>
        {formSet.map((item, idx) => {
          // 동적 태그 컴포넌트
          const WrapperTag = item.tag;
          
          return (
            <WrapperTag 
              key={idx} 
              className="login-form__field"
              {...(item.tag === 'label' && { htmlFor: item.id })}
            >
              <span className="blind">{item.labelText}</span>            
              <Input 
                id={item.id}
                name={item.name}
                type={item.type}
                placeholder={item.placeholder}
                required
              />
            </WrapperTag>
          );
        })}
      </fieldset>
      <div className="login-form__ctrl">
        {btnSet.map(item => (
          <Button 
            key={item.key}
            as={item.as} 
            href={item.href}
            variant={item.variant}
          >
            {item.text}
          </Button>
        ))}
      </div>
    </form>
  );
};

export default Form;