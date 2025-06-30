"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

const RegisterForm = () => {
  const router = useRouter();

  const [form, setForm] = useState({
    username: '',
    nickname: '',
    password: '',
    passwordChk: ''
  });

  const [errors, setErrors] = useState({
    username: '',
    nickname: '',
    password: '',
    passwordChk: ''
  });

  const [touched, setTouched] = useState({
    username: false,
    nickname: false,
    password: false,
    passwordChk: false
  });

  const validateField = (name, value, allValues = form) => {
    switch (name) {
      case 'username':
        return /^[a-zA-Z0-9]{8,16}$/.test(value)
          ? ''
          : '아이디는 영문 8자 이상 16자 이하로 입력해주세요.';
      case 'nickname':
        return /^[가-힣a-zA-Z0-9]{2,10}$/.test(value)
          ? ''
          : '닉네임은 2~10자, 한글/영문/숫자만 사용 가능합니다.';
      case 'password':
        return /^.{8,16}$/.test(value)
          ? ''
          : '비밀번호는 8자 이상 16자 이하로 입력해주세요.';
      case 'passwordChk':
        return value === allValues.password
          ? ''
          : '비밀번호가 일치하지 않습니다.';
      default:
        return '';
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;

    setTouched((prev) => ({ ...prev, [name]: true }));

    setErrors((prev) => ({
      ...prev,
      [name]: validateField(name, value)
    }));
  };

  const validateAll = () => {
    const newErrors = {
      username: validateField('username', form.username),
      nickname: validateField('nickname', form.nickname),
      password: validateField('password', form.password),
      passwordChk: validateField('passwordChk', form.passwordChk, form)
    };

    setErrors(newErrors);
    setTouched({
      username: true,
      nickname: true,
      password: true,
      passwordChk: true
    });

    return Object.values(newErrors).every((msg) => msg === '');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateAll()) {
      router.push('/register/success');
    }
  };

  return (
    <form className="login-form" noValidate onSubmit={handleSubmit}>
      <fieldset className="login-form__fieldset">
        <legend className="blind">회원가입 정보 입력</legend>

        {['username', 'nickname', 'password', 'passwordChk'].map((field) => {
          const labels = {
            username: '아이디',
            nickname: '닉네임',
            password: '비밀번호',
            passwordChk: '비밀번호 확인'
          };

          const placeholders = {
            username: '아이디를 입력하세요',
            nickname: '닉네임을 입력하세요',
            password: '비밀번호를 입력하세요',
            passwordChk: '비밀번호를 다시 입력하세요'
          };

          const types = {
            username: 'text',
            nickname: 'text',
            password: 'password',
            passwordChk: 'password'
          };

          return (
            <label key={field} htmlFor={field} className="login-form__field">
              <span className="blind">{labels[field]}</span>
              <Input
                id={field}
                name={field}
                type={types[field]}
                placeholder={placeholders[field]}
                value={form[field]}
                onChange={handleChange}
                onBlur={handleBlur}
                maxLength={20}
                variant={
                  errors[field]
                    ? 'wrong'
                    : touched[field] && form[field]
                    ? 'correct'
                    : ''
                }
              />
              {errors[field] && (
                <p className="login-form__msg">{errors[field]}</p>
              )}
            </label>
          );
        })}
      </fieldset>

      <div className="login-form__ctrl">
        <Button type="submit" variant="primary">
          회원가입
        </Button>
        <Button as={Link} href="/" variant="secondary">
          뒤로가기
        </Button>
      </div>
    </form>
  );
};

export default RegisterForm;
