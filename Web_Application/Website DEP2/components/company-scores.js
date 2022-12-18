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

const CompanyScoresView = ({
  name,
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
  return (
    <Card class=' p-5 bg-gradient-to-r from-light-yellow to-light-yellow'>
      <CardContent class='grid justify-center grid-cols-1 gap-0.5 '>
        <Typography variant='h5' component='h2'>
          Scores:
        </Typography>
        <Typography>
          Environment: {Math.round(perc_environment * 100)}<sup>e</sup> percentiel
        </Typography>
        <Typography>
          Social: {Math.round(per_social * 100)}<sup>e</sup> percentiel
        </Typography>
        <Typography>
          Governance: {Math.round(perc_governance * 100)}<sup>e</sup> percentiel
        </Typography>
        <Typography>
          Simple Environment Score: {Math.round(simple_env_scores * 100) / 100}
        </Typography>
        <Typography>
          Simple Social Score: {Math.round(simple_soc_scores * 100) / 100}
        </Typography>
        <Typography>
          Simple Governance Score: {Math.round(simple_gov_scores * 100) / 100}
        </Typography>
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
        marginTop: '10px',
      }}
    >
      <div>
        <CompanyScoresView
          name={company.naam}
          score_env={company.subdomeinen_environment}
          score_social={company.subdomeinen_social}
          score_governance={company.subdomeinen_governance}
          perc_environment={company.domein_environment}
          per_social={company.domein_social}
          perc_governance={company.domein_governance}
          simple_env_scores={company.simple_env_scores}
          simple_soc_scores={company.simple_soc_scores}
          simple_gov_scores={company.simple_gov_scores}
          class='pl-4 pt-2'
        />
      </div>
    </Box>
  );
};

export default CompanyScoresOverview;
