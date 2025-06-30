import '@/components/layout/styles/raid.scss'

export const metadata = {
  title: "완자와 주누의 Next 탐험 - 레이드",
  description: "CMS 레이드페이지입니다. 전투에서 승리하세요!",
};

const layout = ({children}) => {
  return (
    <main id="party" className="party">
      {children}
    </main>
  )
}
export default layout