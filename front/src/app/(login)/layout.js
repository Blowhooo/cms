

export default function Layout({children}) {
  return (
    <div className="w-full min-h-svh flex justify-center items-center">
      <main className="flex max-w-screen-lg w-full shadow-lg rounded-lg bg-white">
        <div className="w-1/2 bg-gray-100 py-16 px-8"></div>
        <div className="w-1/2 py-16 px-8">
          {children}
        </div>
      </main>
    </div>
  )
}