import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import {useState, useEffect} from "react"
import useSWR, { mutate } from 'swr'
import fetcher from '../lib/fetcher'

const CompanyList = (props) => {
  const sectorName = props.sector

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/sector/${sectorName}`,
    fetcher
  )
  if (error) return <div>failed to load</div>
  if (!companyList) return <div>loading...</div>

  const {
    data : companiesForSector
  } = companyList

  const complijst = companiesForSector.map(company =>{
    const url = `/company/${company.naam}`
          return (
            <ListItemButton key={`${company.ondernemingsnummer}`} component="a" href={url}>
              <ListItemText primary={`${company.naam}`} />
            </ListItemButton>
          )
  })
  return (
    <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      <List component="nav" aria-label="secondary mailbox folder">
        {complijst}
      </List>
    </Box>
  );
}

export default CompanyList;
