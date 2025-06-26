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
    labelText : "아이디",
  },
  {
    tag: "label",
    id: "password",
    name: "password",
    type: "password",
    placeholder: "비밀번호를 입력하세요",
    labelText : "비밀번호"
  },
]

const Form = () => {
  return (
    <form
      className="login-form"
      noValidate
      aria-describedby="login-desc"
    >
      <fieldset className="login-form__fieldset">
        <legend className="blind">로그인 정보 입력</legend>
        <p id="login-desc" className="blind">
          아이디와 비밀번호를 입력하여 로그인하세요.
        </p>

        {formSet.map((item,idx) => {
          const WrapperTag = item.tag;
          return (
            <WrapperTag
              key={item.id}
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
          )
        })}

        <Button 
          as={Link}
          href="/home"
          aria-describedby="login-button-desc"
        >
          로그인
        </Button>
        
        <p id="login-button-desc" className="blind">
          로그인 버튼을 클릭하면 계정에 로그인됩니다.
        </p>
      </fieldset>

      <div className="login-form__page">
        <Link
          href="/forgot-password"
          className="login-form__link"
          aria-label="비밀번호 찾기 페이지로 이동"
        >
          비밀번호를 잊으셨나요?
        </Link>
        <Link
          href="/register"
          className="login-form__link"
          aria-label="회원가입 페이지로 이동"
        >
          회원가입
        </Link>
      </div>
    </form>
  );
};

export default Form;
