import React from 'react'
import Button from '@/components/ui/Button';
import Link from 'next/link';

const page = () => {
  return (    
    <section className="page-login" aria-labelledby="page-login-title">
      <div className="u-py-32 u-px-24 page-login__container">
        <div className="page-login__int">
          <h1 id="page-login-title" className="u-text-24 page-login__title">
            환영합니다!
          </h1>
          <p className="page-login__ment">
            앞으로 잘부탁드릴게요. 탐험가님!
          </p>            
        </div>
        <div className="page-login__ctrl u-mt-24">
          <Button
              as={Link}
              href="/"
            >
              로그인페이지로 이동하기
          </Button>
        </div>
      </div>
    </section>
  )
}

export default page