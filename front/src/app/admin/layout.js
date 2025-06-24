import { Noto_Sans_KR } from 'next/font/google';
import "@/styles/globals.scss";
import "@/styles/utility.scss";

const noto = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
});

export const metadata = {
  title: "윤주누 Next JS",
  description: "Next를 알고 싶어요.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body className={noto.className}>

        {children}
        <footer id="footer"></footer>
      </body>
    </html>
  );
}
