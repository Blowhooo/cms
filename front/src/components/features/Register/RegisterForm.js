"use client";

import { useState } from 'react'
import Link from 'next/link';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';



const RegisterForm = () => {
  // 아이디 관련
  const [username, setUsername] = useState('');
  const [usernameChk, setUsernameChk] = useState('');
  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };
  const handleUsernameBlur = (e) => {
    const value = e.target.value.trim();
    const isValid = /^[a-zA-Z0-9]+$/.test(value) && value.length >= 8 && value.length <= 16;
    setUsernameChk(value.length === 0 ? '' : isValid ? 'correct' : 'wrong');
  };

  // 닉네임 관련
  const [usernick, setUsernick] = useState('');
  const [usernickChk, setUsernickChk] = useState('');
  const handleUsernickChange = (e) => {
    setUsernick(e.target.value);
  };
  const handleUsernickBlur = (e) => {
    const value = e.target.value.trim();
    const isValid = /^[가-힣a-zA-Z0-9]+$/.test(value) && value.length >= 2 && value.length <= 10;
    setUsernickChk(value.length === 0 ? '' : isValid ? 'correct' : 'wrong');
  };

  // 비밀번호 관련
  const [userPw, setUserPw] = useState('');
  const [userPwChk, setUserPwChk] = useState('');
  const handleUserPwChange = (e) => {
    setUserPw(e.target.value);
  };
  const handleUserPwBlur = (e) => {
    const value = e.target.value.trim();
    const isValid = value.length >= 8 && value.length <= 16;
    setUserPwChk(value.length === 0 ? '' : isValid ? 'correct' : 'wrong');
  };

  // 비밀번호 확인
  const [userPwConfirm, setUserPwConfirm] = useState('');
  const [userPwConfirmChk, setUserPwConfirmChk] = useState('');
  const handleUserPwConfirmChange = (e) => {
    setUserPwConfirm(e.target.value);
  };
  const handleUserPwConfirmBlur = (e) => {
    const value = e.target.value.trim();
    setUserPwConfirmChk(value.length === 0 ? '' : value === userPw ? 'correct' : 'wrong');
  };

  // 회원가입 버튼
  const [formChk, setFormChk] = useState('');

  const handleSubmit = (e) => {
    handleUsernameBlur({ target: { value: username } });
    handleUsernickBlur({ target: { value: usernick } });
    handleUserPwBlur({ target: { value: userPw } });
    handleUserPwConfirmBlur({ target: { value: userPwConfirm } });

     if (
      usernameChk !== 'correct' ||
      usernickChk !== 'correct' ||
      userPwChk !== 'correct' ||
      userPwConfirmChk !== 'correct'
    ) {
      alert('입력하신 정보를 다시 확인해주세요.');
      return;
    }
  }

  const formSet = [
    {
      tag: 'label',
      id: 'username',
      name: 'username',
      type: 'text',
      placeholder: '아이디를 입력하세요',
      labelText: '아이디',
      alert: '아이디는 8자 이상 16자 이하로 입력해주세요.',
      value: username,
      variant: usernameChk,
      onChange: handleUsernameChange,
      onBlur: handleUsernameBlur
    },
    {
      tag: 'label',
      id: 'nickname',
      name: 'nickname',
      type: 'text',
      placeholder: '닉네임을 입력하세요',
      labelText: '닉네임',
      alert: [
        '2자 이상 10자 이하, 한글·영문·숫자만 사용 가능합니다.',
        '한글, 영문, 숫자만 사용 가능하며 특수문자나 한자는 사용할 수 없습니다.'
      ],
      value: usernick,
      variant: usernickChk,
      onChange: handleUsernickChange,
      onBlur: handleUsernickBlur
    },
    {
      tag: 'label',
      id: 'password',
      name: 'password',
      type: 'password',
      placeholder: '비밀번호를 입력하세요',
      labelText: '비밀번호',
      alert: [
        '8자 이상 16자 이하의 영문, 숫자를 포함해야 합니다.',
        '특수문자 사용을 권장하며, 공백은 사용할 수 없습니다.'
      ],
      value: userPw,
      variant: userPwChk,
      onChange: handleUserPwChange,
      onBlur: handleUserPwBlur
    },
    {
      tag: 'label',
      id: 'password-chk',
      name: 'password-chk',
      type: 'password',
      placeholder: '비밀번호를 다시 한번 입력하세요.',
      labelText: '비밀번호 확인',
      value: userPwConfirm,
      variant: userPwConfirmChk,
      onChange: handleUserPwConfirmChange,
      onBlur: handleUserPwConfirmBlur,
      alert: true
    }
  ];

  const btnSet = [
    {
      type: 'submit',
      key: 'register',
      text: '회원가입',
      variant: 'primary'
    },
    {
      as: Link,
      href: '/',
      key: 'back',
      text: '뒤로가기',
      variant: 'secondary'
    }
  ];

  return (
    <form 
      className="login-form" 
      noValidate 
      aria-describedby="register-desc"
       onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <fieldset className="login-form__fieldset">
        <legend className="blind">회원가입 정보 입력</legend>
        <p id="register-desc" className="blind">회원가입을 위한 정보를 입력해주세요.</p>

        {formSet.map((item) => {
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
                maxLength={20}
                {...(item.variant !== undefined && { variant: item.variant })}
                {...(item.value !== undefined && { value: item.value })}
                {...(item.onChange !== undefined && { onChange: item.onChange })}
                {...(item.onBlur !== undefined && { onBlur: item.onBlur })}
              />
              {item.alert && (
                <div className="login-form__alert" role="alert">
                  {item.id === 'password-chk' ? (
                    userPwConfirmChk === 'wrong' ? (
                      <p className="login-form__msg">비밀번호가 일치하지 않습니다.</p>
                    ) : userPwConfirmChk === 'correct' ? (
                      <p className="login-form__msg login-form__msg--correct">비밀번호가 일치합니다.</p>
                    ) : null
                  ) : Array.isArray(item.alert) ? (
                    item.alert.map((msg, i) => (
                      <p
                        key={msg}
                        className={`login-form__msg ${
                          (item.id === 'username' && usernameChk === 'correct') ||
                          (item.id === 'nickname' && usernickChk === 'correct') ||
                          (item.id === 'password' && userPwChk === 'correct')
                            ? 'login-form__msg--correct'
                            : ''
                        }`}
                      >
                        {msg}
                      </p>
                    ))
                  ) : (
                    <p
                      className={`login-form__msg ${
                        (item.id === 'username' && usernameChk === 'correct') ||
                        (item.id === 'nickname' && usernickChk === 'correct') ||
                        (item.id === 'password' && userPwChk === 'correct')
                          ? 'login-form__msg--correct'
                          : ''
                      }`}
                    >
                      {item.alert}
                    </p>
                  )}
                </div>
              )}
            </WrapperTag>
          );
        })}
      </fieldset>

      <div className="login-form__ctrl">
        {btnSet.map((btn) => (
          <Button
            type={btn.type}
            key={btn.key}
            as={btn.as}
            href={btn.href}
            variant={btn.variant}
          >
            {btn.text}
          </Button>
        ))}
      </div>
    </form>
  );
};

export default RegisterForm;
