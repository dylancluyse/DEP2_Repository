import { Link, Button } from '@mui/material';
import { useRouter } from 'next/router';

const AdminPortal = () => {


  return (
    <div className='flex flex-col items-center justify-center min-h-screen py-2  max-h-screen bg-Grijs'>
      <main className='flex flex-col items-center justify-center w-full flex-1 sm:px-20 my-10 '>
        <a href='/' class='mt-2 mb-5 m-5 text-white bg-lichtblauw font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10' >
          Home
        </a>
        <h1 className='text-4xl sm:text-6xl font-bold'>Admin - SUOR SGE Portal Site</h1>

        <div>
          <Button href="/admin/keywords" className='mt-2 mb-5 m-5 text-white bg-lichtblauw hover:bg-gray-500 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10'>Add keywords</Button>
          <Button href="admin/predict" className='mt-2 mb-5 m-5 text-white bg-lichtblauw hover:bg-gray-500 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10'>Predict company</Button>
        </div>
      </main>
    </div>
  );
};

export default AdminPortal;
