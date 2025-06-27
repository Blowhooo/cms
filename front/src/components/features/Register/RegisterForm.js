import Link from 'next/link';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

const formSet = [
  { 
    tag: "label",
    id: "username",
    name: "username",
    type: "text",
    placeholder: "아이디를 입력하세요",
    labelText: "아이디",
    alert: "아이디는 8자 이상 16자 이하로 입력해주세요."
  },
  {    
    tag: "label",
    id: "nickname", 
    name: "nickname",
    type: "text",
    placeholder: "닉네임을 입력하세요",
    labelText: "닉네임",
    alert: [
      "2자 이상 10자 이하, 한글·영문·숫자만 사용 가능합니다.",
      "한글, 영문, 숫자만 사용 가능하며 특수문자나 한자는 사용할 수 없습니다."
    ]
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
    href: "/register/success",
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

const RegisterForm = () => {
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
              key={item.id} 
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
              {item.alert && (
                <div className="login-form__alert" role="alert">
                  {Array.isArray(item.alert) ? (
                    item.alert.map(msg => <p key={msg} className="login-form__msg">{msg}</p>)
                  ) : (
                    <p className="login-form__msg">{item.alert}</p>
                  )}
                </div>
              )}
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

export default RegisterForm;