import { Chart } from 'chart.js/auto'
import DomainCard from '../sector-card'

(async function() {
  

  new Chart(
    document.getElementById('test'),
    {
      type: 'bar',
      data: {
        labels: DomainCard.map(row => row.year),
        datasets: [
          {
            label: 'Acquisitions by year',
            data: DomainCard.map(row => row.count)
          }
        ]
      }
    }
  );
})();