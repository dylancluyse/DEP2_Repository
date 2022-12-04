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
    <div className='flex flex-col items-center justify-center min-h-screen py-2  max-h-screen'>
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

      <main className='flex flex-col items-center justify-center w-full flex-1 sm:px-20 my-20'>
        <h1 className='text-4xl sm:text-6xl font-bold'>Bedrijven</h1>

        <form
          onSubmit={async (e) => {
            e.preventDefault();
            setAdding(true);
            try {
              await fetch(`/api/add-domain?domain=${domain}`);
              await revalidateDomains();
            } catch (error) {
              alert(error.message);
            } finally {
              setAdding(false);
            }
          }}
          className='flex justify-between space-x-4 px-5 w-full max-w-2xl h-10 mt-10'
        >
          <input
            type='text'
            name='domain'
            onInput={(e) => {
              setDomain(e.target.value);
            }}
            autoComplete='off'
            placeholder='sector'
            pattern='^(?:[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.)?[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
            required
            className='rounded-md border border-gray-300 focus:ring-0 focus:border-black px-4 flex-auto min-w-0 sm:text-sm'
          />
          <button
            type='submit'
            disabled={disabled}
            className={`${
              disabled
                ? 'cursor-not-allowed bg-gray-100 text-gray-500 border-gray-300'
                : 'bg-black text-white border-black hover:text-black hover:bg-white'
            } py-2 w-28 text-sm border-solid border rounded-md focus:outline-none transition-all ease-in-out duration-150`}
          >
            {adding ? <LoadingDots /> : 'search'}
          </button>
        </form>
      </main>

      <SectorList />

      <div></div>

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
