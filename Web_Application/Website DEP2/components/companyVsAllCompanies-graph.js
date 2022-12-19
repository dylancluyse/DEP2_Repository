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

const CompanyScoresView = ({
  naam,
  score_env,
  score_social,
  score_governance,
  perc_environment,
  per_social,
  perc_governance,
  simple_env_scores,
  simple_soc_scores,
  simple_gov_scores,
}) => {
  const data = [
    {
      name: naam,
      //score: score_env,
      perc: perc_environment,
      //simple: simple_env_scores,
    },
    {
      name: 'Gemiddelde',
      // score: score_social,
      perc: per_social,
      //simple: simple_soc_scores,
    },
  ];

  return (
    <Card class=' p-5 bg-gradient-to-r from-Grijs to-Grijs'>
      <CardContent class='grid justify-center grid-cols-1 gap-0.5 '>
        <Typography variant='p' component='p'>
          Scores {naam} vs gemiddelde alle bedrijven:
        </Typography>

        <BarChart
          width={380}
          height={280}
          data={data}
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
          {/* <Bar dataKey='score' fill='#8884d8' /> */}
          <Bar dataKey='perc' fill='#82ca9d' />
          {/* <Bar dataKey='simple' fill='#413ea0' /> */}
        </BarChart>
      </CardContent>
    </Card>
  );
};

const CompanyScoresOverview = (props) => {
  if (!props.company) {
    return <p>Please select a company.</p>;
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
          naam={company.naam}
          score_env={company.score_env}
          score_social={company.score_social}
          score_governance={company.score_governance}
          perc_environment={company.domein_environment}
          per_social={company.domein_social}
          perc_governance={company.domein_governance}
          simple_env_scores={company.simple_env_scores}
          simple_soc_scores={company.simple_soc_scores}
          simple_gov_scores={company.simple_gov_scores}
        />
      </div>
    </Box>
  );
};

export default CompanyScoresOverview;
