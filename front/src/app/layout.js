import { Noto_Sans_KR } from 'next/font/google';
import Header from '@/components/client/Header';
import Footer from '@/components/client/Footer';
import "@/styles/globals.scss";
import "@/styles/utility.scss";
import "./client.scss";

const noto = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
});

export const metadata = {
  title: "완자와 주누의 Next 탐험",
  description: "Next를 알고 싶어요.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body className={noto.className}>
        <Header/>
        <div id="wrapper">
          <nav id="nav" className="nav u-p-16">메뉴</nav>
          <main id="main" className="main u-py-16 u-px-16">
            {children}
          </main>          
          <aside id="aside" className="aside u-p-16">사이드바</aside>
        </div>
        <Footer/>
      </body>
    </html>
  );
}
