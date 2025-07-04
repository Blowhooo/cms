import LoginForm from './LoginForm'


const Login = () => {
  return (
    <main className="page-login" aria-labelledby="page-login-title">
      <div className="u-py-32 u-px-24 page-login__container">
        <div className="page-login__int">
          <h1 id="page-login-title" className="u-text-24 page-login__title">
            환영합니다!
          </h1>
          <p className="page-login__ment">
            새로운 모험이 당신을 기다립니다
          </p>
        </div>
        <LoginForm />
      </div>
    </main>
  )
}

export default Login