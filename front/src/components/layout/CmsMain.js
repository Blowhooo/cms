import Link from 'next/link'
import './styles/cms.scss'

export const metadata = {
  title: "완자와 주누의 Next 탐험 - 메인",
  description: "CMS 메인페이지입니다. 탐험을 즐기세요!",
};

const CmsMain = ({ children }) => {
  return (
    <div className="cms-wrapper">
      <section className="cms-top u-p-16" aria-label="서비스명">
        <h1 className="cms-top__tit">CMS</h1>
      </section>

      <nav className="cms-nav u-p-16" aria-label="채널 탐색 메뉴">
        <ul className="cms-nav__list">
          <li className="cms-nav__item"><Link href="/" className="cms-nav__link">채널1</Link></li>
          <li className="cms-nav__item"><Link href="/" className="cms-nav__link">채널2</Link></li>
          <li className="cms-nav__item"><Link href="/" className="cms-nav__link">채널3</Link></li>
          <li className="cms-nav__item"><Link href="/" className="cms-nav__link">채널4</Link></li>
          <li className="cms-nav__item"><Link href="/party" className="cms-nav__link">레이드</Link></li>
        </ul>
      </nav>

      <header className="cms-header u-p-16">
        <h2 className="cms-header__tit">컨텐츠 타이틀</h2>
      </header>

      <main className="cms-layout u-p-16" id="main-content">
        {children}
      </main>

      <aside className="cms-aside u-p-16" aria-label="부가 정보">
        aside
      </aside>
    </div>
  )
}

export default CmsMain
