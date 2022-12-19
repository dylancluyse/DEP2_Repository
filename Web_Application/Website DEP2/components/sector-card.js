import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { useState, useEffect } from 'react';
import useSWR, { mutate } from 'swr';
import fetcher from '../lib/fetcher';

const SectorList = () => {
  const { data: companyList, error } = useSWR(
    `http://localhost:8000/sector`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: sectors } = companyList;

  const sector_lines = sectors.map((sector) => {
    const url = `http://localhost:3000/sector/${sector}`;
    return (
      <a
        href={url}
        className='bg-DonkerGrijs w-100 p-8 m-5 text-white rounded-lg'
      >
        {sector}
      </a>
    );
  });

  return (
    <div>
      <p class='text-center text-2xl'>Sectoren</p>
      <div class='grid grid-flow-row-dense grid-cols-3 grid-rows-3 gap-5 text-gray-500 border-gray-300 text-center '>
        {sector_lines}
      </div>
    </div>
  );
};

export default SectorList;
