import { Box } from '@mui/material';
import useSWR from 'swr';
import AdminKeywordForm from '../../components/admin-keyword-form';
import fetcher from '../../lib/fetcher';

const parseSubDomain = (subdomain, keywordList) => {
  const render = [];
  for (const subdom of Object.entries(keywordList.value)) {
    render.push(<li className='font-normal'>{subdom[1]}</li>);
  }

  return (
    <li className='pb-2 font-bold'>
      {subdomain}
      <Box component='ul' aria-labelledby='category-a' sx={{ pl: 2 }}>
        {render}
      </Box>
    </li>
  );
};

const createKeywordDomainList = (domain, keywords) => {
  const output = [];
  for (const [subdomain, subdomainKeywords] of Object.entries(keywords)) {
    output.push(parseSubDomain(subdomain, subdomainKeywords));
  }

  return (
    <Box
      component='ul'
      aria-labelledby='category-a'
      sx={{ pl: 2 }}
      className='border-2 p-2 '
    >
      <li>
        {domain}
        <Box component='ul' aria-labelledby='category-a' sx={{ pl: 2 }}>
          {output}
        </Box>
      </li>
    </Box>
  );
};

const createKeywordList = (fullList) => {
  const output = [];
  for (const [domain, keywords] of Object.entries(fullList)) {
    output.push(createKeywordDomainList(domain, keywords));
  }
  return <div className='flex mx-auto space-x-5 mb-10'>{output}</div>;
};

export default function keywords() {
  const { data: keywords, error } = useSWR(
    `http://localhost:8000/admin/keywords`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!keywords) return <div>loading...</div>;

  const {domains: doms, categories} = keywords;

  const foo = createKeywordList(doms);

  return (
    <div>
      <a
        href='/'
        class=' absolute mt-2 mb-5 m-5 text-white bg-lichtblauw font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10'
      >
        Home
      </a>
      <h1 className='text-center p-5 text-lg font-bold'> Keywords </h1>
      <div>
        <AdminKeywordForm categories={categories} />
      </div>
      <div className='flex mx-auto '>{foo}</div>
    </div>
  );
}
