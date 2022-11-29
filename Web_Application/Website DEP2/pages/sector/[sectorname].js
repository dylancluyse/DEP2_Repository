import { useRouter } from 'next/router'
import BasicList from '../../components/company-list-card.js'

const Post = () => {
  const router = useRouter()
  const { sectorname } = router.query

  return (
    <div>
      <a href="/">Home </a>
      <h1> {sectorname} </h1>
      <br/>
      <br/>
      <BasicList/ >
    </div>
  )
}

export default Post
