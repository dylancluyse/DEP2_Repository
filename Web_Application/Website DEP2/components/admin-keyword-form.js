import {
  Box,
  FormControl,
  FormHelperText,
  Input,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import { useEffect, useState } from 'react';
import useSWR from 'swr';
import fetcher from '../lib/fetcher';

export default function AdminKeywordForm(props) {
  const { categories } = props;

  // const { data: keywords, error } = useSWR(
  //   `http://localhost:8000/admin/keywords`,
  //   fetcher
  // );
  // if (error) return <div>failed to load</div>;
  // if (!keywords) return <div>loading...</div>;
  //
  const menuItems = [];

  for (const [keyword, id] of Object.entries(categories)) {
    menuItems.push(<MenuItem value={id}>{keyword}</MenuItem>);
  }

  const [category, setCategory] = useState('');

  const handleChange = (event) => {
    setCategory(event.target.value);
    console.log(event.target.value);
  };

  return (
    <div className='snap-center p-5'>
      <Box component='form' aria-labelledby='category-a' sx={{ pl: 2 }}>
        <FormControl className='w-44 '>
          <InputLabel htmlFor='my-input' className=''>
            Kies een categorie:
          </InputLabel>
          <Select
            labelId='simple-select-label'
            id='simple-select'
            value={category}
            label='Age'
            onChange={handleChange}
          >
            {menuItems}
          </Select>
        </FormControl>
        <div className='mt-5'></div>
        <FormControl className=' m-5'>
          <InputLabel htmlFor='my-input-1' className='py-19'>
            Woord:
          </InputLabel>
          <Input
            id='my-input-1'
            className='py-19'
            aria-describedby='my-helper-text'
          />
        </FormControl>
      </Box>
    </div>
  );
}
