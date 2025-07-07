import axios from 'axios';
import TextInput from "../common/TextInput";
import Button from "../common/Button";

// axios.get('/auth/register')
//   .then(response => {
//     console.log(response.data);
//   })
//   .catch(error => {
//     console.error(error);
//   });


export default function RegisterForm() {
  const rgstForm = [
    {
      key : "id",
      cate : "아이디",
      type : "text",
      placeholder : "아이디를 입력해주세요.",
    },
    {
      key : "nickname",
      cate : "닉네임",
      type : "text",
      placeholder : "닉네임을 입력해주세요.",
    },
    {
      key : "password",
      cate : "비밀번호",
      type : "password",
      placeholder : "비밀번호를 입력해주세요.",
    },
    {
      key : "password-chk",
      cate : "비밀번호 확인",
      type : "password",
      placeholder : "비밀번호를 확인해주세요.",
    },
  ]

  const btnForm = [
    {
      text : "회원가입"
    },
    {
      text : "로그인 페이지로"
    }
  ]

  return (
    <form className="w-full">
      <h1 className="text-2xl font-semibold tracking-tight">회원가입</h1>
      <fieldset className="mt-4 flex flex-col gap-3">
        {
          rgstForm.map((item, idx) => (
            <label key={item.key} className="flex">
              <TextInput type={item.type} placeholder={item.placeholder} className="flex-1"/>
            </label>
          ))
        }

        <div className="flex gap-2">
          {
            btnForm.map((item, idx) => (
              <Button key={item.text} text={item.text} className="flex-1"/>
            ))
          }
        </div>
      </fieldset>
    </form>
  )

  
}