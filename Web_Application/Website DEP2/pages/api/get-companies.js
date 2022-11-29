export default async function handler(req, res) {
  const response = await fetch(
    `http://localhost:8000/foo`,
    {
      method: 'GET',
    }
  )
  const json = await response.json()

  // not required –> only for this demo to prevent removal of the demo's domain
  // const filteredDomains = json.domains.filter(
  //   (domain) => domain.name !== 'domains-api.vercel.app'
  // )

  res.status(response.status).send(json)
}
