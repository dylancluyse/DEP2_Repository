import { Link } from '@mui/material';
import { useRouter } from 'next/router';
import CompanyList from '../../components/company-list-card.js';
import CompanyOverview from '../../components/company-card.js';

const Post = () => {
  const router = useRouter();
  const { sectorname } = router.query;

  return (
    <div class='overflow-hidden	'>
      <Link href='/' class='sticky top-0'>
        Home{' '}
      </Link>

      <h1 class='static top-0 p-2 mx-10  bg-red-500 text-center text-2xl	font-bold	'>
        {' '}
        {sectorname}{' '}
      </h1>
      <br />
      <br />
      <div class='text-left pl-2 flex flex-row max-h-screen 	'>
        <CompanyList sector={sectorname} />
        <div class=' bg-gradient-to-r from-oxford-blue to-lighter-oxford w-full text-white	'>
          {/* plaats voor gegevens bedrijf + grafieken */}
          <p>TEST</p>
        </div>
      </div>
    </div>
  );
};

export default Post;
