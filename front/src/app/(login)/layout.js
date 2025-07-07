export default function Layout({children}) {
  return (
    <div className="w-full min-h-svh flex justify-center items-center">
      <main className="flex max-w-screen-sm w-full p-8 shadow-lg rounded-lg bg-white">
        {children}
      </main>
    </div>
  )
}