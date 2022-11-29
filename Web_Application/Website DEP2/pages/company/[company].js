import { Link } from '@mui/material'
import { useRouter } from 'next/router'
import CompanyOverview from '../../components/company-card.js'

const Post = () => {
  const router = useRouter()
  const { company } = router.query

  return (
    <div>
      <Link href="/">Home </Link>
      <h1> {company} </h1>
      < CompanyOverview company={company} />
    </div>
  )
}

export default Post
