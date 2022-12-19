import useSWR from 'swr';
import fetcher from '../../lib/fetcher';


export default function fetch_sector_data(sectorName) {

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/company/data/${sectorName}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: company } = companyList;

  return company;

}
