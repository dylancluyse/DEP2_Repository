import { Link } from '@mui/material';
import { useRouter } from 'next/router';
import CompanyList from '../../components/company-list-card.js';
import CompanyScores from '../../components/company-scores.js';
import CompanyGraph from '../../components/Company-score-graph.js';
import CompanyOverview from '../../components/company-card.js';
import { useState, useCallback } from 'react';
import React from 'react';
import {
  ComposedChart,
  Line,
  Area,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Scatter,
  ResponsiveContainer,
} from 'recharts';

const Post = () => {
  const router = useRouter();
  const { sectorname, company } = router.query;
  const data = [
    { name: 'Page A', uv: 400, mean: 375 },
    { name: 'Page B', uv: 500, mean: 375 },
    { name: 'Page C', uv: 500, mean: 375 },
    { name: 'Page D', uv: 600, mean: 375 },
  ];

  const [selectedCompany, setSelectedCompany] = useState('');

  const setSetterWithoutReload = useCallback((companyName) => {
    setSelectedCompany(companyName);
  }, []);

  const renderLineChart = (
    <ComposedChart width={380} height={350} padding={10} data={data}>
      <CartesianGrid stroke='#f5f5f5' />
      <XAxis dataKey='name' scale='band' />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey='uv' barSize={20} fill='#413ea0' />
      <Line type='monotone' dataKey='mean' stroke='#ff7300' />
    </ComposedChart>
  );

  return (
    <div class='overflow-hidden	'>
      <div>
        <a
          href='/'
          class='absolute mt-2 mb-5 m-5 text-white bg-blue-de-france hover:bg-blue-800  focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800'
        >
          back
        </a>
        <h1 class='sticky top-0 p-2 mx-10 mt-5 text-center text-2xl font-bold	'>
          {' '}
          {sectorname}
        </h1>
        <div class='sticky top-0 p-1 mx-10 mt-1 text-center text-xl'>
          <h2>Score sector:</h2>
        </div>
        <form class='flex items-center justify-start w-96 ml-5 pb-5'>
          <input
            class='flex-grow px-2 py-1 rounded-lg mr-2 w-16'
            type='text'
            placeholder='Search...'
            id='zoekBedrijfInSector'
          ></input>
          <button
            class='px-2 py-1 rounded-lg bg-blue-500 text-white'
            type='submit'
          >
            Search
          </button>
        </form>
      </div>
      <br />

      <div class='absolute text-left pl-2 flex flex-row h-screen w-full'>
        <CompanyList
          sector={sectorname}
          companySetter={setSetterWithoutReload}
        />
        <div class=' relative bg-gradient-to-r from-light-yellow to-light-yellow w-full text-black overflow-hidden'>
          {/* plaats voor gegevens bedrijf + grafieken */}

          <div class='grid grid-cols-3 grid-rows-2 gap-0.5"'>
            <div class='box row-start-1 row-end-1 col-start-1 col-end-3 '>
              <CompanyOverview company={selectedCompany} />
            </div>
            <div>
              <CompanyScores company={selectedCompany} />
            </div>
            <div class=''>
              <CompanyGraph company={selectedCompany} />
            </div>
            <div class=''>{renderLineChart}</div>
            <div class=''>{renderLineChart}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Post;
