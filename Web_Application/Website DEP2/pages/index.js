import Head from 'next/head';
import { useEffect, useState } from 'react';
import LoadingDots from '../components/loading-dots';
import toast, { Toaster } from 'react-hot-toast';
import useSWR from 'swr';
import Image from 'next/image';
import DomainCard from '../components/domain-card';
import fetcher from '../lib/fetcher';
import DomainCardPlaceholder from '../components/domain-card-placeholder';
import Async from 'react-async';
import SectorList from '../components/sector-card.js';
import { Button } from '@mui/material';

export default function Home() {
  const [domain, setDomain] = useState('');

  // const { data: domainList, mutate: revalidateDomains } = useSWR(
  //   `/api/get-domains`,
  //   fetcher
  // )
  const [disabled, setDisabled] = useState(true);
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (domain.length == 0) {
      setDisabled(true);
    } else {
      setDisabled(false);
    }
  }, [domain]);

  useEffect(() => {
    if (adding) setDisabled(true);
  }, [adding]);

  return (
    <div className='flex flex-col items-center justify-center min-h-screen py-2  max-h-screen bg-Grijs'>
      <Head>
        <title>Bedrijven</title>
        <link rel='icon' href='/favicon.ico' />
      </Head>

      <Toaster
        position='bottom-right'
        toastOptions={{
          duration: 10000,
        }}
      />

      <main className='flex flex-col items-center justify-center w-full flex-1 sm:px-20 my-10 '>
        <h1 className='text-4xl sm:text-6xl font-bold'>Bedrijven</h1>

          <Button
            href='/admin'
            className=' m-5 text-white bg-lichtblauw hover:bg-gray-500 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10' >
            Dashboard
          </Button>
      </main>

      <SectorList />

      <footer className='flex items-center justify-center w-full h-10 border-t'>
        <a
          className='flex items-center justify-center'
          target='_blank'
          rel='noreferrer'
        >
          DEP groep 1
        </a>
      </footer>
    </div>
  );
}
