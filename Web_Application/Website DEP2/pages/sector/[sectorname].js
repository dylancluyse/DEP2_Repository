import { Link } from '@mui/material';
import { useRouter } from 'next/router';
import CompanyList from '../../components/company-list-card.js';
import CompanyVsSector from '../../components/Companyvscompany-graph.js';
import CompanyVsCompany from '../../components/companyVsAllCompanies-graph.js';
import CompanyScores from '../../components/company-scores.js';
import CompanyGraph from '../../components/Company-score-graph.js';
import CompanyOverview from '../../components/company-card.js';
import { useState, useCallback } from 'react';
import React from 'react';
import { memo } from 'react';
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
import useSWR from 'swr';
import fetcher from '../../lib/fetcher';
import { CompanySubDomainScoresOverviewEnvironment, CompanySubDomainScoresOverviewGovernance, CompanySubDomainScoresOverviewSocial } from '../../components/company-subdomain-graph.js';

const Post = () => {
  const router = useRouter();
  const { sectorname, company } = router.query;

  const [selectedCompany, setSelectedCompany] = useState('');
  
  const sectorData = "";

  const { data: response, error } = useSWR(
    `http://localhost:8000/sector/data/${sectorname}`,
    fetcher
  );
  if (response) {
    const { data } = response;
    sectorData = data;
  }
  console.log(sectorData)

  const subdomainInformation = "";
  const { data: informationResponse  } = useSWR(
    `http://localhost:8000/data/subdomains`,
    fetcher
  );
  if (informationResponse) {
    const { data: dataResponse } = informationResponse;
    subdomainInformation = dataResponse;
  }




  const setSetterWithoutReload = useCallback((companyName) => {
    setSelectedCompany(companyName);
  }, []);


  return (
    <div class='overflow-hidden	'>
      <div>
        <a
          href='/'
          class='absolute mt-2 mb-5 m-5 text-white bg-blue-de-france hover:bg-blue-800  focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800 z-10'
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
      {/* //height set to auto to prevent the graph from being cut off */}
      <div class='absolute text-left pl-2 flex flex-row h-auto w-full '>
        <CompanyList
          sector={sectorname}
          companySetter={setSetterWithoutReload}
        />
        <div class=' relative bg-gradient-to-r from-light-yellow to-light-yellow w-full text-black overflow-hidden '>
          {/* plaats voor gegevens bedrijf + grafieken */}

          <div class='grid grid-cols-3 grid-rows-3 gap-0.5 '>
            <div class='box row-start-1 row-end-1 col-start-1 col-end-2 ml-24 mt-10 '>
              <CompanyOverview company={selectedCompany} />
            </div>
            <div>zoektermen</div>
            <div>
              <CompanyScores company={selectedCompany} />
            </div>
            <div class=''>
              <CompanyGraph company={selectedCompany} />
            </div>
            <div class=''>
              <CompanyVsSector company={selectedCompany} sectorData={sectorData} />
            </div>
            <div class=''>
            </div>
            <div class=''>
              <CompanySubDomainScoresOverviewEnvironment company={selectedCompany} sectorData={sectorData} subdomainInformation={subdomainInformation} />
            </div>
            <div class=''>
              <CompanySubDomainScoresOverviewSocial company={selectedCompany} sectorData={sectorData} subdomainInformation={subdomainInformation} />
            </div>
            <div class=''>
              <CompanySubDomainScoresOverviewGovernance company={selectedCompany} sectorData={sectorData} subdomainInformation={subdomainInformation} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Post;
