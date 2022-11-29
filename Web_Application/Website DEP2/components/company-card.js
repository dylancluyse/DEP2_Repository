import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import {useState, useEffect} from "react"
import useSWR, { mutate } from 'swr'
import fetcher from '../lib/fetcher'

const CompanyOverview = (props) => {
  // const [companies, setCompanies] = useState('')

  const { data: companyList, mutate: revalidateDomains, error } = useSWR(
    `http://localhost:8000/company/${props.company}`,
    fetcher
  )
  if (error) return <div>failed to load</div>
  if (!companyList) return <div>loading...</div>

  const {
    data : company
  } = companyList
  
  console.log(company)


  const complijst = Object.entries(company).map(prop =>{
    if (prop[1]) {
      return (
        <ListItemText primary={`${prop[0]}: ${prop[1]}`} />
      )
    }

  })

  console.log(complijst)
  return (
    <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      <List component="nav" aria-label="secondary mailbox folder">
        {complijst}
      </List>
    </Box>
  );
}

export default CompanyOverview;
