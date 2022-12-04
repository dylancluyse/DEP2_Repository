import { Link } from '@mui/material'
import { useRouter } from 'next/router'
import CompanyOverview from '../../components/company-card.js'
import Bar from "./test.js"

const Foo = () => {
  const router = useRouter()
  const { company } = router.query
  Bar()

  return (
    <div>

      <canvas id="test"></canvas>
      <p>foo</p>

    </div>
  )
}

export default Foo
