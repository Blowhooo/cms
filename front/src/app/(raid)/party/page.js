import PartyList from '@/components/layout/Party/PartyList'
import PartyProfile from '@/components/layout/Party/PartyProfile'
const page = () => {
  return (
    <>
    <section className="party-section">
      <PartyList/>
    </section>
    <aside className="party-section">
      <PartyProfile/>
    </aside>
    </>
  )
}
export default page