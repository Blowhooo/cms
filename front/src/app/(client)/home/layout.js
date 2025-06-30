import CmsMain from '@/components/layout/CmsMain';


export default function RootLayout({ children }) {
  return (
    <CmsMain>
      {children}
    </CmsMain>
  );
}