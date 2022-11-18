import { useRouter } from 'next/router'
import CompanyOverview from '../../components/company-card.js'

const Post = () => {
  const router = useRouter()
  const { company } = router.query

  return (
    <div>
      <a href="/">Home </a>
      <h1> {company} </h1>
      < CompanyOverview />
    </div>
  )
}

export default Post
