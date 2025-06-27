import Register from "@/components/features/Register";

export const metadata = {
  title: "완자와 주누의 Next 탐험 - 회원가입",
  description: "회원가입 후 서비스를 이용하세요.",
  robots: "noindex, nofollow",
};

const page = () => {
  return (
    <>
      <Register/>
    </>
  );
}
export default page