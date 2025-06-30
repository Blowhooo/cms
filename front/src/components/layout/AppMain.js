'use client';
import '@/components/features/styles/login.scss';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

const routeLabels = {
  '/home': '메인 페이지',
  '/register': '회원가입 페이지',
  '/': '로그인 페이지',
};

const AppMain = ({ children }) => {
  const pathname = usePathname();
  const [ariaLabel, setAriaLabel] = useState('기본 페이지');

  useEffect(() => {
    // 경로 길이 순으로 정렬하여 더 구체적인 경로를 먼저 매칭
    const sortedRoutes = Object.entries(routeLabels)
      .sort(([a], [b]) => b.length - a.length);
    
    const matchedRoute = sortedRoutes.find(([route]) => pathname === route || pathname.startsWith(route));
    const newLabel = matchedRoute?.[1] ?? '기본 페이지';
    
    setAriaLabel(newLabel);
  }, [pathname]);

  return (
    <div id="app" className="app" role="main" aria-label={ariaLabel}>
      {children}
    </div>
  );
};

export default AppMain;