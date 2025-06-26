import { Noto_Sans_KR } from 'next/font/google';
import "@/styles/globals.scss";
import "@/styles/utility.scss";
import "@/styles/layout.scss";

const noto = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
  display: 'swap',
});

export const metadata = {
  title: "완자와 주누의 Next 탐험",
  description: "완자와 주누의 Next 탐험",
  keywords: "Next.js, React, 웹개발, cms",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <body>
        {/* <a href="#wrapper" className="skip-link" aria-label="메인 콘텐츠로 바로가기">메인 콘텐츠로 바로가기</a> */}
        <div id="layout">
          
            {children}
          
        </div>
      </body>
    </html>
  );
}