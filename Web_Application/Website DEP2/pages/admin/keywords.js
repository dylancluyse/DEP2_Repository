import { Box } from '@mui/material';
import useSWR from 'swr';
import fetcher from '../../lib/fetcher';


const parseSubDomain = (subdomain, keywordList) => {

  const render = [];
  for (const subdom of Object.entries(keywordList.value)) {
    render.push(<li className='font-normal'>{subdom[1]}</li>)
  }

  return (
    <li className="pb-2 font-bold">{subdomain}
      <Box component="ul" aria-labelledby="category-a" sx={{ pl: 2 }} >
        {render}
      </Box>
    </li>
  )
}

const createKeywordDomainList = (domain, keywords) => {
  const output = [];
  for (const [subdomain, subdomainKeywords] of Object.entries(keywords)) {
    output.push(parseSubDomain(subdomain, subdomainKeywords))
  }

  return (
    <Box component="ul" aria-labelledby="category-a" sx={{ pl: 2 }} className='border-2 ml-5'>
      <li>{domain}
        <Box component="ul" aria-labelledby="category-a" sx={{ pl: 2 }}>
          {output}
        </Box>
      </li>
    </Box>
  )
}

const createKeywordList = (fullList) => {
  console.log(fullList)
  const output = []
  for (const [domain, keywords] of Object.entries(fullList)) {
    output.push(createKeywordDomainList(domain, keywords))
  }
  return (
    <div className="flex">
      {output}
    </div>
  )
}

export default function keywords() {

  const { data: keywords, error } = useSWR(
    `http://localhost:8000/admin/keywords`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!keywords) return <div>loading...</div>;

  const foo = createKeywordList(keywords)

  return (
    <div>
      <h1> Keywords </h1>
      <div className="flex">
        <p> foo </p>    
      </div>
      <div className="flex">
        {foo}    
      </div>
    </div>
  )
}

