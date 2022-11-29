import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import {useState, useEffect} from "react"
import useSWR, { mutate } from 'swr'
import fetcher from '../lib/fetcher'

const BasicList = () => {
  const [companies, setCompanies] = useState('')

  const id = "ik_ben_een_id"

  const { data: companyList, mutate: revalidateDomains, error } = useSWR(
    `http://localhost:8000/sector/${id}`,
    fetcher
  )
  if (error) return <div>failed to load</div>
  if (!companyList) return <div>loading...</div>

  const {
    data : { items: foo }
  } = companyList

  console.log(foo)
  const complijst = foo.map(comp =>{
    const url = `/companies/${comp.id}`
          return (
            <ListItemButton component="a" href={url}>
              <ListItemText primary={`${comp.id}: ${comp.name}`} />
            </ListItemButton>
          )
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

export default BasicList;
