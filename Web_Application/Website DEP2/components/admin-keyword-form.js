import { useRouter } from 'next/router'
import {
  Box,
  Button,
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

  const menuItems = [];

  for (const [keyword, id] of Object.entries(categories)) {
    menuItems.push(<MenuItem value={id}>{keyword}</MenuItem>);
  }

  const [category, setCategory] = useState('');
  const [selectedKeyword, setSelectedKeyword] = useState('');

  const handleChange = (event) => {
    setCategory(event.target.value);
    console.log(event.target.value);
  };

  const handleInput = (event) => {
    setSelectedKeyword(event.target.value);
    console.log(selectedKeyword);
  };

  const [shouldAdd, setShouldAdd] = useState(false);
  const [shouldRemove, setShouldRemove] = useState(false);

  const {} = useSWR(
    !shouldAdd ? null : `http://localhost:8000/admin/keyword/add?category_id=${category}&keyword=${selectedKeyword}`,
    fetcher
  );

  const {} = useSWR(
    !shouldRemove ? null : `http://localhost:8000/admin/keyword/remove?category_id=${category}&keyword=${selectedKeyword}`,
    fetcher
  );

  const addKeyword = (event) => {
    setShouldAdd(true)
  };
//  

  const router = useRouter()

  const removeKeyword = (event) => {
    setShouldRemove(true)

    router.reload(window.location.pathname)

  };

  return (
    <div className='snap-center p-5'>
      <Box component='form' onSubmit={addKeyword} className='' aria-labelledby='category-a' sx={{ pl: 2 }}>
        <div className='flex w-full' >
          <div className='pr-10 w-1/4'>
        
          <FormControl  className='w-full flex mx-10'>
            <InputLabel htmlFor='my-input' className=''>
              Kies een categorie:
            </InputLabel>
            <Select
              labelId='simple-select-label'
              id='simple-select'
              value={category}
              label='Age'
              className=''
              onChange={handleChange}
            >
              {menuItems}
            </Select>
          </FormControl>

          </div>

          <div className='pr-10'>
        <FormControl className=' m-5'>
          <InputLabel htmlFor='my-input-1' className=''>
            Woord:
          </InputLabel>
          <Input
            id='my-input-1'
            className='w-full'
            aria-describedby='my-helper-text'
            onChange={handleInput}
          />
        </FormControl>
          </div>

          <Button type="submit" className=' m-5 text-white bg-lichtblauw hover:bg-gray-500 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10' >
            Add
          </Button>

          <Button onClick={removeKeyword} className=' m-5 text-white bg-lichtblauw hover:bg-gray-500 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10' >
            Remove
          </Button>
        </div>
      </Box>
    </div>
  );
}
