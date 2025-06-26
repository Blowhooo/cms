import Login from "@/components/common/Login";

export const metadata = {
  title: "완자와 주누의 Next 탐험 - 로그인",
  description: "계정에 로그인하여 서비스를 이용하세요.",
  robots: "noindex, nofollow",
};

const page = () => {
  return (
    <>
      <main id="app" className="app" role="main" aria-label="로그인 페이지">
        <Login/>
      </main>
    </>
  );
}
export default page