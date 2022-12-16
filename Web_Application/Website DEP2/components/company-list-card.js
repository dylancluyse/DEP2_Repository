import * as React from 'react';
import { memo } from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { useState, useEffect } from 'react';
import useSWR, { mutate } from 'swr';
import fetcher from '../lib/fetcher';
import Router from 'next/router';

function doSomething(setter, company, foo, counter) {
  return function () {
    setter(company);
  };
}

const CompanyList = (props) => {
  const sectorName = props.sector;
  const { companySetter } = props;
  const [selectedIndex, setSelectedIndex] = React.useState(-1);

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/sector/${sectorName}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: companiesForSector } = companyList;

  const counter = -1;
  const complijst = companiesForSector.map((company) => {
    counter += 1;
    return (
      <ListItemButton
        key={`${company.ondernemingsnummer}`}
        component='a'
        selected={selectedIndex === counter}
        onClick={doSomething(
          companySetter,
          company.ondernemingsnummer,
          setSelectedIndex,
          counter
        )}
      >
        <ListItemText primary={`${company.naam}`} />
      </ListItemButton>
    );
  });
  return (
    <Box
      sx={{
        width: '100%',
        maxWidth: '20%',
        bgcolor: 'background.paper',
        overflow: 'scroll',
      }}
    >
      <List component='nav' aria-label='secondary mailbox folder'>
        {complijst}
      </List>
    </Box>
  );
};

export default memo(CompanyList);
