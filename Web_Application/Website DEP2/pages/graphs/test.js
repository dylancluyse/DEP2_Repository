import { Chart } from 'chart.js/auto'
import DomainCard from '../../components/domain-card';
import useSWR, { mutate } from 'swr'
import fetcher from '../../lib/fetcher';



const Bar = () => {

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/sector/Handel`,
    fetcher
  )
  if (error) return <div>failed to load</div>
  if (!companyList) return <div>loading...</div>

  const {
    data : companiesForSector
  } = companyList;


  (async function() {


    new Chart(
      document.getElementById('test'),
      {
        type: 'bar',
        data: {
          // x as
          labels: companiesForSector.map(row => row),
          datasets: [
            {
              label: 'Acquisitions by year',
              // y as
              data: companiesForSector.map(row => row.count)
            }
          ]
        }
      }
    );
  })();
}

export default Bar

