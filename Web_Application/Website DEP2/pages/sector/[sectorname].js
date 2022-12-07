import { Link } from '@mui/material';
import { useRouter } from 'next/router';
import CompanyList from '../../components/company-list-card.js';
import CompanyOverview from '../../components/company-card.js';
import { useState, useCallback } from 'react';

const Post = () => {
  const router = useRouter();
  const { sectorname, company } = router.query;

  const [selectedCompany, setSelectedCompany] = useState('');

  const setSetterWithoutReload = useCallback((companyName) => {
    setSelectedCompany(companyName);
  }, []);

  return (
    <div class='overflow-hidden	'>
      <div>
        <a
          href='/'
          class=' fixed mb-5 m-5 text-white bg-blue-de-france hover:bg-blue-800  focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800'
        >
          back
        </a>
        <h1 class='sticky top-0 p-2 mx-10 mt-5 text-center text-2xl font-bold	'>
          {' '}
          {sectorname}{' '}
        </h1>
      </div>

      <br />
      <br />

      <div class='absolute text-left pl-2 flex flex-row max-h-screen w-full	'>
        <CompanyList
          sector={sectorname}
          companySetter={setSetterWithoutReload}
        />
        <div class=' bg-gradient-to-r from-light-yellow to-light-yellow w-full text-black	'>
          {/* plaats voor gegevens bedrijf + grafieken */}
          <CompanyOverview company={selectedCompany} />
        </div>
      </div>
    </div>
  );
};

export default Post;
