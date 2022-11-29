import { Link } from '@mui/material'
import { useRouter } from 'next/router'
import CompanyList from '../../components/company-list-card.js'

const Post = () => {
  const router = useRouter()
  const { sectorname } = router.query

  return (
    <div>
      <Link href="/">Home </Link>
      <h1> {sectorname} </h1>
      <br/>
      <br/>
      <CompanyList sector={sectorname} / >
    </div>
  )
}

export default Post
