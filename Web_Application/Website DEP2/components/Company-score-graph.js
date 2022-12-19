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
import { formatGraphDataToPercentages } from '../utils/graphFormatter';

const CompanyScoresView = ({
  name,
  scoreDomeinEnvironment,
  scoreDomeinSocial,
  scoreDomeinGovernance,
}) => {
  const data = [
    {
      name: 'Environment',
      score: scoreDomeinEnvironment,
    },
    {
      name: 'Social',
      score: scoreDomeinSocial,
    },
    {
      name: 'Governance',
      score: scoreDomeinGovernance,
    },
  ];

  const formattedData = formatGraphDataToPercentages(data, ["score"]) 

  return (
    <Card class=' p-5 bg-gradient-to-r from-light-yellow to-light-yellow'>
      <CardContent class='grid justify-center grid-cols-1 gap-0.5 '>
        <Typography variant='p' component='p'>
          Scores {name}:
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
          <Bar dataKey='score' fill='#8884d8' />
        </BarChart>
      </CardContent>
    </Card>
  );
};

const CompanyScoresOverview = (props) => {
  if (!props.company) {
    return "";
  }

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/company/${props.company}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: company } = companyList;

  return (
    <Box
      sx={{
        width: '100%',
        bgcolor: 'background.paper',
      }}
    >
      <div>
        <CompanyScoresView
          name={company.naam}
          scoreDomeinEnvironment={company.domein_environment}
          scoreDomeinSocial={company.domein_social}
          scoreDomeinGovernance={company.domein_governance}
        />
      </div>
    </Box>
  );
};

export default CompanyScoresOverview;
