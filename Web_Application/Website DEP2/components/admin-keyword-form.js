import { Box, FormControl, FormHelperText, Input, InputLabel, MenuItem, Select } from '@mui/material';
import { useEffect, useState } from 'react';
import useSWR from 'swr';
import fetcher from '../lib/fetcher';


export default function AdminKeywordForm(props) {

  const {categories} = props

  // const { data: keywords, error } = useSWR(
  //   `http://localhost:8000/admin/keywords`,
  //   fetcher
  // );
  // if (error) return <div>failed to load</div>;
  // if (!keywords) return <div>loading...</div>;
  //
  const menuItems = []

  for (const [keyword, id] of Object.entries(categories)) {
    menuItems.push(<MenuItem value={id}>{keyword}</MenuItem>);
  }
  
  const [category, setCategory] = useState('');

  const handleChange = (event) => {
    setCategory(event.target.value);
    console.log(event.target.value)
  };

  return (
    <div  className='border-2 w-full'>
    <Box component="form" aria-labelledby="category-a" sx={{ pl: 2 }} >
      <FormControl>
        <InputLabel htmlFor="my-input">Kies een categorie:</InputLabel>
      <Select
          labelId="simple-select-label"
          id="simple-select"
          value={category}
          label="Age"
          onChange={handleChange}
        >
          {menuItems}
        </Select>

        <InputLabel htmlFor="my-input-1" className='py-19'>TESTJE:</InputLabel>
        <Input id="my-input-1" className='py-19' aria-describedby="my-helper-text" />

        <FormHelperText id="my-helper-text">We'll never share your email.</FormHelperText>
      </FormControl>
    </Box>
    </div>
  )
}

