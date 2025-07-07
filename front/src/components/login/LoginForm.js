

export default function LoginForm() {
  return (
    <form className="w-full">
      <h1 className="text-2xl font-semibold text-center tracking-tight">LOGIN</h1>
      <p className="font-medium tracking-tight"></p>
      <fieldset className="mt-4">
        <TextInput placeholder="아이디를 입력해주세요."/>
      </fieldset>
    </form>
  )
}