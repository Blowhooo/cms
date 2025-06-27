import RegisterForm from './RegisterForm'


const Register = () => {
  return (
    <section className="page-login" aria-labelledby="rgst-title">
      <div className="u-py-32 u-px-24 page-login__container">
        <div className="page-login__int">
          <h1 id="rgst-title" className="u-text-24 page-login__title">
            환영합니다!
          </h1>
          <p className="page-login__ment">
            새로운 모험이 당신을 기다립니다!
          </p>
        </div>
        <RegisterForm/>
      </div>
    </section>
  )
} 

export default Register