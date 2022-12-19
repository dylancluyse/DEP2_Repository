import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import makeStyles from '@mui/material/styles/makeStyles';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import useSWR, { mutate } from 'swr';
import fetcher from '../lib/fetcher';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import { formatGraphDataToPercentages } from '../utils/graphFormatter.js';

const CompanyScoresView = ({
  naam,
  companyScoreEnvironment,
  companyScoreSocial,
  companyScoreGovernance,
  sectorScoreEnvironment,
  sectorScoreSocial,
  sectorScoreGovernance,
  sectornaam,
}) => {
  const data = [
    {
      name: 'Environment',
      companyScore: companyScoreEnvironment,
      sectorScore: sectorScoreEnvironment,
    },
    {
      name: 'Social',
      companyScore: companyScoreSocial,
      sectorScore: sectorScoreSocial,
    },
    {
      name: 'Governance',
      companyScore: companyScoreGovernance,
      sectorScore: sectorScoreGovernance,
    },
  ];

  const formattedData = formatGraphDataToPercentages(data, [
    'companyScore',
    'sectorScore',
  ]);

  return (
    <Card class=' p-5 bg-gradient-to-r from-Grijs to-Grijs'>
      <CardContent class='grid justify-center grid-cols-1 gap-0.5 '>
        <Typography variant='p' component='p'>
          Scores {naam} vs gemiddelde van sector:
        </Typography>

        <BarChart
          width={380}
          height={280}
          data={formattedData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray='3 3' />
          <XAxis dataKey='name' />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey='companyScore' fill='#9ecb88' name={naam} />
          <Bar dataKey='sectorScore' fill='#6883BA' name={sectornaam} />
        </BarChart>
      </CardContent>
    </Card>
  );
};

const CompanyScoresOverview = (props) => {
  if (!props.company) {
    return '';
  }

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/company/${props.company}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: company } = companyList;

  const sectorData = props.sectorData;

  console.log(company);
  console.log(sectorData);

  return (
    <Box
      sx={{
        width: '100%',
        bgcolor: 'background.paper',
      }}
    >
      <div>
        <CompanyScoresView
          naam={company.naam}
          companyScoreEnvironment={company.domein_environment}
          companyScoreSocial={company.domein_social}
          companyScoreGovernance={company.domein_governance}
          sectorScoreEnvironment={sectorData.per_env[1]}
          sectorScoreSocial={sectorData.per_soc[1]}
          sectorScoreGovernance={sectorData.per_gov[1]}
          sectornaam={company.sectornaam}
        />
      </div>
    </Box>
  );
};

export default CompanyScoresOverview;
