import * as React from 'react';
import { memo } from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import useSWR from 'swr';
import fetcher from '../lib/fetcher';
import {useMemo} from 'react';

function doSomething(setter, company, foo, counter) {
  return function () {
    setter(company);
  };
}

const CompanyList = (props) => {
  const sectorName = props.sector;
  const { companySetter, searchQuery } = props;
  const [selectedIndex, setSelectedIndex] = React.useState(-1);

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/sector/${sectorName}?alphabetical=${props.alphabetical}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: companiesForSector } = companyList;

  if (!searchQuery) {
    searchQuery = ""
  }

  const results = companiesForSector.filter((company) =>
        company.naam.toLowerCase().includes(searchQuery.toLowerCase())
      );

  const counter = -1;
  const complijst = results.map((company) => {
    counter += 1;
    return (
      <ListItemButton
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
  props.isLoading(false)
  return (
    <Box
      sx={{
        width: '100%',
        maxWidth: '20%',
        bgcolor: 'background.paper',
        overflowY: 'scroll',
        overflowX: 'hidden',
        maxHeight: '160vh',
      }}
    >
      <List component='nav' aria-label='secondary mailbox folder'>
        {complijst}
      </List>
    </Box>
  );
};

export default memo(CompanyList);
