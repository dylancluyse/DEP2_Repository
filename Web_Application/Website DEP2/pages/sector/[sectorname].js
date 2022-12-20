import { useRouter } from 'next/router';
import CompanyList from '../../components/company-list-card.js';
import CompanyVsSector from '../../components/Companyvscompany-graph.js';
import CompanyScores from '../../components/company-scores.js';
import CompanyGraph from '../../components/Company-score-graph.js';
import CompanyOverview from '../../components/company-card.js';
import { useState, useCallback} from 'react';
import React from 'react';
import useSWR from 'swr';
import fetcher from '../../lib/fetcher';
import {
  CompanySubDomainScoresOverviewEnvironment,
  CompanySubDomainScoresOverviewGovernance,
  CompanySubDomainScoresOverviewSocial,
} from '../../components/company-subdomain-graph.js';

const Post = () => {
  const router = useRouter();
  const { sectorname, alphabetical} = router.query;

  if (!router.isReady) {
    return ""
  }

  const [selectedCompany, setSelectedCompany] = useState('');
  const [filter, setFilter] = useState(Boolean(alphabetical));
  const [isLoading, setLoading] = useState(true);

  const [searchQuery, setSearchQuery] = useState("")

  const sectorData = "";
  

  const { data: response, error } = useSWR(
    `http://localhost:8000/sector/data/${sectorname}`,
    fetcher
  );
  if (response) {
    const { data } = response;
    sectorData = data;
  }

  const subdomainInformation = '';
  const { data: informationResponse } = useSWR(
    `http://localhost:8000/data/subdomains`,
    fetcher
  );
  if (informationResponse) {
    const { data: dataResponse } = informationResponse;
    subdomainInformation = dataResponse;
  }

  const debouncedHandleChange = useCallback(
    (event) => {
      setLoading(true)
      setTimeout(() => {
        setSearchQuery(event)
      }, 500);
    },
    []
  );


  const setSetterWithoutReload = useCallback((companyName) => {
    setSelectedCompany(companyName);
  }, []);


  const handleRadioButtonClick = (value) => {
    setFilter(value)
    setLoading(true)
    router.replace({
      pathname: router.pathname,
      query: { ...router.query, alphabetical: value },
    }, undefined, { shallow: false });
  }

  return (
    <div class='overflow-hidden	'>
      <div>
        <a
          href='/'
          class='absolute mt-2 mb-5 m-5 text-white bg-lichtblauw font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10'
        >
          back
        </a>
        <h1 class='sticky top-0 p-2 mx-10 mt-5 text-center text-2xl font-bold	'>
          {' '}
          {sectorname}
        </h1>

        <form class='flex items-center justify-start w-96 ml-5 pb-5 mt-5'>
          <input
            class='flex-grow px-2 py-1 rounded-lg mr-2 w-16'
            type='text'
            placeholder='Search...'
            id='zoekBedrijfInSector'
            onChange={e => {debouncedHandleChange(e.target.value)}}
          />
          <button
            class='px-2 py-2 rounded-lg bg-lichtblauw text-white'
            type='submit'
          >
            Search
          </button>
        </form>
      </div>
      <div class="flex">
          <p className="pl-6 pr-5"> filter op: </p>

        <form action="">
          <input
            id="score"
            name="foo"
            type="radio"
            value={false}
            checked={!filter}
            onClick={() => handleRadioButtonClick(false)}
          />
          <label for="score" className="pl-2 pr-4">Score</label>
          <input
            name="foo"
            id="name"
            type="radio"
            value={true}
            checked={filter}
            onClick={() => handleRadioButtonClick(true)}
          />
          <label for="name" className="pl-2 pr-8">Naam</label>
        </form>
        {isLoading && <p> loading... </p> }

      </div>
      <br />
      {/* //height set to auto to prevent the graph from being cut off */}
      <div class='absolute text-left pl-2 flex flex-row h-auto w-full '>
        <CompanyList
          sector={sectorname}
          companySetter={setSetterWithoutReload}
          alphabetical={filter}
          isLoading={setLoading}
          searchQuery={searchQuery}
        />
        <div class=' relative bg-gradient-to-r from-Grijs to-Grijs w-full text-black overflow-hidden '>
          {/* plaats voor gegevens bedrijf + grafieken */}

          <div class='grid grid-cols-1 md:grid-cols-1 lg:grid-cols-3 grid-rows-3 gap-0.5'>
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
              <CompanyVsSector
                company={selectedCompany}
                sectorData={sectorData}
              />
            </div>
            <div class=''></div>
            <div class=''>
              <CompanySubDomainScoresOverviewEnvironment
                company={selectedCompany}
                sectorData={sectorData}
                subdomainInformation={subdomainInformation}
              />
            </div>
            <div class=''>
              <CompanySubDomainScoresOverviewSocial
                company={selectedCompany}
                sectorData={sectorData}
                subdomainInformation={subdomainInformation}
              />
            </div>
            <div class=''>
              <CompanySubDomainScoresOverviewGovernance
                company={selectedCompany}
                sectorData={sectorData}
                subdomainInformation={subdomainInformation}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Post;
