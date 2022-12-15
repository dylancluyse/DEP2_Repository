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

const CompanyView = ({ name, id, website, sector, foundingDate }) => {
  return (
    <Card class='p-5 bg-gradient-to-r from-light-yellow to-light-yellow'>
      <CardContent class='grid justify-center grid-cols-1 gap-0.5 '>
        <Typography variant='h5' component='h2'>
          {name}
        </Typography>
        <Typography color='textSecondary'>Ondernemingsnummer: {id}</Typography>
        <Typography color='textSecondary'>
          Website: <a href={website}>{website}</a>
        </Typography>
        <Typography color='textSecondary'>Sector: {sector}</Typography>
        <Typography color='textSecondary'>
          Founding Date: {foundingDate}
        </Typography>
      </CardContent>
    </Card>
  );
};

const CompanyOverview = (props) => {
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
        <CompanyView
          name={company.naam}
          id={company.ondernemingsnummer}
          website={company.website}
          sector={company.sectornaam}
          foundingDate={company.foundingdate}
          class='pl-4 pt-2'
        />
      </div>
    </Box>
  );
};

export default CompanyOverview;
