import { Link, Button } from '@mui/material';
import { useRouter } from 'next/router';

const Predict = () => {
  return (
    <div className=' min-h-screen py-2  max-h-screen bg-Grijs'>
      <a
        href='/'
        class=' absolute mt-2 mb-5 m-5 text-white bg-lichtblauw font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10'
      >
        Home
      </a>
      <main className='mt-28 flex flex-col items-center justify-center w-full flex-1 sm:px-20 my-10 '>
        <h1 className='text-4xl sm:text-6xl font-bold'>
          Admin - Predict Score
        </h1>

        <div className='space-x-10 mt-5'>
          <Button
            href='/admin/keywords'
            className=' m-5 text-white bg-lichtblauw hover:bg-gray-500 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10'
          >
            Add keywords
          </Button>
          <Button
            href='admin/predict'
            className=' m-5 text-white bg-lichtblauw hover:bg-gray-500 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10'
          >
            Predict company
          </Button>
        </div>
      </main>
    </div>
  );
};

export default Predict;
