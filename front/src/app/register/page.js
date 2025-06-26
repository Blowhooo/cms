import Register from "@/components/common/Register";

export const metadata = {
  title: "완자와 주누의 Next 탐험 - 회원가입",
  description: "회원가입 후 서비스를 이용하세요.",
  robots: "noindex, nofollow",
};

const page = () => {
  return (
    <>
      <main id="app" role="main" aria-label="회원가입 페이지">
        <Register/>
      </main>
    </>
  );
}
export default page