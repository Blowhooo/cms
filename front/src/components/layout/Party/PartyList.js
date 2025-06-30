import Link from "next/link"

const PartyRoom = () => {
  const partyItems = [
    {
      "id" : 0,
      "name" : "탱커 한명 구합니다",
      "count" : 3,
    },
    {
      "id" : 1,
      "name" : "딜러 두명 구합니다",
      "count" : 2,
    },
    {
      "id" : 2,
      "name" : "힐러 한명 구합니다",
      "count" : 3,
    },
    {
      "id" : 3,
      "name" : "우리는 풀파티",
      "count" : 4,
    },
    {
      "id" : 4,
      "name" : "아무나 좀 와라 제ㅏㄹ.",
      "count" : 1,
    }
  ]
  return (
    <div className="party-list">
      <table className="party-list__tbl">
          <colgroup>
            <col className="party-list__col party-list__col--num" />
            <col className="party-list__col party-list__col--sbj" />
            <col className="party-list__col party-list__col--cnt" />
            <col className="party-list__col party-list__col--join" />
          </colgroup>
          <thead className="party-list__th">
            <tr className="party-list__tr">
                <th className="party-list__cell">방번호</th>
                <th className="party-list__cell">방제목</th>
                <th className="party-list__cell">참여 인원</th>
                <th className="party-list__cell">참여</th>
            </tr>
          </thead>
          <tbody className="party-list__tb">
            {
              partyItems.map((party, idx) => (
              <tr className="party-list__tr" key={party.id}>
                {
                  party.count > 0 ? (
                    <>
                      <td className="party-list__cell">{party.id}</td>
                      <td className="party-list__cell">
                        <Link href={`/party/${party.id}`} className="party-list__link">{party.name}</Link>
                      </td>
                      <td className="party-list__cell">{party.count} / 4</td>
                      <td className="party-list__cell">참여하기</td>
                    </>
                  ) : (
                    <td className="party-list__cell party-list__cell--empty" colSpan={3}>방이 존재하지 않습니다.</td>
                  )
                }
              </tr>
              ))
            }
          </tbody>
      </table>
    </div>
  )
}
export default PartyRoom